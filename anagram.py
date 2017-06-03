#!/bin/python
# Solution for https://www.hackerrank.com/challenges/anagram

T = int(raw_input().strip())

for c in xrange(T):
    s1s2 = raw_input().strip()
    l = len(s1s2)
    if l % 2:
        print -1
        continue
    l = l / 2
    s1 = s1s2[:l]
    s2 = s1s2[l:]
    chr_s1 = {ch: s1.count(ch) for ch in set(s1)}
    chr_s2 = {ch: s2.count(ch) for ch in set(s2)}
    for ch in chr_s1:
        chr_s2.setdefault(ch, 0)
        chr_s2[ch] -= chr_s1[ch]
    change_count = 0
    for ch in chr_s2:
        change_count += abs(chr_s2[ch])
    change_count = change_count / 2
    print change_count