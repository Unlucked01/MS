import math

import numpy as np


def main():
    baseMatrix = np.zeros((6, 6))
    lambda0 = 1
    lambda_vals = [lambda0]
    Vi = np.array([3.0, 3.0, 3.0, 3.0, 3.0])
    K = np.array([1.0, 3.0, 3.0, 1.0, 2.0])
    m = np.ones(5)

    N1, N2, N3 = 7.0, 4.0, 9.0
    N4 = N1 + N2
    N5 = N1 + N3

    # Заполнение матрицы передач
    baseMatrix[0, 1] = 1.0
    baseMatrix[1, 5] = 1 / N1
    baseMatrix[2, 1] = 1 / N2
    baseMatrix[3, 4] = 1 / N3
    baseMatrix[4, 2] = 1 / N4
    baseMatrix[5, 4] = 1 / N5

    filled_matrix = fill_matrix(baseMatrix)

    A = solve_gauss(filled_matrix)
    print_matrix(filled_matrix)

    A = np.abs(A)  # Заменим отрицательные значения на положительные
    lambda_vals.extend(A[1:] * lambda0)

    rho = get_rho(lambda_vals, Vi, K)
    print("\nЗагрузка каждой СМО (Pi):")
    print_array(rho, "rho", 1)

    print("\nСреднее число занятых каналов каждой СМО (Bj):")
    b_j = lambda_vals[1:] * Vi
    print_array(b_j, "b", 1)

    print("\nВероятности состояния сети (Poj):")
    P0 = get_p0(b_j, m, K)
    print_array(P0, "P0", 1)

    print("\nСредняя длина очереди заявок для каждой СМО:")
    l = get_l(b_j, K, P0)
    print_array(l, "l", 1)

    print("\nСреднее число заявок в каждой СМО:")
    m_i = l + b_j
    print_array(m_i, "m", 1)

    print("\nСреднее время ожидания заявки в очереди системы Sj:")
    w = l / lambda_vals[1:]
    print_array(w, "w", 1)

    print("\nСреднее время пребывания заявки в системе Sj:")
    t = w + Vi
    print_array(t, "T", 1)

    print("\nДля всей сети в целом:")
    all_vals = {
        "L": np.sum(l),
        "N": np.sum(m_i),
        "W": np.sum(A[1:] * w),
        "T": np.sum(A[1:] * t)
    }
    for k, v in all_vals.items():
        print(f"{k} = {v}")


def print_matrix(matrix):
    print(np.array2string(matrix, formatter={'float_kind': lambda x: "%.6f" % x}))


def print_array(array, name, incI):
    for i, v in enumerate(array):
        print(f"{name}[{i + incI}] = {v}")


def fill_matrix(matrix):
    temp = matrix.copy()
    for row in temp:
        non_zero_sum = np.sum(row[row != 0])
        zero_count = len(row) - np.count_nonzero(row)
        if zero_count > 0:
            remaining_sum = 1 - non_zero_sum
            if remaining_sum == 0:
                continue
            random_values = generate_random_values(zero_count, remaining_sum)
            row[row == 0] = random_values
    return temp


def generate_random_values(count, remaining_sum):
    values = np.random.rand(count)
    values /= np.sum(values)
    values *= remaining_sum
    return values


def solve_gauss(matrix):
    n = matrix.shape[0]
    A = np.vstack([matrix.T, np.ones(n)])
    B = np.zeros(n + 1)
    B[-1] = 1  # Условие нормировки
    X = np.linalg.lstsq(A, B, rcond=None)[0]
    return X


def get_rho(lambda_vals, v, k):
    rho = []
    for i in range(1, len(lambda_vals)):
        rho_i = (lambda_vals[i] * v[i - 1]) / k[i - 1]
        while rho_i > 1:
            v[i - 1] /= 2
            rho_i = (lambda_vals[i] * v[i - 1]) / k[i - 1]
        rho.append(rho_i)
    return np.array(rho)


def factorial(n):
    return math.factorial(int(n))


def get_p0(b, m, k):
    result = []
    for i in range(len(b)):
        sumB_divM = 0.0
        if k[i] - 1 == 0.0:
            sumB_divM += np.power(b[i], m[i]) / factorial(m[i])
        else:
            for j in range(int(k[i])):
                sumB_divM += np.power(b[j], m[j]) / factorial(m[j])
        union_sum = np.power(sumB_divM + (np.power(b[i], k[i]) / (factorial(k[i]) * (1 - (b[i] / k[i])))), -1)
        result.append(union_sum)
    return np.array(result)


def get_l(b, k, p0):
    result = []
    for i in range(len(b)):
        l = ((np.power(b[i], 1 + k[i])) / (factorial(k[i]) * k[i] * np.power((1 - (b[i] / k[i])), 2))) * p0[i]
        result.append(l)
    return np.array(result)


if __name__ == "__main__":
    main()
