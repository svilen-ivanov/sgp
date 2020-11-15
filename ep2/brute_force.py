

def subset_sum(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        remaining = numbers[:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)


if __name__ == '__main__':
    for x in subset_sum(list(reversed([1, 2, 5, 10, 20, 50])), 142):
        if (len(x)) < 10:
            x.sort()
            print(x)
