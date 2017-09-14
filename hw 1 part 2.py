# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
#
# Example input: 'read'
# Example output: 'reading'
def verbing(s):
    if len(s) < 3:
        string = s
    elif s[-3:] == 'ing':
        string = s[0: len(s) - 3] + 'ly'
    else:
        string = s + 'ing'
    return string


# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
#
# Example input: 'This dinner is not that bad!'
# Example output: 'This dinner is good!'
def not_bad(s):
    NOT = s.find('not')
    BAD = s.find('bad')
    if NOT == -1:
        string = s
    elif BAD == -1:
        string = s
    elif BAD > NOT:
        string = s[:NOT] + "good" + s[BAD + 3:]
    else:
        string = s
    return string


# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
#
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
#
# Example input: 'abcd', 'xy'
# Example output: 'abxcdy'
def front_back(a, b):
    if len(a) % 2 == 0:
        A = int(len(a) / 2)
    else:
        A = int(len(a) / 2 + 1)
    if len(b) % 2 == 0:
        B = int(len(b) / 2)
    else:
        B = int(len(b) / 2 + 1)
    return a[:A] + b[:B] + a[A:] + b[B:]
