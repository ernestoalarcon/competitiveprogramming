#!/bin/python
def insertNewElement(ar, pos):
    e = ar[pos]
    idx = pos - 1
    while idx >=0 and ar[idx] > e:
        ar[idx+1] = ar[idx]
        idx -= 1
    ar[idx+1] = e

def insertionSort(ar):
    if len(ar) <= 1:
        return
    for pos in range(1, len(ar)):
        insertNewElement(ar, pos)
        print(' '.join(str(v) for v in ar))

m = input()
ar = [int(i) for i in raw_input().strip().split()]
insertionSort(ar)