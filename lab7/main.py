import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy import integrate


# Функция плотности распределения
def pdf(z):
    return np.sqrt(2) * np.cos(z)


# Функция для вычисления математического ожидания
def theoretical_mean():
    mean_integral, _ = integrate.quad(lambda z: z * pdf(z), 0, np.pi / 4)
    return mean_integral


# Функция для вычисления дисперсии
def theoretical_variance(mean):
    variance_integral, _ = integrate.quad(lambda z: (z**2) * pdf(z), 0, np.pi / 4)
    return variance_integral - mean**2


# Функция для генерации выборки с помощью метода обратных функций
# f(z) = sqrt(2) * cos(z), 0 <= z <= pi/4
# F(z) = sqrt(2) * sin(z), 0 <= z <= pi/4
# F^(-1)(u) = arcsin(R / sqrt(2)), R(0, 1)
def inverse_transform_sampling(n):
    R = np.random.uniform(0, 1, n)
    return np.arcsin(R / np.sqrt(2))


# Функция для вычисления среднего значения и дисперсии выборки
def calculate_mean_variance(samples):
    return np.mean(samples), np.var(samples)


# Теоретическая функция распределения (CDF)
def theoretical_cdf(x):
    return np.sqrt(2) * np.sin(x)


# Функция для вычисления эмпирической функции распределения (ECDF)
def empirical_cdf(samples, x_values):
    return np.array([np.sum(samples <= x) / len(samples) for x in x_values])


# Функция для построения графиков выборки
def plot_cdf(samples):
    x = np.linspace(0, np.pi / 4, 1000)

    ecdf = empirical_cdf(samples, x)
    tcdf = theoretical_cdf(x)

    plt.step(x, ecdf, where='post', label='Эмпирическая функция распределения', color='b')
    plt.plot(x, tcdf, 'r', label='Теоретическая функция распределения')

    plt.title(f"Размер выборки: {len(samples)}")
    plt.xlabel('Значение')
    plt.ylabel('Функция распределения')
    plt.legend()
    plt.show()

# Вычисление теоретических значений
theoretical_mean_value = theoretical_mean()
theoretical_variance_value = theoretical_variance(theoretical_mean_value)
print(f"Теоретическое МО: {theoretical_mean_value:.4f}")
print(f"Теоретическая дисперсия: {theoretical_variance_value:.4f}")

# Размеры выборок
sample_sizes = [50, 100, 1000, 10000, 100000]

# Генерация выборок, вычисление среднего значения, дисперсии и статистики критерия Колмогорова
for size in sample_sizes:
    samples = inverse_transform_sampling(size)
    mean, variance = calculate_mean_variance(samples)
    ks_statistic, p_value = stats.kstest(samples, theoretical_cdf)

    print(f"Размер выбоки: {size},"
          f" МО: {mean:.4f},"
          f" СКО: {variance:.4f},"
          f" КС: {ks_statistic:.10f},"
          f" p: {p_value:.10f}.")

    # plot_cdf(samples)
