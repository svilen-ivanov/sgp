import math
import time
import threading
from pprint import pprint

def min_coins_list(min_coins, amount):
    coin_list = []
    while amount >= 0 and min_coins[amount] is not None:
        min_coin = min_coins[amount]
        coin_list.append(min_coin)
        amount -= min_coin
    return coin_list


def min_coin_change(coins, amount):
    num_min_coins = [math.inf] * (amount + 1)
    min_coins = [None] * (amount + 1)

    num_min_coins[0] = 0
    min_coins[0] = None

    for sub_amount in range(1, amount + 1):  # for sub amounts from 1 to amount _inclusive_
        sub_num_min_coins = math.inf
        sub_min_coin = None
        for coin in coins:
            prev_amount = sub_amount - coin
            if prev_amount >= 0:
                candidate_min_coin = num_min_coins[prev_amount] + 1
                if candidate_min_coin < sub_num_min_coins:
                    sub_num_min_coins = candidate_min_coin
                    sub_min_coin = coin

        num_min_coins[sub_amount] = sub_num_min_coins
        min_coins[sub_amount] = sub_min_coin

    return min_coins_list(min_coins, amount), num_min_coins[amount]


if __name__ == '__main__':
    coins = [1, 2, 5]
    amount = 13
    header = "AAAAAA"
    e = threading.Event()

    def trace_calls(frame, event, arg):
        if event != 'call':
            return
        co = frame.f_code
        func_name = co.co_name
        if func_name == 'min_coin_change':
            return trace_func
        return

    def trace_func(frame, event, arg):
        print("-" * 78)
        print(header)
        rel_line = frame.f_lineno - frame.f_code.co_firstlineno
        print(f"Line {rel_line}")

        for var_name, var_value in frame.f_locals.items():
            print(f"{var_name} = {var_value}")
        print("-" * 78)
        e.wait()
        e.clear()
        return

    threading.settrace(trace_calls)
    thread = threading.Thread(target=min_coin_change, args=(coins, amount))
    thread.start()

    time.sleep(1)
    e.set()
    time.sleep(1)
    e.set()
    time.sleep(1)
    e.set()



