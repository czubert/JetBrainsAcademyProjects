import nltk
# nltk.download('punkt')  # use it at the beginning once
import re
from nltk import WhitespaceTokenizer
from collections import Counter
import random


def read_file():
    """
    Takes the file path as an input from user.
    Reads the file.
    Creates tokens
    :return: List of tokens
    """
    file_name = input()
    # file_name = "corpus.txt"

    with open(file_name, "r", encoding="utf-8") as f:
        corp = f.read()
        tk = WhitespaceTokenizer()
        tokens = tk.tokenize(corp)

    return tokens


def get_heads(tokens):
    bigrams = []
    heads = {}

    bigrams_gen = nltk.bigrams(tokens)
    for el in bigrams_gen:
        head = el[0]
        tail = el[1]
        bigrams.append((head, tail))

    for head, tails in bigrams:
        heads.setdefault(head, []).append(tails)

    for key in heads.keys():
        heads[key] = Counter(heads[key])

    return heads


def validate_user_input(heads_tails, word):
    """
    Takes user input, and checks if it is valid. If yes returns input word if not raises error.
    :param word: str
    :param heads_tails: dict
    :return: str
    """

    if word == 'exit':
        exit()

    try:
        heads_tails[word]
    except KeyError:
        raise KeyError("The requested word is not in the model. Please input another word.")

    return word


def run_preprocess(heads_tails):
    """
    Takes tokens list and tokens len as arguments.
    Runs the script which gets the index as a user input, and outputs the token from the given index.
    :param heads_tails: List of tokens
    """
    while True:
        user_input = input()

        print(f'Head: {user_input}')

        try:
            user_input = validate_user_input(heads_tails, user_input)
        except Exception as e:
            print(e)
            continue

        pair = heads_tails[user_input]

        for key, value in pair.items():
            print(f"Tail: {key}     Count: {value}")
        print()


def getting_random_word(corpus):
    first_capitalised = False
    while not first_capitalised:
        most_common_word = random.choices(list(corpus.keys()))[0]
        if re.match(r'(^[A-Z])(\w)*([^!.\?]$)', most_common_word):
            return most_common_word


def compose_sentence(corpus, start_word):
    sentence = [start_word]
    start_word = corpus[start_word].most_common(1)[0][0]
    ending_word = False
    while len(sentence) < 5 or not ending_word:
        if re.match(r'(\w)*([!.\?]$)', start_word):
            ending_word = True
        else:
            ending_word = False

        sentence.append(start_word)

        start_word = corpus[start_word].most_common(1)[0][0]

    print(' '.join(sentence))


def main():
    """
    Runs the script.
    First it reads the file from a path given as an input, and creates a tokens list.
    Then it takes index as an input from user and outputs the token from the list at the given index.
    """
    try:
        tokens = read_file()  # getting tokens as a list, it's len, and unique tokens len
        head_tails = get_heads(tokens)
        # run_preprocess(heads)  # step 3
        # step 4:
        for _ in range(10):
            start_word = getting_random_word(head_tails)
            compose_sentence(head_tails, start_word)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
