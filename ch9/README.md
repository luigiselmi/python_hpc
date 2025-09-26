Ch.9 Multiprocessing
====================
We can use 1 or all the cores available in the machine. Each core can run one process and each process can run one or more threads. Thread and processes are called workers since they are responsible for a share of the calculations.

## Script example 
The [pi_parallel_worker.py](pi_parallel_worker.py) script estimate Pi using Threads and Processes. The script computes PI as the ratio of the number of random points that fall into a circle and those N that fall on the square that includes the circle. The method is called Monte Carlo. The type of task is called *embarrassingly parallel* because it can be easily parallelized since parallel threads or processes do not need to communicate to perform the task. We can use 1 or all the cores available in the machine. Each core can run one process and each process can run one or more threads. Thread and processes are called workers since they are responsible for a share of the calculations. The number of cores to be used must be provided when executing the script, e.g. 4. The multiprocessing module creates a pool of worker and send the function to be executed and its argument to each worker. Two algorithms are available for the computation of the number of points that fall in the quarter circle: one based on Python and one based on NumPy. The default algorithm is based on Python. The two algorithms can be compared to see the the difference in performances.
```
$ python pi_parallel_worker.py --algorithm numpy 4
```
The default settings uses Threads as workers. In this case only one CPU core is used with 4
threads. In order to use the other CPU cores with processes we have to use
```
$ python pi_parallel_worker.py --processes 4
```
We can change the number N of random points by setting the argument --nbr_samples_in_total
```
$ python pi_parallel_worker.py --processes --nbr_samples_in_total 100000 4
```
