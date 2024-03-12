# 37 вариант
# Мура с 6 входами, 4 выходами

class MooreMachine:
    def __init__(self, num_states, num_inputs, num_outputs):
        self.num_states = num_states
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.state = 0

        self.TRANS = [[1, 2, 3, 0, 1, 2],
                      [3, 0, 1, 2, 3, 0],
                      [2, 3, 0, 1, 2, 3],
                      [0, 1, 2, 3, 0, 1]]

        self.OUT = [[0, 1, 2, 0, 1, 2],
                    [2, 0, 1, 2, 0, 1],
                    [1, 2, 0, 1, 2, 0],
                    [0, 1, 2, 0, 1, 2]]

    def transition(self, input_signal):
        self.state = self.TRANS[self.state][input_signal]

    def output(self, input_signal):
        return self.OUT[self.state][input_signal]


def main():
    num_states = 4
    num_inputs = 6
    num_outputs = 3

    machine = MooreMachine(num_states, num_inputs, num_outputs)

    inputs = input("Ведите последовательность входных сигналов: ").strip().split()
    if not inputs:
        inputs = ['1', '2', '3', '2', '3', '5']
    if len(inputs) != num_inputs:
        print(f"Ошибка: введите {num_inputs} чисел, разделенных пробелом")
        return

    header = "Последовательность входных сигналов:     "
    print(" "*len(header), f"{'0':<2} {'1':<2} {'2':<2} {'3':<2} {'4':<2} {'5':<2} {'6':<2}")

    sequence_states = []
    sequence_outputs = []
    x = []

    step = 0
    x.append("--")
    sequence_states.append(f"z{machine.state}")
    sequence_outputs.append(f"y{machine.output(machine.state)}")

    for input_signal in inputs:
        if not input_signal.isdigit() or int(input_signal) < 0 or int(input_signal) > 5:
            print("Ошибка: введите числа от 0 до 5, разделенные пробелом")
            return
        input_signal = int(input_signal)

        machine.transition(input_signal)
        output_signal = machine.output(input_signal)

        sequence_states.append(f"z{machine.state + 1}")
        sequence_outputs.append(f"y{output_signal + 1}")
        x.append(f"x{input_signal + 1}")
        step += 1

    print(header, *x)
    print("Последовательность состояний автомата:   ", *sequence_states)
    print("Последовательность выходных сигналов:    ", *sequence_outputs)


if __name__ == "__main__":
    main()