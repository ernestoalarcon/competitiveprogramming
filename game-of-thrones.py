#!/bin/python
# Solution for https://www.hackerrank.com/challenges/game-of-thrones

string = raw_input().strip()

def can_be_palindrome(data):
    odd_requencies = 0
    for l in set(data):
        current_frequency = data.count(l)
        if current_frequency % 2: 
            odd_requencies += 1
        if odd_requencies > 1:
            return False
    return True
 
palindromable = can_be_palindrome(string)

if not palindromable:
    print("NO")
else:
    print("YES")
