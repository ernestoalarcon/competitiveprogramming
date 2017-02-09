#!/bin/python
# Solution for https://www.hackerrank.com/challenges/divisible-sum-pairs

import sys


n,k = raw_input().strip().split(' ')
n,k = [int(n),int(k)]
a = map(int,raw_input().strip().split(' '))

div_count = 0
for idx1 in range(len(a)):
    for idx2 in range(idx1 + 1, len(a)):
        if not ((a[idx1] + a[idx2]) % k):
            div_count += 1
print div_count