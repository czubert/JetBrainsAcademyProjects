# Write your code here
import random

# List of messages
msgs = ["You survived!", "You lost!"]
# List of words to guess
words = ['python', 'java', 'swift', 'javascript']
# Randomly choosing a word to guess in the game
word = random.choice(words)
end = False
score = {'win': 0, 'lost': 0}


def play():
    text = 'attempts'
    user_inputs = set()
    # Number of attempts a user have
    attempts = 8
    # Guessing the word
    hidden_word = word
    for el in hidden_word:
        hidden_word = hidden_word.replace(el, '-')

    while attempts > 0 and '-' in set(hidden_word):
        if attempts == 1:
            text = 'attempt'
        print(hidden_word)  # printing chosen word with characters changed to '-'
        print('Input a letter: ')
        guess = input()

        if len(guess) != 1:
            print("Please, input a single letter.")
            continue

        if not guess.isalpha() or not guess.islower():
            print("Please, enter a lowercase letter from the English alphabet.")
            continue

        if guess in user_inputs:
            print(guess)
            print(f'user inputs {user_inputs}')
            print(f"You've already guessed this letter.")
            continue
        elif guess in set(word):
            for i in range(len(word)):
                if guess == word[i]:
                    hidden_word = list(hidden_word)
                    hidden_word[i] = guess
                    hidden_word = ''.join(hidden_word)
        else:
            attempts -= 1
            print(f"That letter doesn't appear in the word. # {attempts} {text}")

        user_inputs.add(guess)

    if '-' not in set(hidden_word):
        print(f'You guessed the word {hidden_word}!')
        print('You survived!')
        score["win"] += 1
    else:
        print("You lost!")
        score["lost"] += 1


# Greetings
print(f"H A N G M A N  # 8 attempts")

while not end:
    print('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:')
    decision = input()
    if decision == 'play':
        play()
    elif decision == 'results':
        print(f'You won: {score["win"]} times.')
        print(f'You lost: {score["lost"]} times.')
    elif decision == 'exit':
        end = True
