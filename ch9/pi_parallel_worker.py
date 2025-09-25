# This script estimate Pi using Threads and Processes
# The script computes PI as the ratio of the number of random points that fall into 
# a circle and those N that fall on the square that includes the circle. The method is 
# called Monte Carlo. The type of task is called *embarrassingly parallel* because it
# can be easily parallelized since parallel threads or processes do not need to communicate
# to perform the task. We can use 1 or all the cores available in the machine. Each core
# can run one process and each process can run one or more threads. Thread and processes 
# are called workers since they are responsible for a share of the calculations. 
# The number of cores to be used must be provided when executing the script, e.g. 4.
# The multiprocessing module creates a pool of worker and send the function to be executed 
# and its argument to each worker.
#
# $ python pi_parallel_worker.py 4
#
# The default settings uses Threads as workers. In this case only one CPU core is used with 4
# threads. In order to use the other CPU cores with processes we have to use
#
# $ python pi_parallel_worker.py --processes 4
#
# We can change the number N of random points by setting the argument --nbr_samples_in_total
#
#  $ python pi_parallel_worker.py --processes --nbr_samples_in_total 100000 4
#
import os
import random
import time
import argparse
import numpy as np
import multiprocessing

def estimate_nbr_points_in_quarter_circle_python(nbr_estimates):
    """Monte carlo estimate of the number of points in a quarter circle using pure Python"""
    print(f"Executing estimate_nbr_points_in_quarter_circle with {nbr_estimates:,} on pid {os.getpid()}")
    nbr_trials_in_quarter_unit_circle = 0
    for step in range(int(nbr_estimates)):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        is_in_unit_circle = x * x + y * y <= 1.0
        nbr_trials_in_quarter_unit_circle += is_in_unit_circle

    return nbr_trials_in_quarter_unit_circle

def estimate_nbr_points_in_quarter_circle_numpy(nbr_samples):
    """Estimate Pi using vectorised numpy arrays"""
    np.random.seed() # remember to set the seed per process
    xs = np.random.uniform(0, 1, nbr_samples)
    ys = np.random.uniform(0, 1, nbr_samples)
    estimate_inside_quarter_unit_circle = (xs * xs + ys * ys) <= 1
    nbr_trials_in_quarter_unit_circle = np.sum(estimate_inside_quarter_unit_circle)
    return nbr_trials_in_quarter_unit_circle

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('nbr_workers', type=int, help='Number of workers e.g. 1, 2, 4, 8')
    parser.add_argument('--nbr_samples_in_total', type=int, default=1e8, help='Number of samples in total e.g. 100000000')
    parser.add_argument('--processes', action="store_true", default=False, help='True if using Processes, absent (False) for Threads')

    print('Number of cores: ', multiprocessing.cpu_count())

    args = parser.parse_args()
    if args.processes:
        print("Using Processes")
        from multiprocessing import Pool
    else:
        print("Using Threads")
        from multiprocessing.dummy import Pool

    nbr_samples_in_total = int(args.nbr_samples_in_total)  # should be 1e8
    nbr_parallel_blocks = int(args.nbr_workers)

    pool = Pool()

    nbr_samples_per_worker = int(nbr_samples_in_total / nbr_parallel_blocks)
    print("Making {} samples per worker".format(nbr_samples_per_worker))

    # confirm we have an integer number of jobs to distribute
    assert nbr_samples_per_worker == int(nbr_samples_per_worker)
    nbr_samples_per_worker == int(nbr_samples_per_worker)
    map_inputs = [nbr_samples_per_worker] * nbr_parallel_blocks
    t1 = time.time()
    results = pool.map(estimate_nbr_points_in_quarter_circle_python, map_inputs)
    pool.close()
    exec_time = time.time() - t1
    print("Dart throws in unit circle per worker:", results)
    print('Took {:.2f} s'.format(exec_time))
    nbr_in_circle = sum(results)
    combined_nbr_samples = sum(map_inputs)

    pi_estimate = float(nbr_in_circle) / combined_nbr_samples * 4
    print("Estimated pi", pi_estimate)
    print("Pi", np.pi)