import random
import sqlite3


class Account:
    IIN = 400000

    def __init__(self):

        self.pin = str(random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 4)).strip("[]").replace(',', '').replace(' ', '')
        self.card_number = str(Account.luhn_algorithm(self)).strip("[]").replace(',', '').replace(' ', '')

    def luhn_algorithm(self):
        card = [4, 0, 0, 0, 0, 0] + random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
        temp = card.copy()
        index = 0
        for digit in temp:
            if (index + 1) % 2 != 0:
                temp[index] = digit * 2
            index += 1
        index = 0
        for digit in temp:
            if digit > 9:
                temp[index] = digit - 9
            index += 1
        total = sum(temp)
        card.append((total * 9) % 10)
        return card

    def get_card_number(self):
        return self.card_number

    def get_pin(self):
        return self.pin


class Bank:
    def __init__(self):
        self.Accounts = []
        self.Accounts_details = {}
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance INTEGER DEFAULT 0
            );
            ''')
        self.conn.commit()

    def run(self):
        while True:
            choice = input('1. Create an account \n2. Log into account\n0. Exit\n')
            if choice == '1':
                Bank.create_account(self)
            elif choice == '2':
                card = input('Enter your card number:\n')
                pin = input('Enter your PIN:\n')
                if Bank.check_account(self, card, pin):
                    print('You have successfully logged in!')
                    Bank.login(self, card)
                else:
                    print('Wrong card number or PIN!')
            else:
                print('Bye!')
                exit()

    def check_account(self, card_number, pin):
        self.cur.execute('SELECT * FROM card')
        bank_data = self.cur.fetchall()
        for a in bank_data:
            if a[1] == card_number:
                if a[2] == pin:
                    return True
                else:
                    return False

    def check_card(self, card_number):
        self.cur.execute('SELECT * FROM card')
        bank_data = self.cur.fetchall()
        for a in bank_data:
            if a[1] == card_number:
                return True
        return False

    def check_receiver(self, card_number):
        temp = list(card_number).copy()
        check_digit = temp.pop()
        index = 0
        for digit in temp:
            if (index + 1) % 2 != 0:
                temp[index] = int(digit) * 2
            index += 1
        index = 0
        for digit in temp:
            if int(digit) > 9:
                temp[index] = int(digit) - 9
            index += 1
        total = 0
        for digit in temp:
            total += int(digit)
        return int(check_digit) == ((total * 9) % 10)

    def create_account(self):
        a = Account()
        self.cur.execute(f"INSERT INTO card(number, pin, balance) VALUES({a.get_card_number()}, {a.get_pin()}, 0)")
        self.conn.commit()
        print('Your card number:')
        print(a.get_card_number() + '\n')
        print('Your card PIN:')
        print(a.get_pin() + '\n')

    def add_income(self, card_number, amount):
        self.cur.execute(f'SELECT * FROM card WHERE number = {card_number}')
        card = self.cur.fetchall()
        self.cur.execute(f'UPDATE card SET balance = {card[0][3] + amount} WHERE number = {card_number}')
        self.conn.commit()

    def withdraw(self, card_number, amount):
        self.cur.execute(f'SELECT * FROM card WHERE number = {card_number}')
        card = self.cur.fetchall()
        self.cur.execute(f'UPDATE card SET balance = {card[0][3] - amount} WHERE number = {card_number}')
        self.conn.commit()

    def transfer(self, from_, to):
        if from_ == to:
            print('You can\'t transfer money to the same account!')
        elif not Bank.check_receiver(self, to):
            print('Probably you made mistake in the card number. Please try again!')
        elif not Bank.check_card(self, to):
            print("Such a card does not exist.")
        else:
            amount = int(input('Enter how much money you want to transfer:'))
            if amount > Bank.get_balance(self, from_):
                print('Not enough money!')
            else:
                Bank.add_income(self, to, amount)
                Bank.withdraw(self, from_, amount)
                print('Success!')

    def get_balance(self, card_number):
        self.cur.execute(f'SELECT * FROM card WHERE number = {card_number}')
        card = self.cur.fetchall()
        return card[0][3]

    def login(self, card_number):
        while True:
            choice = input('1. Balance \n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n')
            if choice == '1':
                print('Balance:', Bank.get_balance(self, card_number))
            elif choice == '2':
                amount = int(input('Enter income:'))
                Bank.add_income(self, card_number, amount)
            elif choice == '3':
                receiver = input('Enter card number:')
                Bank.transfer(self, card_number, receiver)
            elif choice == '4':
                self.cur.execute(f'DELETE FROM card WHERE number = {card_number}')
                self.conn.commit()
                print('The account has been closed!')
                break
            elif choice == '5':
                print('You have successfully logged out!')
                break
            else:
                print('Bye!')
                exit()


B = Bank()

B.run()