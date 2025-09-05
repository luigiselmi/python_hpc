# This script performs the same task as the Jupyter notebook with the same name.
# To run this script, open a terminal run the command
#
# $ python hpc_ch2.py 
#
# In order to use the profiler run the command
#
# python -m cProfile -s cumulative hpc_ch2.py > log.txt
#
# The output with the profiler informtation will be redirected to a text file.
# We can also use a cprofile format for the statistics
#
# $ python -m cProfile -o profile.stats hpc_ch2.py
#
# The line_profiler (to be installed) provides the timing for each line in the script
#
# $ python kernprof -l -v julia1_lineprofiler.py
#
# python -m cProfile -o profile.stats hpc_ch2.py
import math
from PIL import Image
import array
import time
import matplotlib.pyplot as plt
from functools import wraps
#--------------------------------------------------------------------------------------------------
#                                             Functions 
#--------------------------------------------------------------------------------------------------
def show_false_greyscale(output_raw, width, height, max_iterations):
    """Convert list to array, show using PIL"""
    # convert our output to PIL-compatible input
    assert width * height == len(output_raw)  # sanity check our 1D array and desired 2D form
    # rescale output_raw to be in the inclusive range [0..255]
    max_value = float(max(output_raw))
    output_raw_limited = [int(float(o) / max_value * 255) for o in output_raw]
    # create a slightly fancy colour map that shows colour changes with
    # increased contrast (thanks to John Montgomery)
    output_rgb = ((o + (256 * o) + (256 ** 2) * o) * 16 for o in output_raw_limited)  # fancier
    output_rgb = array.array('I', output_rgb)  # array of unsigned ints (size is platform specific)
    # display with PIL/pillow
    im = Image.new("RGB", (width, height))
    # EXPLAIN RGBX L 0 -1
    im.frombytes(output_rgb.tobytes(), "raw", "RGBX", 0, -1)
    im.show()

def show_greyscale(output_raw, width, height, max_iterations):
    """Convert list to array, show using PIL"""
    # convert our output to PIL-compatible input
    # scale to [0...255]
    max_iterations = float(max(output_raw))
    print(max_iterations)
    scale_factor = float(max_iterations)
    scaled = [int(o / scale_factor * 255) for o in output_raw]
    output = array.array('B', scaled)  # array of unsigned ints
    # display with PIL
    im = Image.new("L", (width, width))
    # EXPLAIN RAW L 0 -1
    im.frombytes(output.tobytes(), "raw", "L", 0, -1)
    im.show()

def z_points(x1, x2, y1, y2, desired_width):
    x_step = (x2 - x1) / desired_width
    y_step = (y1 - y2) / desired_width
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    
    #print("Length of x:", len(x))
    # set width and height to the generated pixel counts, rather than the
    # pre-rounding desired width and height
    width = len(x)
    height = len(y)
    # build a list of co-ordinates and the initial condition for each cell.
    # Note that our initial condition is a constant and could easily be removed,
    # we use it to simulate a real-world scenario with several inputs to our function
    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))
    return zs, cs, width, height

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        exec_time = t2 - t1
        print(f"@timefn: {fn.__name__} took {exec_time:.3f} seconds")
        return result
    return measure_time

@timefn
def calculate_z_serial_purepython(maxiter, zs, cs):
    """Calculate output list using Julia update rule"""
    output = [0] * len(zs) # list of zeros
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n
    return output

def calc_pure_python(zs, cs, width, height, draw_output, desired_width, max_iterations):
    """Create a list of complex co-ordinates (zs) and complex parameters (cs), build Julia set and display"""
    
    #start_time = time.time()
    output = calculate_z_serial_purepython(max_iterations, zs, cs)
    #end_time = time.time()
    #secs = end_time - start_time
    #print(calculate_z_serial_purepython.__name__ + " took {:.3f} seconds".format(secs))

    assert sum(output) == 33219980  # this sum is expected for 1000^2 grid with 300 iterations

    if draw_output:
        show_false_greyscale(output, width, height, max_iterations)
        #show_greyscale(output, width, height, max_iterations)
#--------------------------------------------------------------------------------------------------
#                                             Application 
#--------------------------------------------------------------------------------------------------
# area of complex space to investigate
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
desired_width=1000
c_real, c_imag = -0.62772, -.42193

zs, cs, width, height = z_points(x1, x2, y1, y2, desired_width)
print("Total elements:", len(zs))

if __name__ == "__main__":
    # Calculate the Julia set using a pure Python solution with
    # reasonable defaults for a laptop
    # set draw_output to True to use PIL to draw an image
    calc_pure_python(zs, cs, width, height, draw_output=True, desired_width=1000, max_iterations=300)

