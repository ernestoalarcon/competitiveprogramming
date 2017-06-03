#!/bin/python
# Solution for https://www.hackerrank.com/challenges/bear-and-steady-gene

n = int(raw_input().strip())
s = raw_input().strip()

#n = 8
#s = 'GAAATAAA'

#file = open('testCases\\input02.txt', 'r')
#n = int(file.readline().strip())
#s = file.readline().strip()

def get_letter_count(s):
    s_count = {}
    for c in list(set(s)):
        s_count[c] = s.count(c)
    return s_count

def get_missing_letters_count(required_letters, substring_letters):
    result = 0
    for c in required_letters:
        if not c in substring_letters:
            result += required_letters[c]
        elif required_letters[c] > substring_letters[c]:
            result += required_letters[c] - substring_letters[c]
    return result

# find all minimum changes required
min_changes = 0 
fr = n / 4
s_count = get_letter_count(s)
s_errs = {}
for c in s_count:
    if s_count[c] > fr:
        s_errs[c] = s_count[c] - fr
        min_changes += s_errs[c]

# find shortest substring that has all characters and frequencies gathered in s_errs
if min_changes > 0:

    while min_changes < len(s):

        use_min_changes = False

        missing_letters_count = 0
        sub = None
        for i in xrange(len(s) - min_changes):
            if not sub: 
                sub = s[i: i + min_changes]
                sub_count = get_letter_count(sub)
            else:
                prev_sub = sub
                sub = s[i: i + min_changes]
                dropped_letter = prev_sub[0]
                added_letter = sub[-1]
                sub_count[dropped_letter] -= 1
                sub_count.setdefault(added_letter, 0)
                sub_count[added_letter] += 1

            if missing_letters_count == 0:
                missing_letters_count = get_missing_letters_count(s_errs, sub_count)
                if missing_letters_count == 0:
                    use_min_changes = True
                    break
            else:
                missing_letters_count -= 1

        if use_min_changes:
            break

        min_changes += 1

print min_changes