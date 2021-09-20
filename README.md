<b>A synchronous ring election</b> with one-directional (clockwise) communication <b>was simulated</b> using only one thread and one process (i.e. sequentially) in Python 3.

UID's were sampled using the 4th version of UUID <b>[1]</b> in order to measure both the time and communication complexity of the Chang and Robrts (LCR) algorithm <b>[2]</b>. 

<b>The following figure shows the results</b>. According to theory, the time complexity is O(n), worst-case communication complexity is O(n²), and average communication complexity is O(nlog(n)). Nevertheless, fitting the last two functions  over the communication cost per ring size so-far collapses to a linear parametrization. In order to "go deeper", i.e. try rings an order of magnitude bigger, the simulation was migrated to Google Colab and the results are yet to be tested..

<img src="https://github.com/GastonMazzei/ring-election-simulation/blob/main/LCR-results.png" width=1000>

<b>Biblio</b>

<b>[1]</b> https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)

<b>[2]</b> Ernest Chang; Rosemary Roberts (1979), "An improved algorithm for decentralized extrema-finding in circular configurations of processes", Communications of the ACM, ACM, 22 (5): 281–283, doi:10.1145/359104.359108
