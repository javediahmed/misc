import sys, time
from functools import lru_cache, wraps
#sys.setrecursionlimit(2000)

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        program_time = time.perf_counter() - start
        print(f'Program time: {program_time}')
        return result
    return wrapper

def my_decorator(f): 
    def log_f_as_called(*args, **kwargs):
        print(f'{f} was called with arguments={args} and kwargs={kwargs}')
        value = f(*args, **kwargs)
        print(f'{f} return value {value}')
        return value
    return log_f_as_called

def fib(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

@timer
def fib_t(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

@my_decorator
def fib_w(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

    
@lru_cache(maxsize=512)
def fib_m(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    else:
        return fib_m(n-1) + fib_m(n-2)






