#!/bin/python

def partition(ar, left, right):
    right_idx = right
    left_idx = left
    pivot = ar[right]

    while left_idx < right_idx:
        if ar[left_idx] >= pivot:
            while left_idx < right_idx and ar[right_idx] >= pivot:
                right_idx -= 1
            if left_idx < right_idx:
                ar[right_idx], ar[left_idx] = ar[left_idx], ar[right_idx]
                right_idx -= 1
            else:
                break
        left_idx += 1

    if ar[left_idx] > pivot:
        ar[left_idx], ar[right] = ar[right], ar[left_idx]

    print(' '.join(str(v) for v in ar))
    return left_idx

def quick_sort(ar, left, right):
    if left >= right:
        return ar
    pivot_idx = partition(ar, left, right)
    quick_sort(ar, left, pivot_idx-1)
    quick_sort(ar, pivot_idx+1, right)
    return ar

#m = input()
#ar = [int(i) for i in raw_input().strip().split()]
ar = [4, 2, 1, 3, 9, 9, 8, 3, 2, 7, 5]
#partition(ar, 0, len(ar) - 1)
quick_sort(ar, 0, len(ar) - 1)