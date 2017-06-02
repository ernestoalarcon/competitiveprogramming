#!/bin/python
# Solution for https://www.hackerrank.com/challenges/ip-address-validation

import re

def is_ipv4(val):
    v4_pattern = r'\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b'
    match = re.search(v4_pattern, val)
    if match:
        for v in (int(x) for x in match.groups()):
            if not (0 <= v <= 255):
                return False
        return True
    return False
    
def is_ipv6(val):
    v6_pattern = r'\b([0-9abcdef]{1,4}):([0-9abcdef]{1,4}):([0-9abcdef]{1,4}):([0-9abcdef]{1,4}):([0-9abcdef]{1,4}):([0-9abcdef]{1,4}):([0-9abcdef]{1,4}):([0-9abcdef]{1,4})\b'
    match = re.search(v6_pattern, val)
    if match:
        return True
    return False

n = int(raw_input().strip())
for i in range(n):
    v = raw_input().strip()
    if is_ipv4(v):
        print 'IPv4'
    elif is_ipv6(v):
        print 'IPv6'
    else:
        print 'Neither'