#!/bin/python
# Solution for https://www.hackerrank.com/challenges/birthday-cake-candles

n = int(input().strip())
candles = [int(x) for x in input().strip().split(' ')]
frequencies = {}
max_candle = 0
for c in candles:
    if c >= max_candle:
        max_candle = c
        frequencies.setdefault(c, 0)
        frequencies[c] += 1

print frequencies[max_candle]