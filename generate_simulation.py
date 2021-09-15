import multiprocessing

import sys

from uuid import uuid4

algorithm = 'LCR'

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


def transition(P):
    if algorithm=='LCR':
        if P.cim[0]!=None:
            if P.u == P.cim[0]:
                P.leader = True
                P.com = [None]
            elif P.u < P.cim[0]:
                P.com = P.cim
            else:
                P.com = [None]
    else:
        pass

def populate_states_and_channels(p):
    # apply a particular criteria for the initial condition
    # of both the message channels and processor'states
    if algorithm=='LCR':
        p.com[0] = p.u
    else:
        pass

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
    if algorithm=='LCR':
        for i,p in enumerate(ring):
            print(f'Processor {i} sends the message: {p.com}')
    else:
        pass

def update_complexity(ring):
    ring.rounds += 1
    for p in ring.ring:
        if p.com[0]!=None:
            ring.communications += 1
        if p.aom[0]!=None:
            ring.communications += 1

class ProcessorRing():
    def __init__(self, N, verbose=True):
        self.ring = [Processor() for _ in range(N)]
        self.communications = 0
        self.rounds = 0
        self.verbose = verbose
        for p in self.ring:
            populate_states_and_channels(p)
            update_complexity(self)
        if self.verbose:
            report_messages(self.ring)
    def transition_function(self):
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

   
def main(N, VERBOSITY=False):
    R = N
    ring = ProcessorRing(N, verbose=VERBOSITY)
    if VERBOSITY:
        print('\n\n')
    for iteration in range(R):
        ring.transition_function()
        if VERBOSITY:
            print('\n\n')


if __name__ == "__main__":

    # Define parameters
    VERBOSITY=False

    for N in range(5,200):
        for _ in range(100):
            try:
                main(N)
            except:
                pass
