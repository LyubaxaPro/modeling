import matplotlib.pyplot as plt
from math import exp, factorial
import numpy
import sys

def uniform_density(a, b, x):
    if x >= a and x <= b:
        return 1 / (b - a)
    return 0

def poisson_density(k, lmbd):
    return exp(-lmbd) * pow(lmbd, k) / factorial(k)

def uniform_distribution(a, b, x):
    if x < a:
        return 0
    elif x > b:
        return 1
    else:
        return (x - a) / (b - a)

def poisson_distribution(k, lmbd):
    sum = 0
    for i in range(k + 1):
        sum = sum + (pow(lmbd, i)) / factorial(i)
    sum = sum * exp(-lmbd)
    return sum

def poisson(k_start, k_stop, lmbd):
    distribution_x = [i for i in range(k_start, k_stop + 1)]
    distribution_y = [poisson_distribution(x, lmbd) for x in distribution_x]
    prepare_show_poisson(distribution_x, distribution_y, "График функции распределения Пуассона", "x", "F(x)", lmbd)
    plt.show()

    density_x = [i for i in range(k_start, k_stop + 1)]
    density_y = [poisson_density(x, lmbd) for x in density_x]
    prepare_show_poisson(density_x, density_y, "График функции вероятности Пуассона", "x", "P(x)", lmbd)
    plt.show()

def uniform(start, stop, a, b):
    distribution_x = [i for i in range(start, stop + 1)]
    distribution_y = [uniform_distribution(a, b, x) for x in distribution_x]
    prepare_show_uniform(distribution_x, distribution_y, "График функции равномерного распределения", "x", "F(x)", a, b)
    plt.show()

    density_x = numpy.linspace(start, stop + 1, num=500, endpoint=True, retstep=False, dtype=None, axis=0)
    density_y = [uniform_density(a, b, x) for x in density_x]
    prepare_show_uniform(density_x, density_y, "График функции плотности равномерного распределения", "x", "f(x)", a, b)
    plt.show()

def prepare_show_poisson(x_value, y_value, title, x_label, y_label, lmbd):
    plt.plot(x_value, y_value)
    plt.grid(True)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)

    label = "λ="
    label += str(lmbd)
    label_lmbd = label

    plt.text(x_value[-2], min(y_value), label_lmbd, fontsize=10)

def prepare_show_uniform(x_value, y_value, title, x_label, y_label, a, b):
    plt.plot(x_value, y_value)
    plt.grid(True)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)

    label = "a="+str(a)+" b="+str(b)
    label_lmbd = label

    plt.text(x_value[-2], min(y_value), label_lmbd, fontsize=10)

if __name__ == '__main__':
    startU, stopU = map(int, input("Введите(через пробел) границы интервала для равномерного распределения: ").split())

    if startU >= stopU:
        print("Левая граница должна быть меньше правой")
        sys.exit(0)

    a, b = map(int, input("Введите(через пробел) значения параметров a и b для равномерного распределения: ").split())

    if a >= b:
        print("Параметр a должен быть меньше параметра b")
        sys.exit(0)
    uniform(startU, stopU, a, b)

    start, stop, lmbd = map(int, input("Введите(через пробел) границы интервала и λ для распределения Пуассона: ").split())
    if start < 0 or stop < 0:
        print("Границы интервала не могут быть отрицательными")
        sys.exit(0)
    elif start >= stop:
        print("Левая граница должна быть меньше правой")
        sys.exit(0)
    elif lmbd < 0:
        print("λ должна быть больше 0")
        sys.exit(0)
    else:
        poisson(start, stop, lmbd)
