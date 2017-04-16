#!/bin/python

def partition(ar):
    left = []
    right = []
    equal = []
    if len(ar) > 0:
        pivot = ar[0]
        for x in ar:
            if x < pivot:
                left.append(x)
            elif x > pivot:
                right.append(x)
            else:
                equal.append(x)
    return left, equal, right

def quick_sort(ar):
    if len(ar) <= 1:
        return ar
    left, equal, right = partition(ar)
    result = quick_sort(left) + equal + quick_sort(right)
    print(' '.join(str(v) for v in result))
    return result

m = input()
ar = [int(i) for i in raw_input().strip().split()]
quick_sort(ar)