import logging
import timeit

# Setup logger for the runner
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("MAIN")

"""
1 -----
Difference between an abstract class an record class 
(mean't regular).
2 -----
I was asked by both the middle engineers and the senior 
engineer which is the last instruction of a non-void method that contains a "try-catch-finally" 
statement: the value returned, or the "finally" statement. The middle engineers states the 
finally, which was what I answered with. The senior engineer stated that was wrong, and that 
the return value happens after the finally.
3 -----
If a user gives a username and password and authenticates themselves through a web app, 
what do you do when the database returns two rows containing the same username but different passwords?  
4 -----
Given a username and password with a relational database table containing login information, write out the method and statement to verify authentication.  
5 -----
What is multithreading? What are the pro&#039;s and con&#039;s?  
6 -----
Difference between an abstract class and regular class?  
7 -----
Develop order book  
Answer Question
8 -----
Resume based questions
9 -----
white board coding question and typical java based questions on Multi threading, 
10 -----
collections, 
11 -----
Garbage collection and Spring  
12 -----
Standard interview process where questions on design patterns, 
integration patterns are asked along with few questions 
related with Java. 
13 -----
There were a few behavior questions and big picture questions and few 
basic questions on the business side - 
14 -----
what's a put option, what's a call option, what's a future and strategy.
15 -----
Name few of the design patterns that you have used in your projects  
16 -----
rotate the string
17 -----
flatten the nested list, 
18 -----
find the two numbers that sum to a given number  
19 -----
how to get individual letter from number formatted input. eg. given 123 , get 1, 2… 
20 -----
What is another way you could have solved the coding challenge?  


CHAT:
-----
- Enthusiasm
- dynamic, think on the spot
- whiteboard

Why flask and not django?

How would you set this up in django? Describe a django setup

what happens if we have a much larger file?

Threading in this case?

How do we handle the polling (beat) with larger file? 

What if it misses a tick?

What if no connection?

Test the tasks

Write down the counts with sql

timestamps: 28963734 - 28800011 11/30/1970 @ 8:00am - 12/02/1970 @ 5:28am (UTC)

dev server vs prod server? which prod server?
"""

import sys


def cache_fib(func):
    cache = {}

    def wrapped(input):
        if input in cache:
            output = cache[input]
        else:
            output = func(input)
            cache[input] = output

        return output

    return wrapped


@cache_fib
def run_fibo_recursive(n):
    if n < 2:
        return n
    return run_fibo_recursive(n - 1) + run_fibo_recursive(n - 2)


def run_fibo_iterative(n):

    if n < 2:
        return n

    buffer = [0, 1]
    for i in range(n):
        y = buffer[0] + buffer[1]
        buffer[1] = buffer[0]
        buffer[0] = y
        logger.debug(f"BUFFER: {buffer}")

    return y


def run_fibo_generator(n):
    a, b = 0, 1
    for i in range(n):
        yield b
        a, b = b, a + b


if __name__ == "__main__":
    n = 100
    sys.setrecursionlimit(10 ** 6)
    result_recursive = run_fibo_recursive(n)
    result_iterative = run_fibo_iterative(n)
    result_generator = run_fibo_generator(n)
    logger.debug(f"{n}th recursice fibonacci result is: {result_recursive}")
    logger.debug(f"{n}th iterative fibonacci result is: {result_iterative}")

    assert result_recursive == result_iterative
