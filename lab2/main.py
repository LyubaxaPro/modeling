import random
import numpy
from prettytable import PrettyTable
import matplotlib.pyplot as plt
TIME_DELTA = 1e-3
EPS = 1e-5

def dp(matrix, probabilities):
    res = []
    n = len(matrix)
    for i in range(n):
        summ = 0
        for j in range(n):
            if i == j:
                sum_i = 0
                for t in range(n):
                    sum_i += matrix[i][t]

                summ += probabilities[j] * (-1 * sum_i + matrix[i][i])
            else:
                summ += probabilities[j] * matrix[j][i]
        res.append(TIME_DELTA * summ)
    return res

def get_stabilization_times(matrix, start_probabilities):
    n = len(matrix)
    current_time = 0
    current_probabilities = start_probabilities.copy()
    stabilization_times = [0 for i in range(n)]
    stabilization_p = [0 for i in range(n)]
    prev_probabilities = []
    for i in range(n):
        prev_probabilities.append([])
    x = []
    counter = 0
    prev_dp = dp(matrix, current_probabilities)
    while not all(stabilization_times):
        while counter < 100:
            curr_dp = dp(matrix, current_probabilities)
            for i in range(n):
                prev_probabilities[i].append(current_probabilities[i])
                current_probabilities[i] += curr_dp[i]
            counter += 1
            x.append(current_time)
            current_time += TIME_DELTA
        for i in range(n):
            if not stabilization_times[i] and abs(prev_dp[i] - curr_dp[i]) < EPS and abs(curr_dp[i]) < EPS:
                stabilization_times[i] = current_time - TIME_DELTA * 30
                stabilization_p[i] = current_probabilities[i]
        counter = 0
        prev_dp = curr_dp

    counter = 0
    while counter < 100:
        curr_dp = dp(matrix, current_probabilities)
        for i in range(n):
            prev_probabilities[i].append(current_probabilities[i])
            current_probabilities[i] += curr_dp[i]
        counter += 1
        x.append(current_time)
        current_time += TIME_DELTA
    fig, ax = plt.subplots()

    for i in range(n):
        ax.plot(x, prev_probabilities[i], label = 'S' + str(i))
        ax.scatter(stabilization_times[i], stabilization_p[i], color='orange', s=40, marker='o')
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('Probabilities')
    plt.show()
    return stabilization_times


def solve(matrix):
    matrix = numpy.array(matrix)
    n = len(matrix)
    coeff_matrix = numpy.zeros((n, n))

    for state in range(n - 1):
        for col in range(n):
            coeff_matrix[state, state] -= matrix[state, col]
        for row in range(n):
            coeff_matrix[state, row] += matrix[row, state]

    for state in range(n):
        coeff_matrix[n - 1, state] = 1

    res = [0 for i in range(n)]
    res[n - 1] = 1
    augmentation_matrix = numpy.array(res)

    return numpy.linalg.solve(coeff_matrix, augmentation_matrix)

if __name__ == '__main__':
    n = int(input("Введите количество состояний системы: "))
    if n <= 0 or n > 10:
        print("Некорректное количество состояний")
        exit(1)
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(n):
            matrix[i].append(0.0)

    flag = input("Если Вы хотите заполнить матрицу состояний самостоятельно введите 1, "
                 "для автоматического заполнения матрицы введите 0: ")
    if flag == "0":
        for i in range(n):
            for j in range(n):
                if i != j:
                    matrix[i][j] = round(random.random(), 4)

    elif flag == "1":
        print("Введите интенсивность перехода из одного сотояния в другое указав три значения: {состояние из которого совершается переход} {состояние в которое совершается переход} {значение интенсивности}")
        print("Нумерация состояний начинается с 0")
        print("Введите построчно значения по образцу для всех интенсивностей которые Вы хотите поместить в матрицу")
        print("Для завершения ввода введите слово STOP")

        while(1):
            s = input()
            if s == "STOP":
                break
            i, j, lmbda = map(float, s.split())
            if i == j:
                print("Переход в одно и то же состояние невозможен")
            elif (i < 0 or i >= n or j < 0 or j >= n):
                print("Несуществует таких состояний")
            else:
                matrix[int(i)][int(j)] = lmbda
    else:
        print("Некорректный ввод")
        exit(1)

    print("\nМатрица связей и интенсивностей системы")
    table = PrettyTable()
    names = [""]
    for i in range(n):
        names.append(str(i))
    table.field_names = names

    for i in range(n):
        tmp = [i]
        tmp.extend(item for item in matrix[i])
        table.add_row(tmp)
    print(table)

    # начальные значения для dp
    start_probabilities = [0] * n
    start_probabilities[0] = 1

    # вычисление предельных вероятностей
    probability = solve(matrix)
    print("\nПредельные вероятности")

    table_probability = PrettyTable()
    names = []
    for i in range(n):
        names.append("p" + str(i))
    table_probability.field_names = names

    tmp = []
    tmp.extend(round(item, 6) for item in probability)
    table_probability.add_row(tmp)
    print(table_probability)

    # поиск времени стабилизации
    stabilization_time = get_stabilization_times(matrix, start_probabilities)

    print("\nВремя стабилизации")

    table_stabilization = PrettyTable()
    names = []
    for i in range(n):
        names.append("t" + str(i))
    table_stabilization.field_names = names

    tmp = []
    tmp.extend(round(item, 6) for item in stabilization_time)
    table_stabilization.add_row(tmp)
    print(table_stabilization)