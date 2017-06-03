#!/bin/python
# Solution for https://www.hackerrank.com/challenges/detect-html-tags

import re

def get_tags(s):
    tag_pattern = r'<\s*([a-zA-Z]\w*)\s*?(?:\s+[a-zA-Z]\w*\s*=\s*".*?"\s*)*/?\s*>'
    
    tags = []
    for m in re.finditer(tag_pattern, s):
        ag = m.groups()
        tags.append(m.group(1))
    return tags

n = int(raw_input().strip())
tags = []
for i in range(n):
    s = raw_input().strip()
    tags.extend(get_tags(s))
print ';'.join(sorted(set(tags)))