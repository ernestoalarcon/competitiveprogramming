#!/bin/python
# Solution for https://www.hackerrank.com/challenges/mini-max-sum

import sys

a,b,c,d,e = raw_input().strip().split(' ')
values = [int(a),int(b),int(c),int(d),int(e)]
min_sum = None
max_sum = None

for idx in range(len(values)):
    four_values = values[:idx] + values[idx+1:]
    current_sum = reduce(lambda v1, v2: v1 + v2, four_values)
    if min_sum == None or min_sum > current_sum:
        min_sum = current_sum
    if max_sum == None or max_sum < current_sum:
        max_sum = current_sum
print "%d %d" % (min_sum, max_sum)