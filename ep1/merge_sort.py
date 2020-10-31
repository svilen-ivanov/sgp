#!/usr/bin/env python3


def merge_sort(elements):
    count = len(elements)
    if count <= 1:
        return elements
    middle = count // 2
    left = merge_sort(elements[:middle])
    right = merge_sort(elements[middle:])
    return merge(left, right)


def merge(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    if i < len(left):
        result.extend(left[i:])
    elif j < len(right):
        result.extend(right[j:])

    return result


print(merge_sort([3, 4, 5, 6]))
print(merge_sort([3, 5, 4, 6]))
print(merge_sort([7, 3, 5, 4, 6]))
print(merge_sort([7, 3, 5, 4, 6, 1]))
