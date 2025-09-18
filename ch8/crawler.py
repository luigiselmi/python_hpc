# This script implements a single-threaded http client. It is used to send requests to an 
# http server listening on port 8080 of the local host. Each request will send two keys: 
# name and delay. the first key is a string and the second key is a number that will tell 
# the server how long it should keep the synchronous connection before returning the control 
# to the client. The client will wait for the connection to be closed before sending a new 
# request.
import os
import threading
import random
import string
import requests

def threads_info():
    total_threads = threading.active_count()
    thread_name = threading.current_thread().name
    print(f'Python process running with process id: {os.getpid()}')
    print(f'Python is currently running {total_threads} thread(s)')
    print(f'The current thread is {thread_name}')

def generate_urls(base_url, num_urls):
    '''
    We add random characters to the end of the URL to break any caching
    mechanisms in the requests library or the server
    '''
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))

def run_experiment(base_url, num_iter=1000):
    response_size = 0
    for url in generate_urls(base_url, num_iter):
        response = requests.get(url)
        response_size += len(response.text)
    return response_size


if __name__ == "__main__":
    import time
    threads_info()
    delay = 100
    num_iter = 100
    base_url = f'http://127.0.0.1:8080/add?name=serial&delay={delay}&'
    print(f'Sending: {num_iter} request to http://127.0.0.1:8080 with delay {delay} ms.')
    start = time.time()
    result = run_experiment(base_url, num_iter)
    end = time.time()
    exec_time = end - start
    print('Result: {:d}, Time: {:.1f} sec.'.format(result, exec_time))