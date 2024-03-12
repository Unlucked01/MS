from matplotlib import pyplot as plt
import numpy as np
import math


c = 8000
u = 20
T = 11
h_0 = 9900
g = 9.81
x1 = 0
x2 = 0
x3 = 1100

prev_step = []
prev_lost = []


def system(vector):
    F = np.zeros(3)
    r = 0.1 * math.e ** -vector[1] / h_0
    F[0] = vector[1]  # x1
    F[1] = (c * u) / vector[2] - g - (r * vector[1] ** 2) / vector[2]  # (cu)/x3 - g - (rx2^2)/x3
    F[2] = -u  # -u
    return F


def Euler(vector, step_size, calculation_end):
    step_count = int(calculation_end / step_size) + 1
    result = [vector]
    for i in range(1, step_count):
        result.append(result[-1] + step_size * system(result[-1]))
    return result


def fixed_step():
    step_size = prev_step[-1]

    R1 = Euler(np.array([x1, x2, x3]), step_size, T)
    R2 = Euler(np.array([x1, x2, x3]), step_size / 2, T)
    steps = np.arange(0, T, step_size)

    res_x1 = [R1[i][0] for i in range(0, len(steps))]
    res_x2 = [R1[i][1] for i in range(0, len(steps))]
    res_x3 = [R1[i][2] for i in range(0, len(steps))]

    plt.plot(steps, res_x1, label='x1')
    plt.plot(steps, res_x2, label='x2')
    plt.plot(steps, res_x3, label='x3')

    plt.xlabel('Интервал')
    plt.ylabel('Значения')
    plt.legend()
    plt.show()

    print(f'Погрешность переменной Х1 при шаге {round(step_size, 5)} составляет {round(abs((R2[-1][0] - R1[-1][0]) / R2[-1][0]) * 100, 5)}%')
    print(f'Погрешность переменной X2 при шаге {round(step_size, 5)} составляет {round(abs((R2[-1][1] - R1[-1][1]) / R2[-1][1]) * 100, 5)}%')
    print(f'Погрешность переменной X3 при шаге {round(step_size, 5)} составляет {round(abs((R2[-1][2] - R1[-1][2]) / R2[-1][2]) * 100, 5)}%')


def dynamic_step():
    curr_step_size = 1
    first_step_size = curr_step_size
    while curr_step_size > 0:
        R1 = Euler(np.array([x1, x2, x3]), curr_step_size, T)
        R2 = Euler(np.array([x1, x2, x3]), curr_step_size / 2, T)
        sigma = abs((R2[-1][0] - R1[-1][0]) / R2[-1][0]) * 100
        # print(f'Размер шага {round(curr_step_size, 6)} потери {round(sigma, 3)}%')
        prev_step.append(curr_step_size)
        prev_lost.append(sigma)
        if sigma < 1:
            break
        curr_step_size -= 0.01

    fig, ax = plt.subplots()
    ax.plot(prev_step, prev_lost)
    plt.xlabel('Размер шага')
    plt.ylabel('Погрешность, %')
    ax.set_xlim(first_step_size, curr_step_size)
    plt.show()
    print(f"Итоговый размер шага: {round(prev_step[-1], 3)}")


if __name__ == '__main__':
    dynamic_step()
    fixed_step()


