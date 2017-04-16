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
    return left + equal + right

m = input()
ar = [int(i) for i in raw_input().strip().split()]
result = partition(ar)
print ' '.join(str(v) for v in result)