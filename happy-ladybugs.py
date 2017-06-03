#!/bin/python
# Solution for https://www.hackerrank.com/challenges/happy-ladybugs

import sys

empty = '_'

def is_happy(s):
    if len(s) == 0:
        return True
    if len(s) == 1 and s == empty:
        return True
    if len(s) == 1 and s != empty:
        return False
    for i, c in enumerate(s):
        if c != empty and ((i == 0 or c != s[i-1]) and (i == len(s)-1 or c != s[i+1])):
            return False
    return True

Q = int(raw_input().strip())
for a0 in xrange(Q):
    n = int(raw_input().strip())
    b = raw_input().strip()

    empty_count = b.count(empty)
    b_counts = { c: b.count(c) for c in (set(b) - { empty }) }
    if any((v == 1 for v in b_counts.values())):
        print 'NO'
    elif empty_count <= 0 and not is_happy(b):
        print 'NO'
    else:
        print 'YES'