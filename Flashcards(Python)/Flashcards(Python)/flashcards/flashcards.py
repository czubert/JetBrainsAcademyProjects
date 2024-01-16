import random
from io import StringIO
import json
import logging
import sys
import argparse


class Cards:

    def __init__(self):
        self.log = StringIO()
        self.flashcards = {}

    def get_log(self, func):
        targets = logging.StreamHandler(sys.stdout), logging.StreamHandler(self.log)
        logging.basicConfig(format='%(message)s', level=logging.INFO, handlers=targets)
        logging.info(func)

    def compare_answers(self, definition, answer):
        term_list = list(self.flashcards.keys())
        def_list = [self.flashcards[term]["word_def"] for term in term_list]

        if answer != definition:
            def_pos = def_list.index(definition)  # store the index for the definition
            if answer in def_list:
                pos = def_list.index(answer)
                self.flashcards[term_list[def_pos]]["mistake"] += 1

                return f'Wrong. The right answer is "{definition}",\
                        but your definition is correct for "{term_list[pos]}".\n'
            else:
                self.flashcards[term_list[def_pos]]["mistake"] += 1

                return f'Wrong. The right answer is "{definition}".\n'

        return "Correct !\n"

    def add_cards(self):
        message = f"The card:\n"
        word_term = input(message)
        print(message, word_term, file=self.log, flush=True)
        definitions = [self.flashcards[card]["word_def"] for card in self.flashcards]
        while word_term in self.flashcards.keys():
            message = f'The card "{word_term}" already exists.\n'
            word_term = input(message)
            print(message, word_term, file=self.log, flush=True)
        else:
            message = f"The definition of the card:\n"
            word_def = input(message)
            print(message, word_def, file=self.log, flush=True)
            while word_def in definitions:
                message = f'The definition "{word_def}" already exists.\n'
                word_def = input(message)
                print(message, word_def, file=self.log, flush=True)
            else:
                self.flashcards[word_term] = {"word_def": word_def, "mistake": 0}
                return f'The pair ("{word_term}":"{word_def}") has been added.\n'

    def remove_cards(self, card):
        try:
            del self.flashcards[card]
            return "The card has been removed.\n"
        except KeyError:
            return f'Can\'t remove "{card}": there is no such card.\n'

    def read_file(self, file_name):
        try:
            with open(file_name, "r+") as file:
                cards = json.load(file)
            self.flashcards = self.flashcards | cards

            return f"{len(cards)} cards have been loaded\n"
        except FileNotFoundError:
            return "File not found.\n"

    def save_file(self, file_name):
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(self.flashcards, file)
        return f"{len(self.flashcards)} cards have been saved.\n"

    def ask(self):
        term_list = list(self.flashcards.keys())
        word = random.choice(term_list)
        message = f'Print the definition of "{word}":\n'
        user_answer = input(message)
        print(message, user_answer, file=self.log, flush=True)
        return self.compare_answers(self.flashcards[word]["word_def"], user_answer)

    def hardest_card(self):
        term_list = list(self.flashcards.keys())
        mistakes_list = [self.flashcards[card]["mistake"] for card in self.flashcards]
        positions = [i for i, x in enumerate(mistakes_list) if x == max(mistakes_list) and x > 0]
        if len(positions) == 1:
            return f"The hardest card is {term_list[positions[0]]}. \
                    You have {mistakes_list[positions[0]]} errors answering it.\n"
        elif len(positions) == 0:
            return f"There are no cards with errors.\n"
        else:
            hardest_list = [f'"{term_list[pos]}"' for pos in positions]
            return f'The hardest cards are {"{}, " * len(hardest_list)}\n'.format(*hardest_list)

    def reset_stats(self):
        for card in self.flashcards:
            self.flashcards[card]["mistake"] = 0
        return f"Card statistics have been reset.\n"

    def log_to_file(self, file_name):
        with open(file_name, "w") as file:
            file.write(self.log.getvalue())
        return f"The log has been saved.\n"

    def exit_(self):
        return f"Bye Bye!\n"

    def main(self):
        while True:
            opener = "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n"
            user_choice = input(opener)
            print(opener, user_choice, file=self.log, flush=True)
            if user_choice == "exit":
                self.get_log(self.exit_())
                break
            elif user_choice == "add":
                self.get_log(self.add_cards())
            elif user_choice == "remove":
                message = input("Which card?\n")
                print(message, file=self.log, flush=True)
                self.get_log(self.remove_cards(message))
            elif user_choice == "import":
                message = input("File name:\n")
                print(message, file=self.log, flush=True)
                self.get_log(self.read_file(message))
            elif user_choice == "export":
                message = input("File name:\n")
                print(message, file=self.log, flush=True)
                self.get_log(self.save_file(message))
            elif user_choice == "ask":
                n_times = input("How many times to ask?\n")
                print(n_times, file=self.log, flush=True)
                for _ in range(int(n_times)):
                    self.get_log(self.ask())
            elif user_choice == "log":
                message = input("File name:\n")
                print(message, file=self.log, flush=True)
                self.get_log(self.log_to_file(message))
            elif user_choice == "hardest card":
                self.get_log(self.hardest_card())
            elif user_choice == "reset stats":
                self.get_log(self.reset_stats())
            else:
                self.get_log("No such option! Try again!")

    def arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--import_from")
        parser.add_argument("--export_to")
        args = parser.parse_args()
        if args.import_from and args.export_to:
            self.get_log(self.read_file(args.import_from))
            self.main()
            self.get_log(self.save_file(args.export_to))
        elif args.import_from:
            self.get_log(self.read_file(args.import_from))
            self.main()
        elif args.export_to:
            self.main()
            self.get_log(self.save_file(args.export_to))
        else:
            self.main()


flashcard = Cards()
if __name__ == "__main__":
    flashcard.arg_parser()
