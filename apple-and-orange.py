#!/bin/python
# Solution for https://www.hackerrank.com/challenges/apple-and-orange

import sys

s,t = [int(x) for x in raw_input().strip().split(' ')]
a,b = [int(x) for x in raw_input().strip().split(' ')]
m,n = [int(x) for x in raw_input().strip().split(' ')]
apple = map(int,raw_input().strip().split(' '))
orange = map(int,raw_input().strip().split(' '))

apple_count = 0
for idx in range(m):
    v = a + apple[idx]
    if s <= v <= t:
        apple_count += 1

orange_count = 0
for idx in range(n):
    v = b + orange[idx]
    if s <= v <= t:
        orange_count += 1

print apple_count
print orange_count