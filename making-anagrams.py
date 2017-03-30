#!/bin/python
# Solution for https://www.hackerrank.com/challenges/making-anagrams

a = raw_input().strip()
b = raw_input().strip()

def get_frequencies(data, letters):
    result = {}
    for l in letters:
        result[l] = data.count(l)
    return result

a_set = set(a)
b_set = set(b)
all_set = a_set | b_set

a_fr = get_frequencies(a, a_set)
b_fr = get_frequencies(b, b_set)

differences = 0

for l in all_set:
    if l in a_set and l in b_set:
        differences += abs(a_fr[l] - b_fr[l])
    elif l in a_set:
        differences += a_fr[l]
    elif l in b_set:
        differences += b_fr[l]

print differences