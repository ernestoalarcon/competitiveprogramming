#!/bin/python
# Solution for https://www.hackerrank.com/challenges/the-hurdle-race

import sys

n,k = raw_input().strip().split(' ')
n,k = [int(n),int(k)]
height = map(int, raw_input().strip().split(' '))

max_height = max(height)
if k < max_height:
    print max_height - k
else:
    print 0