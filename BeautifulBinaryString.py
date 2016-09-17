# Solution for https://www.hackerrank.com/challenges/beautiful-binary-string

import sys

n = int(raw_input().strip())
B = raw_input().strip()

c = 0
while True:
	idx = B.find('010')
	if idx == -1: break
	B = B[:idx] + '011' + B[idx+3:]
	c += 1
print(c)