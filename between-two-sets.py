#!/bin/python
# Solution for https://www.hackerrank.com/challenges/between-two-sets

import sys

n, m = map(int, raw_input().strip().split(' '))
A = map(int, raw_input().strip().split(' '))
B = map(int, raw_input().strip().split(' '))

min_a = min(A)
min_b = min(B)

between_count = 0

if min_a <= min_b:
    for val in range(min_a, min_b + 1):
        val_is_between = True
        for a_i in A:
            if val % a_i: 
                val_is_between = False
                break
        if not val_is_between: 
            continue
        for b_i in B:
            if b_i % val: 
                val_is_between = False
                break
        if val_is_between: 
            between_count += 1
            
print between_count