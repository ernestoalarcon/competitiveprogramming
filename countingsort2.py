n = int(raw_input().strip())
ar = [int(v) for v in raw_input().strip().split()]

count = {}
for idx in range(100):
    count[idx] = 0
for v in ar:
    count[v] += 1

result = ''
for idx in range(100):
    if count[idx] > 0:
        result = ' '.join(result,' '.join(str(idx) for c in range(count[idx])))

print result