Ch.10 Clusters and job queues
=============================
A cluster of nodes is used when the resources that are needed to run an application (memory, storage, latency) are beyond  what can be used in one single node, in other words when a node cannot be scaled up vertically. One other reason to set up a cluster is to avoid one single point of failure. The nodes that are members of a cluster needs to communicate so all the cluster frameworks use an internal communication system or use an external one. Among the many cluster frameworks available three are described.  

* [IPython Parallel](https://ipyparallel.readthedocs.io/en/latest/index.html#)
* [NSQ](https://nsq.io/)
* [Dask](https://www.dask.org/)