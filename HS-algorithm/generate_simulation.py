import multiprocessing

import sys

from uuid import uuid4

algorithm = ['LCR', 'HS'][1]

class Processor():
    def __init__(self):
        self.leader = False
        self.u = int(str(uuid4().int)[:16])
        self.state = []
        # clockwise inward message
        self.cim = [None]
        # clockwise outward message
        self.com = [None]
        # anti-clockwise inward message
        self.aim = [None]
        # anti-clockwise outward message
        self.aom = [None]


def load_messages(Pc, Pn1, Pn2):
    # Pc: Processor_current
    # Pn1: Processor_neighbor1
    # Pn2: Processor_neighbor2
    Pc.cim = Pn1.com
    Pc.aim = Pn2.aom



def transition(P: Processor):
    DEBUG = [True, False][1]
    if DEBUG: print(f'Processor with uid: {P.u}')
    if algorithm=='LCR':
        if P.cim[0]!=None:
            if P.u == P.cim[0]:
                P.leader = True
                P.com = [None]
            elif P.u < P.cim[0]:
                P.com = P.cim
            else:
                P.com = [None]
    elif algorithm=='HS':
        P.com = [None]*3
        P.aom = [None]*3
        if P.cim[1] == 'out':
            if P.cim[0] > P.u:
                assert(P.cim[-1] >= 1)
                if P.cim[-1] > 1:
                    P.com = P.cim[:-1] + [P.cim[-1] - 1]
                    if DEBUG: print("A")
                else:
                    P.aom = [P.cim[0], 'in', 1]
                    if DEBUG: print("B")
            elif P.cim[0] == P.u:
                P.leader = True
        if P.aim[1] == 'out':
            if P.aim[0] > P.u:
                assert(P.aim[-1] >= 1)
                if  P.aim[-1] > 1:
                    P.aom = P.aim[:-1] + [P.aim[-1] - 1]
                    if DEBUG: print("C")
                else:
                    P.com = [P.aim[0], 'in', 1]
                    if DEBUG: print("D")
            elif P.cim[0] == P.u:
                P.leader = True
        if P.cim[1] == 'in' and P.cim[0] != P.u:
            P.com = [P.cim[0], 'in', 1]
        if P.aim[1] == 'in' and P.aim[0] != P.u:
            P.aom = [P.aim[0], 'in', 1]
        if (P.cim[1] == 'in' and P.cim[2] == 1 and P.cim == P.aim):
            P.state[0] += 1
            P.com = [P.u, 'out', 2 ** P.state[0]]
            P.aom = [P.u, 'out', 2 ** P.state[0]]

def populate_states_and_channels(P: Processor):
    # apply a particular criteria for the initial condition
    # of both the message channels and processor'states
    if algorithm == 'LCR':
        P.com[0] = P.u
    elif algorithm == 'HS':
        P.state = [0] # [phase]
        P.com = [P.u,'out',1] # 2^phase 
        P.aom = [P.u,'out',1]


def check_leader(ring):        
    s = sum([p.leader for p in ring.ring])
    if s==1:
        print(f'A leader was elected!')
        ring.complexity_report()
        sys.exit(0)
    elif s>1:
        print(f'Algorithm failed: more than one leader was elected')
        sys.exit(1)

def report_messages(ring):
    sep = '--------------------------------------------'
    if algorithm=='LCR':
        for i,p in enumerate(ring):
            print(f'Processor {i} sends the message: {p.com}')
    elif algorithm=='HS':
        for i,p in enumerate(ring):
            print(sep)
            print(f'Processor {i} sends the messages:\n(clockwise) {p.com}\n(anticlock) {p.aom}')

def update_complexity(ring):
    ring.rounds += 1
    if algorithm == 'LCR':
        for p in ring.ring:
            if p.com[0]!=None:
                ring.communications += 1
            if p.aom[0]!=None:
                ring.communications += 1
    if algorithm == 'HS':
        for p in ring.ring:
            if p.com!=[None]*3:
                ring.communications += 1
            if p.aom!=[None]*3:
                ring.communications += 1

class ProcessorRing():
    def __init__(self, N, verbose=True):
        self.ring = [Processor() for _ in range(N)]
        self.ring_size = N
        self.communications = 0
        self.rounds = 0
        self.verbose = verbose
        for p in self.ring:
            populate_states_and_channels(p)
            update_complexity(self)
        if self.verbose:
            report_messages(self.ring)
    def transition_function(self):
        N = self.ring_size
        for i in range(N):
            load_messages(self.ring[i], self.ring[(i-1)%N], self.ring[(i+1)%N])
        for i in range(N):
            transition(self.ring[i])
        update_complexity(self)
        # Check if a leader was elected
        check_leader(self)
        # Report the messages in the network
        if self.verbose:
            report_messages(self.ring)
    def complexity_report(self):
        print(f'length of the ring: {len(self.ring)}')
        print(f'number of rounds: {self.rounds}')
        print(f'number of communications: {self.communications}')

   
def main(N, R, VERBOSITY=False):
    ring = ProcessorRing(N, verbose=VERBOSITY)
    if VERBOSITY:
        print('\n\n')
    for iteration in range(R):
        ring.transition_function()
        if VERBOSITY:
            print('\n\n')


if __name__ == "__main__":

    # Define parameters
    VERBOSITY = False
    TEST = [True, False][1]
    
    if TEST:
        VERBOSITY = [True, False][1]
        main(5, 20, VERBOSITY = VERBOSITY)
    else:
        for N in range(5,200):
            for _ in range(100):
                try:
                    main(N, N**3)
                except:
                    pass
