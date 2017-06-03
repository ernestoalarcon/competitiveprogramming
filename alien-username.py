#!/bin/python
# Solution for https://www.hackerrank.com/challenges/alien-username

import re

def is_valid_username(s):
    pattern = r'^[_\.][0-9]+[a-zA-Z]*_?$'
    match = re.match(pattern, s)
    return match

n = int(raw_input().strip())
for i in range(n):
    s = raw_input().strip()
    if is_valid_username(s):
        print 'VALID'
    else:
        print 'INVALID'