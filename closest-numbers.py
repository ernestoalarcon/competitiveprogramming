n = input()
ar = [int(v) for v in raw_input().strip().split()]
ar.sort()
min_diff = None

diff_map = { }
for idx in range(len(ar) - 1):
    diff = abs(ar[idx] - ar[idx+1])
    diff_map.setdefault(diff, []).extend((ar[idx], ar[idx+1]))
    if min_diff is None or min_diff > diff:
        min_diff = diff

print ' '.join(str(v) for v in diff_map[min_diff])