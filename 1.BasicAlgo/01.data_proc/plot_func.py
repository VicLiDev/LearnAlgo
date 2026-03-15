#!/opt/homebrew/anaconda3/bin/python
# 程序说明：
# 绘制函数

import sys,getopt
import numpy as np
import math
import matplotlib.pyplot as plt

def plot2D(x, y):
    fig_1 = plt.figure()  # an empty figure with no Axes
    ax_1 = fig_1.add_subplot(111)
    ax_1.plot(x, 0.4*x, marker=".", color="r", linestyle="-")  # Plot some data on the axes.
    return

def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

def plot3D(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax.scatter(x, y, z)

    return

def main():
    # plot 2D
    x = np.linspace(0, 2, 100)
    y = np.linspace(0, 2, 100)
    z = np.linspace(0, 2, 100)
    # plot2D(x, y)

    y2 = 0.8 * (np.power(2, x / 6) - 1)
    plot2D(x, y2)

    y3 = 0.5 * x - 7
    # plot2D(x, y3)

    # plot 3D
    n = 100
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0,  100)
    zs = randrange(n, 50, 100)
    plot3D(xs, ys, zs)

    plt.show()

if __name__ == '__main__':
    main()
