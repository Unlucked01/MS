import numpy as np
import math
import pandas as pd

# Исходные данные
c = 8000
u = 20
T = 11
h_0 = 9900
g = 9.81
x1 = 0
x2 = 0
x3 = 1100

m = 70  # Число параллельных испытаний


def system(vector, c, u, h_0):
    F = np.zeros(3)
    r = 0.1 * math.exp(-vector[1] / h_0)
    F[0] = vector[1]
    F[1] = (c * u) / vector[2] - g - (r * vector[1] ** 2) / vector[2]
    F[2] = -u
    return F


def Euler(vector, step_size, calculation_end, c, u, h_0):
    step_count = int(calculation_end / step_size) + 1
    result = [vector]
    for i in range(1, step_count):
        result.append(result[-1] + step_size * system(result[-1], c, u, h_0))
    return result


def run_experiments():
    param_ranges = {
        'c': [c * 0.8, c * 1.2],
        'u': [u * 0.8, u * 1.2],
        'T': [T * 0.8, T * 1.2],
        'h_0': [h_0 * 0.8, h_0 * 1.2],
    }

    step_size = 0.1
    results = []

    for c_val in param_ranges['c']:
        for u_val in param_ranges['u']:
            for T_val in param_ranges['T']:
                for h_0_val in param_ranges['h_0']:
                    areas = []
                    for _ in range(m):  # 70 параллельных испытаний
                        R = Euler(np.array([x1, x2, x3]), step_size, T_val, c_val, u_val, h_0_val)
                        res_x1 = [R[i][2] for i in range(len(R))]
                        area = np.trapz(res_x1, dx=step_size)  # Площадь под кривой x3
                        areas.append(area)
                    avg_area = np.mean(areas)
                    results.append([c_val, u_val, T_val, h_0_val, avg_area])

    return results


if __name__ == '__main__':
    results = run_experiments()

    # Создание DataFrame
    df = pd.DataFrame(results, columns=['c', 'u', 'T', 'h_0', 'area'])
    # Рандомизация строк DataFrame
    df = df.sample(frac=1).reset_index(drop=True)
    # Запись результатов в Excel-файл
    df.to_excel('experiment_results1.xlsx', index=False)

    print("Результаты эксперимента записаны в файл 'experiment_results.xlsx'.")
