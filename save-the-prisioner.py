
#!/bin/python
# Solution for https://www.hackerrank.com/challenges/save-the-prisoner
import sys

t = int(raw_input().strip())

for i in range(t):
    n, m, s = [int(x) for x in raw_input().strip().split(' ')]
    last = (s + m - 1) % n
    if last == 0: last = n
    print last