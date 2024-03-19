import random

# Определение констант
n = 2  # входной алфавит состоит из 2 символов
m = 4  # выходной алфавит состоит из 4 символов
p = 4  # количество состояний

a = [
    [[0.3, 0, 0.5, 0.2], [1, 0, 0, 0], [0.2, 0.2, 0.1, 0.5], [0, 0.5, 0.5, 0]],
    [[0, 0.5, 0.5, 0], [0, 0.3, 0.3, 0.4], [0.8, 0, 0.1, 0.1], [0.3, 0, 0.5, 0.2]]
]

b = [
    [[0.4, 0.4, 0.1, 0.1], [1, 0, 0, 0], [0, 0.8, 0.1, 0.1], [0, 0.3, 0.3, 0.4]],
    [[0, 0.3, 0.3, 0.4], [0.5, 0.5, 0, 0], [0.6, 0.3, 0, 0.1], [0.4, 0.4, 0.1, 0.1]]
]

c = [0.2, 0.2, 0.3, 0.3]


# Функция для определения следующего состояния
def determine_next_state(x, z_old, r_1):
    cumulative_prob = 0
    for i in range(p):
        cumulative_prob += a[x - 1][z_old - 1][i]
        if r_1 <= cumulative_prob:
            return i + 1


# Функция для определения выходного символа
def determine_output(x, z_old, r_2):
    cumulative_prob = 0
    for i in range(m):
        cumulative_prob += b[x - 1][z_old - 1][i]
        if r_2 <= cumulative_prob:
            return chr(ord('m') + i)


def determine_initial_state():
    rand_num = random.random()
    cumulative_prob = 0
    for i in range(p):
        cumulative_prob += c[i]
        if rand_num <= cumulative_prob:
            return i + 1


# Инициализация переменных
# random.seed(42)
x_sequence = [random.randint(1, n) for _ in range(5)]

print(f"x | z_old |  r_1 | z_new |  r_2 | y")

# Моделирование работы автомата и сбор статистики
state_count = [0] * p
total_transitions = 0

for x in x_sequence:
    r_1 = random.random()
    r_2 = random.random()

    z_old = determine_initial_state()

    z_new = determine_next_state(x, z_old, r_1)
    y = determine_output(x, z_old, r_2)
    state_count[z_new - 1] += 1
    print(f"{x} | {chr(ord('a') + z_old - 1):>5} | {r_1:.2f} | {chr(ord('a') + z_new - 1):>5} | {r_2:.2f} | {y}")
    z_old = z_new
    total_transitions += 1

print("\nСтатистика:")
for i in range(p):
    print(
        f"Состояние {chr(ord('a') + i)}: абсолютная частота - {state_count[i]}, процент - {state_count[i] / total_transitions * 100}%")
