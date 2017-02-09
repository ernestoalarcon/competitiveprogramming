#!/bin/python
# Solution for https://www.hackerrank.com/challenges/kangaroo

import sys


x1,v1,x2,v2 = raw_input().strip().split(' ')
x1,v1,x2,v2 = [int(x1),int(v1),int(x2),int(v2)]

# x1 + k * v1 = x2 + k * v2
#k = (x2 - x1) / (v1 - v2)
#v1 - v2 != 0
#(x2 - x1) % (v1 - v2) == 0
#(x2 - x1) / (v1 - v2) >= 0

if (v1 - v2 != 0) and ((x2 - x1) % (v1 - v2) == 0) and ((x2 - x1) / (v1 - v2) >= 0):
    print 'YES'
else:
    print 'NO'

  
