#!/bin/python
# Solution for https://www.hackerrank.com/challenges/detect-the-email-addresses

import re

def get_emails(s):
    email_pattern = r'\b(\w+(?:\.\w+)*@(?:\w+\.)+\w+)\b'
    
    emails = []
    for m in re.finditer(email_pattern, s):
        ag = m.groups()
        emails.append(m.group(1))
    return emails

n = int(raw_input().strip())
emails = []
for i in range(n):
    s = raw_input().strip()
    emails.extend(get_emails(s))
print ';'.join(sorted(set(emails)))