
#!/bin/python
# Solution for https://www.hackerrank.com/challenges/repeated-string

import sys

s = raw_input().strip()
n = long(raw_input().strip())

as_in_s = s.count('a')

if as_in_s == 0:
    print '0'
else:
    s_times = n // len(s)
    left_chars = n % len(s)

    as_in_left_chars = 0
    for idx in range(left_chars):
        if s[idx] == 'a':
            as_in_left_chars += 1

    total_as = s_times * as_in_s + as_in_left_chars

    print total_as