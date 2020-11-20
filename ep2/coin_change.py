import math


def min_coin_list(min_coins, amount):
    coin_list = []
    while amount >= 0 and min_coins[amount] is not None:
        min_coin = min_coins[amount]
        coin_list.append(min_coin)
        amount -= min_coin
    return coin_list


def min_coin_change(coins, amount):
    num_min_coins = [math.inf] * (amount + 1)
    min_coin = [None] * (amount + 1)
    num_min_coins[0] = 0

    for sub_amount in range(1, amount + 1): # for sub amounts from 1 to amount _inclusive_
        sub_num_min_coins = math.inf
        sub_min_coin = None
        for coin in coins:
            prev_amount = sub_amount - coin
            if prev_amount >= 0:
                candidate_num_min_coins = num_min_coins[prev_amount] + 1
                if candidate_num_min_coins < sub_num_min_coins:
                    sub_num_min_coins = candidate_num_min_coins
                    sub_min_coin = coin

        num_min_coins[sub_amount] = sub_num_min_coins
        min_coin[sub_amount] = sub_min_coin

    return min_coin_list(min_coin, amount), num_min_coins[amount]


def print_min_change(coins, amount):
    print(f"coins: {', '.join([str(c) for c in coins])} ")
    min_list, min_change = min_coin_change(coins, amount)
    print(f"min coins for {amount} is {min_change} ({', '.join([str(c) for c in min_list])})\n")


if __name__ == '__main__':
    coins = [1, 2, 5, 10, 20, 25]
    amount = 40
    print_min_change(coins, amount)

    coins = [1, 2, 5]
    amount = 13
    print_min_change(coins, amount)

    coins = [10, 20]
    amount = 5
    print_min_change(coins, amount)

    coins = [1, 2, 5, 10, 20, 50]
    amount = 142
    print_min_change(coins, amount)

