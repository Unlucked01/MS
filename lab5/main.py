import numpy as np
import matplotlib.pyplot as plt

Q1 = np.array([
    [0, 2, 1, 0],
    [0, 0, 0, 1],
    [3, 2, 0, 0],
    [0, 0, 0, 2]
])


# def system(p):
#     return np.array([
#         -np.sum(Q1[0] * p) + Q1[1][0] * p[1] + Q1[2][0] * p[2] + Q1[3][0] * p[3],
#         Q1[0][1] * p[0] - np.sum(Q1[1] * p) + Q1[2][1] * p[2] + Q1[3][1] * p[3],
#         Q1[0][2] * p[0] + Q1[1][2] * p[1] - np.sum(Q1[2] * p) + Q1[3][2] * p[3],
#         Q1[0][3] * p[0] + Q1[1][3] * p[1] + Q1[2][3] * p[2] - np.sum(Q1[3] * p)
#     ])


def kolmogorov_equations(P):
    dPdt = np.zeros_like(P)
    dPdt[0] = -Q1[0] * P + Q1[1][0] * P[1] + Q1[2][0] * P[2] + Q1[3][0] * P[3]
    dPdt[1] = -Q1[1] * P + Q1[0][1] * P[0] + Q1[2][1] * P[2] + Q1[3][1] * P[3]
    dPdt[2] = -Q1[2] * P + Q1[0][2] * P[0] + Q1[2][2] * P[2] + Q1[3][2] * P[3]
    dPdt[3] = -Q1[3] * P + Q1[0][3] * P[0] + Q1[1][3] * P[1] + Q1[2][3] * P[2]
    return dPdt


def RK4(vector, step_size, calculation_end):
    step_count = int(calculation_end / step_size) + 1
    result = [vector]
    for i in range(1, step_count):
        k1 = step_size * kolmogorov_equations(result[-1])
        k2 = step_size * kolmogorov_equations(result[-1] + 0.5 * k1)
        k3 = step_size * kolmogorov_equations(result[-1] + 0.5 * k2)
        k4 = step_size * kolmogorov_equations(result[-1] + k3)
        result.append(result[-1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    return result


def main():
    p0 = np.array([1, 0, 0, 0])
    h = 0.001  # Шаг интегрирования
    T = 10  # Время интегрирования
    p_rk4 = RK4(p0, h, T)

    t_values = np.linspace(0, T, len(p_rk4))
    plt.figure(figsize=(10, 6))
    plt.plot(t_values, np.array(p_rk4))
    plt.xlabel('Время')
    plt.ylabel('Вероятности состояний')
    plt.title('Динамика вероятностей состояний во времени')
    plt.legend(['Состояние 0', 'Состояние 1', 'Состояние 2', 'Состояние 3'])
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
