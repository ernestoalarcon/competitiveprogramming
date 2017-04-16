
def count_items(ar):
    count_map = {}
    for idx in range(100):
        count_map[idx] = [0, []]
    for item in ar:
        count_map[item[0]][0] += 1
        count_map[item[0]][1].append(item[1])
    return count_map

n = int(raw_input().strip())

ar = []
for idx in range(n):
    first_half = False
    if idx < n // 2: 
        first_half = True
    k, v = raw_input().strip().split()
    if first_half:
        ar.append((int(k), '-'))
    else:
        ar.append((int(k), v))

count_map = count_items(ar)

result = ''
for idx in range(100):
    if count_map[idx][0] > 0:
        result = result + ' ' + ' '.join(str(item) for item in count_map[idx][1])

print result.strip()