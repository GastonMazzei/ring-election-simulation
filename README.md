<b>A synchronous ring election</b> with one-directional (clockwise) communication <b>was simulated</b> using only one thread and one process (i.e. sequentially) in Python 3.

UID's were sampled using the 4th version of UUID <b>[1]</b> in order to measure both the time and communication complexity of the Chang and Robrts (LCR) algorithm <b>[2]</b>. 

<b>The following figure shows the results</b>, were in accordance with theory, i.e. time complexity is O(n) and communication complexity is O(n²), with "n" the number of nodes in the ring.

<img src="https://github.com/GastonMazzei/ring-election-simulation/blob/main/results.png" width=1000>

<b>Biblio</b>

<b>[1]</b> https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)

<b>[2]</b> Ernest Chang; Rosemary Roberts (1979), "An improved algorithm for decentralized extrema-finding in circular configurations of processes", Communications of the ACM, ACM, 22 (5): 281–283, doi:10.1145/359104.359108
