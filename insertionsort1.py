#!/bin/python
def insertionSort(ar):
    e = ar[-1]
    idx = len(ar) - 2

    while idx >= 0:
        if ar[idx] > e:
            ar[idx+1] = ar[idx]
            print (' '.join(str(v) for v in ar))
            idx -= 1
        else:
            break

    ar[idx+1] = e
    print (' '.join(str(v) for v in ar))
    return ""

#m = input()
#ar = [int(i) for i in raw_input().strip().split()]

m = 5
ar = [2, 4, 6, 8, 8, 7]

insertionSort(ar)