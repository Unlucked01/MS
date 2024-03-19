import random

# Определение констант
n = 2  # входной алфавит состоит из двух символов
m = 2  # выходной алфавит состоит из двух символов
p = 4  # количество состояний

a = [
    [[0.5, 0, 0.5], [1, 0, 0], [0.3, 0.3, 0.1]],
    [[0, 0.5, 0.5], [0, 0.3, 0.7], [0.9, 0, 0.1]]
]

b = [
    [[0.4, 0.6], [1, 0], [0, 1]],
    [[0, 1], [0.5, 0.5], [0.7, 0.3]]
]

c = [0.2, 0.2, 0.6]


# Функция для определения следующего состояния
def determine_next_state(x, z_old, r_1):
    cumulative_prob = 0

    for i in range(p):
        cumulative_prob += a[x - 1][z_old - 1][i]
        if r_1 <= cumulative_prob:
            return i + 1  # Возвращаем индекс + 1 (так как индексы начинаются с 0)


# Функция для определения выходного символа
def determine_output(x, z_old, r_2):
    cumulative_prob = 0

    for i in range(m):
        cumulative_prob += b[x - 1][z_old - 1][i]
        if r_2 <= cumulative_prob:
            return chr(ord('m') + i)  # Преобразуем индекс в символ 'm' или 'n'


# Инициализация переменных
random.seed(42)  # Установка начального состояния генератора случайных чисел для воспроизводимости
x_sequence = [random.randint(1, n) for _ in range(5)]  # Входная последовательность случайных чисел
z_old = random.randint(1, p)  # Начальное состояние

# Вывод заголовка таблицы
print(f"x | z_old |  r_1 | z_new |  r_2 | y")

# Моделирование работы автомата и сбор статистики
state_count = [0] * p  # Инициализация счетчика состояний
total_transitions = 0

for x in x_sequence:
    r_1 = random.random()  # Генерация случайного числа r_1
    r_2 = random.random()  # Генерация случайного числа r_2

    z_new = determine_next_state(x, z_old, r_1)
    y = determine_output(x, z_old, r_2)

    # Увеличиваем счетчик для нового состояния
    state_count[z_new - 1] += 1

    # Выводим информацию о текущем такте
    print(f"{x} | {chr(ord('a') + z_old - 1):>5} | {r_1:.2f} | {chr(ord('a') + z_new - 1):>5} | {r_2:.2f} | {y}")

    # Обновляем текущее состояние
    z_old = z_new
    total_transitions += 1

# Вывод статистики
print("\nСтатистика:")
for i in range(p):
    print(
        f"Состояние {chr(ord('a') + i)}: абсолютная частота - {state_count[i]}, процент - {state_count[i] / total_transitions * 100}%")
