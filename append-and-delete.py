
#!/bin/python
# Solution for https://www.hackerrank.com/challenges/append-and-delete

import sys

s = raw_input().strip()
t = raw_input().strip()
k = int(raw_input().strip())

equal_start_len = 0

for idx in range(len(s)):
    if idx < len(t) and s[idx] == t[idx]:
        equal_start_len += 1
    else:
        break
        
operation_difference = len(s) + len(t) - 2 * equal_start_len

operations_left = k - operation_difference

if operations_left < 0:
    print 'No'
elif operations_left %2 == 0:
    print 'Yes'
elif operations_left >= 2 * equal_start_len:
    print 'Yes'
else:
    print 'No'