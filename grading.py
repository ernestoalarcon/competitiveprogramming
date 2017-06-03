#!/bin/python
# Solution for https://www.hackerrank.com/challenges/grading

import sys

def round_grade(grade):
    if grade >= 38 and grade % 5 >= 3:
        result = grade + (5 - (grade % 5))
    else:
        result = grade
    return result

n = int(raw_input().strip())
for a0 in xrange(n):
    grade = int(raw_input().strip())
    print round_grade(grade)
