#!/bin/python
# Solution for https://www.hackerrank.com/challenges/equality-in-a-array

n = int(raw_input().strip())
a = [int(x) for x in raw_input().strip().split(' ')]

fr = {}
max_fr_key = None
max_fr = 0
for v in a:
    fr.setdefault(v, 0)
    fr[v] += 1
    if max_fr < fr[v]:
        max_fr = fr[v]
        max_fr_key = v
min_deletes = sum((fr[v] for v in fr if v != max_fr_key))
print min_deletes