
#!/bin/python
# Solution for https://www.hackerrank.com/challenges/two-characters

import sys
import itertools

def trim_except(s, pair):
    result = []
    for cur in s:
        if cur in pair:
            result.append(cur)
    return ''.join(result)

def is_alternating(s):
    if len(s) <= 1:
        return True
    chrEven = s[0]
    chrOdd = s[1]
    for idx, cur in enumerate(s):
        if not idx % 2 and cur != chrEven:
            return False
        if idx % 2 and cur != chrOdd:
            return False
    return True

s_len = int(raw_input().strip())
s = raw_input().strip()

maxAlternating = 0
chrSet = set(s)
chrCombinations = itertools.combinations(chrSet, 2)
for pair in chrCombinations:
    sTrimmed = trim_except(s, pair)
    if is_alternating(sTrimmed) and len(sTrimmed) > maxAlternating:
        maxAlternating = len(sTrimmed)
        
print maxAlternating