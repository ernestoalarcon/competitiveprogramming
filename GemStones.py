# Solution for https://www.hackerrank.com/challenges/gem-stones

import sys
import string

n = int(raw_input().strip())
rocks = []
for i in range(n):
	rocks.append(raw_input().strip())

elem_count = 0
for e in string.ascii_lowercase:
	is_in_all = 1
	for r in rocks:
		if e not in r:
			is_in_all = 0
			break
	if is_in_all == 1:
		elem_count += 1

print (elem_count)