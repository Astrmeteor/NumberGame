import random
from itertools import permutations
import numpy as np

class NumberGuessGame:
    def __init__(self, digits, max_attempts):
        self.digits = digits
        self.max_attempts = max_attempts
        self.target = self.generate_target(digits)
        self.attempts = 0
        self.possible_answers = self.generate_possible_answers(digits)

    @staticmethod
    def generate_target(digits):
        return ''.join(random.sample('0123456789', digits))

    @staticmethod
    def generate_possible_answers(digits):
        return [''.join(p) for p in permutations('0123456789', digits)]

    def guess(self, number):
        self.attempts += 1

        if number == self.target:
            return 'Correct!'

        hits = sum(t == g for t, g in zip(self.target, number))
        blows = sum(t in number for t in self.target) - hits

        # update possible answers
        self.possible_answers = [
            answer for answer in self.possible_answers
            if sum(t == g for t, g in zip(answer, number)) == hits
               and (sum(t in number for t in answer) - hits == blows)
        ]

        # generate digit probabilities
        digit_frequencies = [{str(i): 0 for i in range(10)} for _ in range(self.digits)]
        for answer in self.possible_answers:
            for i, digit in enumerate(answer):
                digit_frequencies[i][digit] += 1

        return f'{hits} Hit, {blows} Blow', digit_frequencies


def print_matrix(matrix):
    # 输出标题行
    headers = ["Digit 1", "Digit 2", "Digit 3", "Digit 4"]
    title = 'Dig: ' + ' '.join(headers)
    print(title)

    # 获取每列的最大宽度
    col_widths = [len(h) for h in headers]
    for row in matrix:
        for i, value in enumerate(row):
            col_widths[i] = max(col_widths[i], len(f"{value:.2f}"))

    # 输出每行数据，行号+数据
    for i, row in enumerate(matrix):
        row_str = [f"{value:>{col_widths[j]}.2f}" for j, value in enumerate(row)]
        print(f"{i}: {' '.join(row_str)}")

    ref_number = ""
    for col_idx in range(len(matrix[0])):
        max_value = matrix[0][col_idx]
        max_row = 0
        for row_idx in range(1, len(matrix)):
            if matrix[row_idx][col_idx] > max_value:
                max_row = row_idx
                continue
        ref_number += str(max_row)
    print(f"Reference Number for Next round: {ref_number}")

def play_game():
    maxguess = int(input('Input the maximum round for game:'))
    print(f"Guess chance is: {maxguess}")
    game = NumberGuessGame(digits=4, max_attempts=maxguess)
    print(f"Random Number is: {game.target}")
    F = np.zeros((10, 4))
    while True:
        number = input('Enter your guess: ')
        result, frequencies = game.guess(number)
        print(result)
        print("Next round number probabilities:")
        for i, frequency in enumerate(frequencies):
            total = sum(frequency.values())
            for digit, freq in frequency.items():
                F[int(digit)][i] = freq / total if total > 0 else 0

        print_matrix(F)
        if result == 'Correct!':
            break

        if game.attempts >= game.max_attempts:
            return print("Sorry, you've reached the maximum attempts.")


if __name__ == "__main__":
    play_game()
