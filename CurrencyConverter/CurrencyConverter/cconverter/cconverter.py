import json
import requests

curr = input().upper()

json_file = requests.get(f"http://www.floatrates.com/daily/{curr.lower()}.json")
chosen_currency = json.loads(json_file.text)

if curr == 'USD':
    curr_cache = {'EUR': chosen_currency['eur']['rate']}
elif curr == 'EUR':
    curr_cache = {'USD': chosen_currency['usd']['rate']}
else:
    curr_cache = {'USD': chosen_currency['usd']['rate'], 'EUR': chosen_currency['eur']['rate']}

while True:
    ex_curr = input().upper()
    if ex_curr == '':
        break

    amount = float(input())

    print('Checking the cache...')

    if ex_curr in curr_cache.keys():
        print("Oh! It is in the cache!")
    else:
        print("Sorry, but it is not in the cache")
        curr_cache[ex_curr] = chosen_currency[ex_curr.lower()]['rate']

    print(f"You received {round(curr_cache[ex_curr] * amount, 2)} {ex_curr}.")



