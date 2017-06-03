
# Solution for https://www.hackerrank.com/challenges/caesar-cipher-1
import sys

n = int(raw_input().strip())
s = raw_input().strip()
k = int(raw_input().strip())

lowers = range(ord('a'), ord('z') + 1)
uppers = range(ord('A'), ord('Z') + 1)
alphabet_count = len(lowers)

cyphered = []
for idx in range(len(s)):
    curr = ord(s[idx])
    if curr in lowers:
        idx_curr = lowers.index(curr)
        idx_curr = (idx_curr + k) % alphabet_count
        curr = lowers[idx_curr]
    elif curr in uppers:
        idx_curr = uppers.index(curr)
        idx_curr = (idx_curr + k) % alphabet_count
        curr = uppers[idx_curr]
    cyphered.append(chr(curr))
print ''.join(cyphered)