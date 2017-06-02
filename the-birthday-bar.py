#!/bin/python
# Solution for https://www.hackerrank.com/challenges/the-birthday-bar

n = int(raw_input().strip())
values = [int(x) for x in raw_input().strip().split(' ')]
d, m  = [int(x) for x in raw_input().strip().split(' ')]

split_count = 0

if len(values) >= m:
    val_sum = sum(values[:m])
    if val_sum == d:
        split_count += 1
    idx_l, idx_r = 0, m
    while idx_r < len(values):
        val_sum += values[idx_r]
        val_sum -= values[idx_l]
        if val_sum == d:
            split_count += 1
        idx_l, idx_r = idx_l + 1, idx_r + 1

print split_count