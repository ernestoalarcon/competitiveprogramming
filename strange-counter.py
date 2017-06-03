
#!/bin/python
# Solution for https://www.hackerrank.com/challenges/strange-code

import sys

t = int(raw_input().strip())
#t = 21

initial_counter = 3
counter = initial_counter

periodSum = 0

period = 1
periodLength = 3 * (2**(period - 1))
lastPeriodSum = 0
periodSum += periodLength

while periodSum < t:
    period += 1
    periodLength = 3 * (2**(period - 1))
    lastPeriodSum = periodSum
    periodSum += periodLength

counter_value = periodLength - (t - lastPeriodSum) + 1
    
print counter_value