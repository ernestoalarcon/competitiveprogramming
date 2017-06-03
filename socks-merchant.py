
#!/bin/python
# Solution for https://www.hackerrank.com/challenges/sock-merchant

import sys

n = int(raw_input().strip())
c = [int(x) for x in raw_input().strip().split(' ')]

frequecies = {}
for idx in range(len(c)):
    if c[idx] in frequecies:
        frequecies[c[idx]] += 1
    else:
        frequecies[c[idx]] = 1

pairs = 0
for key in frequecies.keys():
    pairs += frequecies[key] // 2
    
print pairs