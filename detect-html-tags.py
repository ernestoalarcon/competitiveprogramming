import re

#n = int(input().strip())

def get_tags(fragment):
    tags = set()
    for rem in re.finditer(r'<\s*([a-zA-Z]+).*(/\s*>|>.*<\s*/\s*\1\s*>)', fragment):
        tags.update(rem.groups())
    return tags

test = '<   p > H ol a< /  p><a href="123">123 </a><div /><br />'
tags = get_tags(test)
print(tags)
exit()

tags = set()
for i in range(n):
    fragment = input().strip()
    tags.update(get_tags(fragment))

print(';'.join(sorted(list(tags))))