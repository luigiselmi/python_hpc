Python High performance Computing
=================================
A collection of code examples about parallel and high performance computing with Python. The noteboks in this repository are based on the books:

* [Gorelick, Ozsvald - High Performance Python, 2nd Ed.](https://www.oreilly.com/library/view/high-performance-python/9781492055013/).

## 1. Performant Python
A computing unit is made of a CPU connected to a RAM memory unit and a HD for data storage. A CPU comes with its own very fast memory units, or caches, named L1, L2. A CPU is characterized by
 
* Number of instructions per cycle (IPC)
* Number of cycles per second (or clock speed)

A CPU can perform vectorized computation with the Single Instruction Multiple Data (SIMD) architecture.
Different techniques have been developed to improve a CPU performance:

* Multithreading, that is, using one CPU by more than one process
* Multicore architecture, that is putting more cores on one CPU for parallel processing. Specific software must be developed to use the cores available. The slowest process in a parallel computation defines the speed of the computation.

Python cannot handle parallel instructions. This issue is known as Global Interpreter Lock (GIL). Only one instruction is executed at any one time even if more cores are available. Some packages like NumPy do not have this limitation.

The characteristics of memory units, cache, RAM, SSD, hard disks, are read/write speeds and latency.      

The parts of a computer, CPU, RAM and memory units, communicate via a bus. They have different speed and number of lines, e.g. 8 or a multiple to send one or more bytes of data from one component to another. The characteristics of a bus are its width (number of lines) and transfers per second (frequency).

Other issues of Python against high performance are that it is an interpreted language, so the code cannot be optimized at compilation time, and that it uses dynamic types not static ones so the compiler cannot check for errors nor optimize the memory usage. Many of these issues can be solved by using additional packages such as NumPy that provide API interfaces between the Python code and C/C++ or Fortran compiled code.
