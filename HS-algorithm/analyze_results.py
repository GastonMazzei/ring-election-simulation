
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
L = [log2(x) for x in L]
N_r = [log2(x) for x in N_r]
N_c = [log2(x) for x in N_c]


# Fit the slope of the polinomial
sorted_L = sorted(L)
p_r = np.polyfit(L, N_r, 1)
p_c = np.polyfit(L, N_c, 1)



# Plot
plt.scatter(L,N_r, c='r', label='# rounds')
plt.plot(sorted_L, np.polyval(p_r, sorted_L), c='r', label=r'$y(x)=x^\alpha$, '\
                                                        r'$\alpha$='+f'{round(p_r[0],2)}')
plt.plot(sorted_L, np.polyval(p_c, sorted_L), c='b', label=r'$y(x)=x^\beta$, '\
                                                        r'$\beta$='+f'{round(p_c[0],2)}')
plt.scatter(L,N_c, c='b', label='# communications')
plt.legend()
plt.xlabel(r'$log_2$(Ring Size)')
plt.ylabel(r'$log_2$(variable)')
plt.grid()
plt.title('HS Algorithm (numerical simulation)')
plt.show()

