import random
import sys
from brain_games.cli import welcome_user

def is_even(number):
    return number % 2 == 0

def generate_question_answer():
    number = random.randint(1, 100)
    correct_answer = 'yes' if is_even(number) else 'no'
    return number, correct_answer

def main():
    print('Welcome to the Brain Games!')
    name = welcome_user()  # Используем функцию для приветствия и получения имени
    print('Answer "yes" if the number is even, otherwise answer "no".')

    correct_answers_count = 0
    while correct_answers_count < 3:
        number, correct_answer = generate_question_answer()
        print(f'Question: {number}')
        user_answer = input('Your answer: ').strip().lower()

        if user_answer == correct_answer:
            print('Correct!')
            correct_answers_count += 1
        else:
            print(f"'{user_answer}' is wrong answer ;(. Correct answer was '{correct_answer}'.")
            print(f"Let's try again, {name}!")
            return

    print(f'Congratulations, {name}!')