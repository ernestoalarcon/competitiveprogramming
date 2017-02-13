
#!/bin/python
# Solution for https://www.hackerrank.com/challenges/beautiful-days-at-the-movies
import sys

i, j, k = [int(x) for x in raw_input().strip().split(' ')]

count = 0
for v in range(i, j+1):
    if abs(v - int(str(v)[::-1])) % k == 0:
        count += 1
print count