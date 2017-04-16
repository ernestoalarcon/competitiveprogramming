n = int(raw_input().strip())
ar = [int(v) for v in raw_input().strip().split()]

count = {}

for idx in range(100):
    count[idx] = 0

for v in ar:
    count[v] += 1

print ' '.join(str(count[idx]) for idx in range(100))