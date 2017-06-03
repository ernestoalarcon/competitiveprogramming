
#!/bin/python
# Solution for https://www.hackerrank.com/challenges/strange-advertising

n = int(raw_input().strip())

total = 0
current = 2
total = current

for day in range(n-1):
    current = (current * 3) // 2
    total += current
    
print total    

#f(n+1) = f(n) * 3 // 2