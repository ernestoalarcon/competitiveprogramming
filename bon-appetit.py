
# Solution for https://www.hackerrank.com/challenges/bon-appetit

n, k = [int(x) for x in raw_input().strip().split(' ')]
c = [int(x) for x in raw_input().strip().split(' ')]
p = int(raw_input().strip())

share = (sum(c) - c[k]) / 2

if p == share:
    print "Bon Appetit"
else:
    print (p - share)