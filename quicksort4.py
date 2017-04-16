#!/bin/python

'''Quick Sort'''

def partition(ar, left, right):
    shifts = 0
    right_idx = right
    left_idx = left
    pivot = ar[right]

    while left_idx < right_idx:
        if ar[left_idx] >= pivot:
            while left_idx < right_idx and ar[right_idx] >= pivot:
                right_idx -= 1
            if left_idx < right_idx:
                ar[right_idx], ar[left_idx] = ar[left_idx], ar[right_idx]
                shifts += 1
                right_idx -= 1
            else:
                break
        left_idx += 1

    if ar[left_idx] > pivot:
        ar[left_idx], ar[right] = ar[right], ar[left_idx]
        shifts += 1
    
    return left_idx, shifts

def quick_sort(ar, left, right):
    shifts = 0
    if left < right:
        pivot_idx, shifts = partition(ar, left, right)
        shifts += quick_sort(ar, left, pivot_idx-1)
        shifts += quick_sort(ar, pivot_idx+1, right)
    return shifts

'''Insertion Sort'''

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

#m = input()
#ar = [int(i) for i in raw_input().strip().split()]
ar1 = [4, 2, 1, 3, 9, 9, 8, 3, 2, 7, 5]
ar2 = list(ar1[:])
print(insertionSort(ar1) - quick_sort(ar2, 0, len(ar2) - 1))