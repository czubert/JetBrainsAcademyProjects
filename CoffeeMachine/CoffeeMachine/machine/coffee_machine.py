class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550

    def order(self):
        while True:
            print("Write action (buy, fill, take, remaining, exit):")
            action = input()
            if action == 'buy':
                print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
                coffee_type = input()
                self.buy(coffee_type)
            elif action == 'fill':
                self.fill()
            elif action == 'take':
                self.take()
            elif action == 'remaining':
                self.log_machine_status()
            elif action == 'exit':
                break
            else:
                print('something went wrong')

    def log_machine_status(self):
        print("The coffee machine has:")
        print(f'{self.water} ml of water')
        print(f'{self.milk} ml of milk')
        print(f'{self.beans} g of coffee beans')
        print(f'{self.cups} disposable cups')
        print(f'${self.money} of money')

    def buy(self, coffee):
        if coffee == '1':
            return self.produce_coffee(water=250, beans=16, money=4)
        elif coffee == '2':
            return self.produce_coffee(water=350, beans=20, money=7, milk=75)
        elif coffee == '3':
            return self.produce_coffee(water=200, beans=12, money=6, milk=100)
        elif coffee == 'back':
            return

    def produce_coffee(self, water, beans, money, milk=0, cups=1):
        if self.water < water:
            print(f"Sorry, not enough water!")
        elif self.milk < milk:
            print(f"Sorry, not enough milk!")
        elif self.beans < beans:
            print(f"Sorry, not enough beans!")
        elif self.cups < cups:
            print(f"Sorry, not enough cups!")
        else:
            print(f"I have enough resources, making you a coffee!")
            self.water -= water
            self.milk -= milk
            self.beans -= beans
            self.money += money
            self.cups -= cups

    def fill(self):
        print("Write how many ml of water you want to add:")
        water = int(input())
        self.water += water
        print("Write how many ml of milk you want to add:")
        milk = int(input())
        self.milk += milk
        print("Write how many grams of coffee beans you want to add:")
        beans = int(input())
        self.beans += beans
        print("Write how many disposable cups you want to add:")
        cups = int(input())
        self.cups += cups

    def take(self):
        print(f"I gave you ${self.money}")
        self.money = 0


customer = CoffeeMachine()
customer.order()
