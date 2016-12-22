# DOSCIS-simple-queue-simulator
A simple discrete event simulator based on DOCSIS, for visualizing the dynamics of a queue during some simulation time an the mean waiting time for every package in it.
It contains a Token Bucket algorithm for shapping the traffic rate in the queue.

Example of using:
Include the SimuladorDOCSIS.py file and run:

simQueue(10,1,15,20)
Where:
- 10 is the number of subscribers in the system. It will be simulated a CMTS node with transmission capacity of 800Mb, equally distributed to 10 subscribers (queues). That means the analized queue will have a arrival rate of 800/10 = 80 Mbps.
- 1 is the simulation total time (simulation will last 1s).
- 15 is the Token bucket fill rate. It means the subscriber bought a 15Mbps limited broadband internet from the CATV operator. The token bucket algorithm is responsible to shape the transmission rate to the client's cable modem.
- 20 is the queue service rate. It means the rate that packages are processed in the queue, leaving it and letting the next package be attended.

Other parameters can be modified when calling a function. Check the simQueue function in the code for additional information on its utilization.


