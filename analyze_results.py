from math import log2
import sys

import numpy as np

from math import log2
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

with open('results.txt','r') as f:
    data = f.readlines()

# check that the results are divisible by 4
assert(len(data) % 4==0)

# check that every index multiple of 4 is the string:
# "A leader was elected!\n"
for i in range(len(data)//4):
    assert(data[i * 4] == "A leader was elected!\n")

# Populate the statistics with results
L, N_r, N_c = [],[],[]
for i in range(len(data)//4):
    try:
        L += [int(data[i * 4 + 1][20:-1])]
        N_r += [int(data[i * 4 + 2][18:-1])]
        N_c += [int(data[i * 4 + 3][26:-1])]
    except:
        print('ERR: Unknown error occurred with the following data:')
        print(data[i*4+1:i*4+4])
        sys.exit(1)

# check that they all have the same length
assert(len(L)==len(N_r)==len(N_c))


# Compute  mean for each ring size
THR = 3
pairs = list(zip(L, N_c))
uniques = list(set(L))
various = {u:[] for u in uniques}
for p in pairs:
    various[p[0]].append(p[1])
s = sorted(various.keys())
s = [s_ for s_ in s if len(various[s_])>=THR]
v=[]
for s_ in s:
    v_ = various[s_]
    v += [sum(v_)/len(v_)]

def model(x, a,b,c,d):
    return a+b*x*np.log2(c*x+1)

# Plot
plt.scatter(L,N_c, c='b', label='# communications')


if False:
    N_c = np.asarray(N_c)
    L = np.asarray(L)
    thr = min(L) + 0.99*(max(L)-min(L))
    mask = np.where(L>thr,True,False)
    popt, pcov = curve_fit(model, 
                        L[mask],
                        N_c[mask],
                        maxfev=20000, bounds=(0,10000000))
else:
    popt, pcov = curve_fit(model, 
                        s,
                        v,
                        maxfev=20000, bounds=(0,10000000))

plt.plot(sorted(L), [model(L_, *popt)  for L_ in sorted(L)], lw=4, c='r',label=r'$f(x)=a+bxlog_2(cx+1)$ fit of the mean'+f'\na={round(popt[0],2)}, b={round(popt[1],2)}, c={round(popt[2],2)}')

# --QUADRATIC FIT--
pquad = np.polyfit(s,v,2)
plt.plot(sorted(L), np.polyval(pquad,
    sorted(L)), c='g', lw=2,ls='dashdot', label=r'$f(x)=ax^2+bx$ fit  of the  mean'+f'\na={round(pquad[0],2)}, b={round(pquad[1],2)}')

# --QUADRATIC FIT--
if False:
    plt.plot(sorted(L), np.polyval(np.polyfit(s, v, 1),
        sorted(L)), c='y', lw=2,ls='--', label=r'$f(x)=x$')


plt.xlabel(r'$Ring Size')
plt.plot(s,v,c='k',ls=':',lw=4,label='mean')
plt.ylabel(r'$# Communications')
plt.grid()
plt.title('LCR Algorithm - numerical simulation\n(N is too small to distinguish quadratic and log(n) behaviour)')
plt.legend()
plt.show()

