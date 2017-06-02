#!/bin/python
# Solution for https://www.hackerrank.com/challenges/fair-rations

import sys

N = int(raw_input().strip())
B = [int(x) for x in raw_input().strip().split(' ')]

def is_impossible(dist):
    return len([x for x in dist if x%2])%2

if is_impossible(B):
    print 'NO'
else:
    count = 0
    idx1 = 0
    idx2 = 0
    while idx1 < len(B):

        if not B[idx1]%2:
            idx1 += 1
            continue
            
        idx2 = idx1 + 1
        while idx2 < len(B) and not B[idx2]%2:
            idx2 += 1
        
        if idx1 < idx2 < len(B):
            count += (idx2 - idx1) * 2

        idx1 = idx2 + 1

    print count