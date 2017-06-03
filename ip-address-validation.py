import re

def is_ipv4(value):
    rem = re.match(r'\b((25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(25[0-5]|2[0-4]\d|[01]?\d?\d)\b', value)
    if rem:
        return True
    return False

def is_ipv6(value):
    rem = re.match(r'^[0-9a-f]{1,4}:[0-9a-f]{1,4}:[0-9a-f]{1,4}:[0-9a-f]{1,4}:[0-9a-f]{1,4}:[0-9a-f]{1,4}:[0-9a-f]{1,4}:[0-9a-f]{1,4}$', value)
    if rem:
        return True
    return False

n = int(input().strip())
for i in range(n):
    line = input().strip()
    if is_ipv4(line):
        print ('IPv4')
    elif is_ipv6(line):
        print ('IPv6')
    else:
        print ('Neither')