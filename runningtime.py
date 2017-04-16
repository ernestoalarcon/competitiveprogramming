#!/bin/python
def insertNewElement(ar, pos):
    shifts = 0
    e = ar[pos]
    idx = pos - 1
    while idx >=0 and ar[idx] > e:
        shifts += 1
        ar[idx+1] = ar[idx]
        idx -= 1
    ar[idx+1] = e
    return shifts

def insertionSort(ar):
    shifts = 0

    if len(ar) <= 1:
        return
    for pos in range(1, len(ar)):
        shifts += insertNewElement(ar, pos)
        #print(' '.join(str(v) for v in ar))
    return shifts

m = input()
ar = [int(i) for i in raw_input().strip().split()]
print(insertionSort(ar))