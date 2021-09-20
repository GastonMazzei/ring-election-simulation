<b>A synchronous ring election</b> with one-directional (clockwise) communication <b>was simulated</b> using only one thread and one process (i.e. sequentially) in Python 3.

Real-valued UID's were sampled uniformly in [0,1] in order to measure both the time and communication complexity of the Chang and Robrts (LCR) algorithm <b>[1]</b>. 

<b>The following figure shows the results</b>. According to theory, the time complexity is O(n), worst-case communication complexity is O(n²), and average communication complexity is O(nlog(n)). In the figure it can be qualitatively noted that the theoretical average case complexity has been reproduced.

<img src="https://github.com/GastonMazzei/ring-election-simulation/blob/main/LCR-results.png" width=1000>

<b>Biblio</b>

<b>[1]</b> Ernest Chang; Rosemary Roberts (1979), "An improved algorithm for decentralized extrema-finding in circular configurations of processes", Communications of the ACM, ACM, 22 (5): 281–283, doi:10.1145/359104.359108
