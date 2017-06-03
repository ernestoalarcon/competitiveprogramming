#!/bin/python
# Solution for https://www.hackerrank.com/challenges/almost-sorted

n = int(raw_input().strip())
values = [int(s) for s in raw_input().strip().split(' ')]
ascending = 1
descending = 2

def is_ascending_or_descending(data, direction):
    if len(data) <= 1:
        return True
    item = data[0]
    for i in range(1, len(data)):
        if direction == ascending and item > data[i]:
            return False
        if direction == descending and item < data[i]:
            return False
        item = data[i]
    return True

if len(values) <= 1:
    print 'yes'
else:
    cu_v = values[0]
    de_count, de_l, de_r, direction = 0, None, None, None    
    for i in range(1, len(values)):
        ne_v = values[i]
        if cu_v > ne_v and direction in { None, ascending }: # Change to descending
            de_count += 1
            direction = descending
            de_l = i - 1
        if cu_v < ne_v and direction in { None, descending }: # Change to ascending
            direction = ascending
            de_r = i - 1
        cu_v = ne_v
    
    if de_count <= 0:
        print 'yes'
    elif de_count > 1:
        print 'no'
    else:
        if de_r is None or de_r < de_l:
            de_r = len(values) - 1
        while de_r < len(values) and values[de_r] == values[de_r+1]:
            de_r += 1
        while de_l > 0 and values[de_l] == values[de_l-1]:
            de_l -= 1
        values = values[:de_l] + list(reversed(values[de_l:de_r + 1])) + values[de_r + 1:]
        if is_ascending_or_descending(values, ascending):
            print 'yes'
            if de_r - de_l + 1 > 2:
                print 'reverse', de_l + 1, de_r + 1
            else:
                print 'swap', de_l + 1, de_r + 1
        else:
            print 'no'