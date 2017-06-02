#!/bin/python
# Solution for https://www.hackerrank.com/challenges/migratory-birds

n = int(raw_input().strip())
values = [int(x) for x in raw_input().strip().split(' ')]
frequencies = {1:0, 2:0, 3:0, 4:0, 5:0}
max_frequency = 0
max_type = 5
for v in values:
    frequencies[v] += 1
    if max_frequency < frequencies[v] or (max_frequency == frequencies[v] and v < max_type):
        max_type = v
        max_frequency = frequencies[v]
print max_type