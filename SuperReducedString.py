# Solution for https://www.hackerrank.com/challenges/reduced-string

import sys

def reduce_string(val):
    '''reduce_string documentation'''
    result = []
    i = 0
    while i < len(val) - 1:
        if val[i] != val[i + 1]:
            result.append(val[i])
            i += 1
        else:
            i += 2
    if i == len(val) - 1:
        result.append(val[-1])
    return ''.join(result)

value = sys.stdin.readlines()[0]
value_len_new = -1
value_len = 1

while value_len != value_len_new:
    value_len = len(value)
    value = reduce_string(value)
    value_len_new = len(value)

if len(value) == 0:
    print('Empty String')
else:
    print(value)
