print('Day 25 of Advent of Code')

DIGITS = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
CONVERSION_TABLE = {'3': '=', '4': '-', '5': '0', '6': '1', '7': '2'}

def base10_to_SNAFU(num):
    def to_base_5(n):
        s = ""
        while n:
            s = str(n % 5) + s
            n //= 5
        return s
    SNAFU_digits = list(to_base_5(num)[::-1])
    i, j = 0, len(SNAFU_digits)
    while i < j:
        if SNAFU_digits[i] in CONVERSION_TABLE:
            SNAFU_digits[i] = CONVERSION_TABLE[SNAFU_digits[i]]
            if i < len(SNAFU_digits) - 1:
                SNAFU_digits[i+1] = str(int(SNAFU_digits[i+1]) + 1)
            else:
                SNAFU_digits.append(str(1))
                j += 1
        i += 1
    return ''.join(SNAFU_digits)[::-1]

SNAFU_to_base10 = lambda num: sum(DIGITS[dig] * 5**i for i, dig in enumerate(num[::-1]))

test_data = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''

print('Testing...')
print('Example data:', base10_to_SNAFU(sum(SNAFU_to_base10(line) for line in test_data.splitlines())) == '2=-1=0')

with open('inp.dat', mode='r') as inp:
    print('Solution...')
    print('Actual data:', base10_to_SNAFU(sum(SNAFU_to_base10(line) for line in inp.read().splitlines())))
