import prompt


def welcome_user():
    print('May I have your name? ', end='')
    name = prompt.string('May I have your name? ')
    print(f'Hello, {name}!')
