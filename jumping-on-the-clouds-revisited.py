
#!/bin/python
# Solution for https://www.hackerrank.com/challenges/jumping-on-the-clouds-revisited

import sys

n,k = raw_input().strip().split(' ')
n,k = [int(n),int(k)]
c = map(int,raw_input().strip().split(' '))

E = 100
current = 0
time = 0

while not (time > 0 and current == 0):
    current += k
    current = current % n
    if c[current] == 0:
        E -= 1
    if c[current] == 1:
        E -= 3
    time += 1

print E