""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

from numba import njit

# Exc1
def approximate_pi(n):
    # n is the number of points

    # Write your code here
    x_inside = []
    y_inside = []

    x_outside = []
    y_outside = []

    for i in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        if (pow(x,2) + pow(y,2)) <= 1:
            x_inside.append(x)
            y_inside.append(y)
        else:
            x_outside.append(x)
            y_outside.append(y)

    plt.plot(x_inside, y_inside, 'ro')
    plt.plot(x_outside, y_outside, 'bo')
    plt.show()

    print(
        (4 * len(x_inside)) 
        /
        (n)
        )

    return (4 * len(x_inside)) / (n)

# Exc2, approximation
def sphere_volume(n, d):

    total_point = []

    for i in range(n):
        one_point = [random.uniform(-1, 1) for _ in range(d)] # list comprehension
        total_point.append(one_point)

    inside_sphere = list( # filter(), lambda, map()
        filter(lambda point: sum(map(lambda x: x ** 2, point)) <= 1, 
               total_point)
               )

    volume = (2 ** d) * len(inside_sphere) / n

    # print(volume)
    return volume

#Exc2, real value
def hypersphere_exact(n, d):
    return pow(m.pi, d/2) / m.gamma(d/2 + 1)

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float:
    total_point = []
    inside_sphere = []

    # n is the number of points
    # d is the number of dimensions of the sphere

    for i in range(n):
        one_point = []

        for j in range(d):
            x = random.uniform(-1, 1)
            one_point.append(x)
        total_point.append(one_point)

        sum_square = 0

        for j in range(d):
            sum_square += pow(total_point[i][j], 2)

        if sum_square <= 1:# inside of sphere
            inside_sphere.append(total_point[i])

    return (pow(2,d) * len(inside_sphere)) / (n)

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel(n, d, np = 10):
    points_per_process = n // np # allocate divided works to each processor

    n_list = [points_per_process] * np
    d_list = [d] * np

    with future.ProcessPoolExecutor(max_workers = np) as ex:
        results = ex.map(sphere_volume, n_list, d_list)
        results = list(results)
    return mean(results)
    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    
    print("-------------------------")
    
    # Exc2
    n = 100000
    d = 2
    print(f"Appoximate volume of {d} dimentional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    print(f"Appoximate volume of {d} dimentional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")
    
    print("-------------------------")
    
    # Exc3
    n = 1000000
    d = 11

    # sequential time
    # 1st
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc3: 1st Sequential time of {d} and {n}: {stop-start}")
    # 2nd
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc3: 2nd Sequential time of {d} and {n}: {stop-start}")
    # 3rd
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc3: 3rd Sequential time of {d} and {n}: {stop-start}")

    # numba time
    print("What is numba time?")
    # 1st
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f"Exc3: 1st Numba time of {d} and {n}: {stop-start}")
    # 2nd
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f"Exc3: 2nd Numba time of {d} and {n}: {stop-start}")
    # 3rd
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f"Exc3: 3rd Numba time of {d} and {n}: {stop-start}")
    
    print("-------------------------")

    # Exc4
    n = 1000000
    d = 11

    # Sequential time
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")

    # Parallel time
    print("What is parallel time?")
    start = pc()
    sphere_volume_parallel(n, d)
    stop = pc()
    print(f"Exc4: Parallel time of {d} and {n}: {stop-start}")
    

if __name__ == '__main__':
	main()


