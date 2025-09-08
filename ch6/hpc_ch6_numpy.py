#!/usr/bin/env python3
# To run this script, open a terminal run the command
#
# $ python hpc_ch6_numpy.py 
#
# In order to use the profiler run the command
#
# python -m cProfile -s cumulative hpc_ch6_numpy.py > log.txt
#
# The output with the profiler informtation will be redirected to a text file.
# We can also use a cprofile format for the statistics
#
# $ python -m cProfile -o profile.stats hpc_ch6_numpy.py
#
import numpy as np
from numpy import zeros, roll
import time

def laplacian(grid):
    return (
        roll(grid, +1, 0) +
        roll(grid, -1, 0) +
        roll(grid, +1, 1) +
        roll(grid, -1, 1) -
        4 * grid
    )

def evolve(grid, dt, D=1):
    return grid + dt * D * laplacian(grid)

def run_experiment(num_iterations):
    grid_shape = (640, 640)
    grid = zeros(grid_shape)
    
    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005
    
    start = time.time()
    for i in range(num_iterations):
        grid = evolve(grid, 0.1)
    return time.time() - start

if __name__ == "__main__":
    exec_time = run_experiment(500)
    print('execution time: {:.2f} sec.'.format(exec_time))
