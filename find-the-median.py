def partition(ar, median_idx):
    left, middle, right = [], [], []
    pivot = ar[median_idx]
    for v in ar:
        if v < pivot:
            left.append(v)
        elif v > pivot:
            right.append(v)
        else:
            middle.append(v)
    median_found = len(left) <= median_idx <= len(left) + len(middle)
    return left+middle+right, median_found

def median(ar):
    median_idx = len(ar) // 2
    pivot_idx = 0
    while True:
        ar, median_found = partition(ar, median_idx)
        if median_found:
            break
    return ar[median_idx]

n = int(raw_input().strip())
ar = [int(v) for v in raw_input().strip().split()]

print median(ar)