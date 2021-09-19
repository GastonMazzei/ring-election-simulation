from math import log2
import sys

import numpy as np

from math import log2
from matplotlib import pyplot as plt

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


# Apply the log_2 function to data



# Plot
plt.scatter(L,N_c, c='b', label='# communications')


def model(x, a,b,c):
    return a+b*x*np.log2(x*c)


from scipy.optimize import curve_fit

L = np.asarray(L)
N_c = np.asarray(N_c)
thr = min(L) + 0.75*(max(L)-min(L))
mask = np.where(L>thr,True,False)
popt, pcov = curve_fit(model, 
                        L[mask],
                        N_c[mask],
                        maxfev=20000)

plt.plot(sorted(L), [model(L_, *popt)  for L_ in sorted(L)], c='r',label=r'$f(x)=xlog_2(x)$')

plt.plot(sorted(L), np.polyval(np.polyfit(L, N_c, 2),
    sorted(L)), c='g', label=r'$f(x)=x^2$')
plt.legend()
plt.xlabel(r'$Ring Size')
plt.plot(sorted(L), np.polyval(np.polyfit(L, N_c, 1),
    sorted(L)), c='k', label=r'$f(x)=x$')
plt.ylabel(r'$# Communications')
plt.grid()
plt.title('LCR Algorithm (numerical simulation)')
plt.show()

