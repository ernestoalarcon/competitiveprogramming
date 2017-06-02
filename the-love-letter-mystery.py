#!/bin/python
# Solution for https://www.hackerrank.com/challenges/the-love-letter-mystery

T = int(raw_input().strip())
for c in xrange(T):
    s = raw_input().strip()
    result = 0
    for idx in xrange(len(s)//2):
        c1 = s[idx]
        c2 = s[(idx+1)*-1]
        if c1 != c2:
            result += abs(ord(c1) - ord(c2))
    print result