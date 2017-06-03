#!/bin/python
# Solution for https://www.hackerrank.com/challenges/manasa-and-stones

T = int(raw_input().strip())
for case in xrange(T):
    n = int(raw_input().strip())
    a = int(raw_input().strip())
    b = int(raw_input().strip())
    a, b = min(a, b), max(a, b)
    print ' '.join(str(v) for v in sorted(list(set((a*(n - k) + b*k for k in xrange(n+1))))))