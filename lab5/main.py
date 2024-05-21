import numpy as np
import matplotlib.pyplot as plt

lambda_matrix = np.array([
    [0.7, 0.15, 0.1, 0.05],
    [0, 0.5, 0.3, 0.2],
    [0, 0, 0.3, 0.7],
    [0, 0, 0, 1]
])


def dPdt(p):
    dpdt = np.zeros_like(p)
    dpdt[0] = -(lambda_matrix[0].sum()) * p[0]
    dpdt[1] = -(lambda_matrix[1].sum()) * p[1] + lambda_matrix[0, 1] * p[0]
    dpdt[2] = -(lambda_matrix[2].sum()) * p[2] + lambda_matrix[0, 2] * p[0] + lambda_matrix[1, 2] * p[1]
    dpdt[3] = -(lambda_matrix[3].sum()) * p[3] + lambda_matrix[0, 3] * p[0] + lambda_matrix[1, 3] * p[1] + lambda_matrix[2, 3] * p[2]
    return dpdt


T = (0, 10000)
h = 0.01
probabilities = []

p0 = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)

t = T[0]
while t < T[1]:
    dp = dPdt(p0) * h
    p0 += dp
    p0 /= p0.sum()
    probabilities.append(p0.copy())
    t += h

probabilities = np.array(probabilities)
probabilities = np.round(probabilities, 3)
print("Предельные вероятности: ", probabilities[-1])
print("Сумма предельных вероятностей: ", np.sum(probabilities[-1]))

plt.figure(figsize=(10, 6))
for i in range(4):
    plt.plot(np.linspace(T[0], T[1], len(probabilities)), probabilities[:, i], label=f'S{i+1}')
plt.title('Вероятности состояний от времени')
plt.xlabel('Время')
plt.ylabel('Вероятность')
plt.legend()
plt.grid(True)
plt.show()
