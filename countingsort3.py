
def count_items(ar):
    count = {}
    for idx in range(100):
        count[idx] = 0
    for v in ar:
        count[v] += 1
    return count

n = int(raw_input().strip())
ar = []
for idx in range(n):
    ar.append(int(raw_input().strip().split()[0]))
count_map = count_items(ar)
count = 0
items_set = set(ar)

result = ''
for idx in range(100):
    if idx in items_set:
        count += count_map[idx]
    result = result + ' ' + str(count)

print result.strip()