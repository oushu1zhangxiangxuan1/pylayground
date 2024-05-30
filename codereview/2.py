def reverse_string(s):
    reversed = ''
    for c in s:
        reversed = c + reversed
    return reversed

print(reverse_string("hello"))