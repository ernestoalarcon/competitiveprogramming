#!/bin/python
# Solution for https://www.hackerrank.com/challenges/breaking-best-and-worst-records

n = int(raw_input().strip())
scores = [int(x) for x in raw_input().strip().split(' ')]

min_breaks, max_breaks = 0, 0
for i, s in enumerate(scores):
    if i == 0:
        min_score, max_score = s, s
    else:
        if min_score > s:
            min_breaks += 1
            min_score = s
        elif max_score < s:
            max_breaks += 1
            max_score = s
print max_breaks, min_breaks