# Solution for https://www.hackerrank.com/challenges/camelcase

import sys

s = raw_input().strip()
r = 0
for c in s : 
    if c.isupper(): r += 1
print (r + 1)

