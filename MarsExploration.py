# Solution for https://www.hackerrank.com/challenges/mars-exploration

import sys

S = raw_input().strip()
err_count = 0

for idx in range(len(S)/3):
	if S[idx*3] != 'S': err_count += 1
	if S[idx*3+1] != 'O': err_count += 1
	if S[idx*3+2] != 'S': err_count += 1

print (err_count)