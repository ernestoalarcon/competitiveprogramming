#!/bin/python
# Solution for https://www.hackerrank.com/challenges/minimum-distances

import sys

n = int(raw_input().strip())
arr = map(int,raw_input().strip().split(' '))

fr = {}
for idx, val in enumerate(arr):
    fr.setdefault(val, []).append(idx)

min_distance = len(arr)
for val in fr:
    if len(fr[val]) > 1:
        idxs = list(sorted(fr[val]))
        local_min_distance = abs(idxs[0] - idxs[-1])
        if min_distance > local_min_distance:
            min_distance = local_min_distance

if min_distance == len(arr):
    print -1 
else:
    print min_distance