from timeit import default_timer as timer
import re
import math


class Expression:

    def __init__(self, operator, number, child1, child2, is_digit=False):
        self.operator = operator
        self.number = number
        self.child1 = child1
        self.child2 = child2
        self.is_digit = is_digit

    def get_number(self):
        return self.number

    def get_operator(self):
        return self.operator

    def __add__(self, other):
        return self.number + other.number

    def __sub__(self, other):
        return self.number - other.number

    def __mul__(self, other):
        return self.number * other.number

    def __truediv__(self, other):
        return self.number / other.number


def create_numbers(target_number, digit, operations):
    found_numbers = set()
    rows = [[Expression(None, digit, None, None, True)]]
    if digit < 14:
        result = math.factorial(digit)
        rows[0].append(Expression('!', result, rows[0][0], None))
        found_numbers.add(result)
        if result == target_number:
            print("Number of Digits:")
            print(len(rows))
            return rows[0][1]
    found_numbers.add(digit)
    if rows[0][0].get_number() == target_number:
        print("Number of Digits:")
        print(len(rows))
        return rows[0][0]
    n = 1
    exponent = 6
    if digit > 9:
        exponent = 12
    maximum = 10**exponent    # Performance depends on this number
    while n <= 40:
        if rows[n-1][0].is_digit:
            result = int(str(rows[n - 1][0].get_number()) + str(digit))
            if result < maximum:
                rows.append([Expression(None, result, None, None, True)])
                found_numbers.add(result)
            else:
                rows.append([])
        else:
            rows.append([])

        if n == 1 and digit != 1:
            rows[-1].append(Expression('/', 1, rows[0][0], rows[0][0]))
            found_numbers.add(1)
        for e in rows[n - 1]:
            result = e.get_number()
            if result <= 2:
                continue
            count = 0
            while result <= 10:
                result = math.factorial(result)
                if result not in found_numbers:
                    if count > 0:
                        rows[n-1].append(Expression('!', result, rows[n-1][-1], None))
                    else:
                        rows[n-1].append(Expression('!', result, e, None))
                    if result == target_number:
                        print("Number of Digits:")
                        print(len(rows) - 1)
                        return rows[n-1][-1]
                count += 1
        n1 = 0
        n2 = n - 1
        while not n2 < n1:
            for i in rows[n1]:
                for j in rows[n2]:
                    for k in operations:
                        reversed = False
                        num1 = i.get_number()
                        num2 = j.get_number()
                        if k == '+':
                            result = num1 + num2
                            if result > maximum:
                                continue
                        elif k == '-':
                            if num1 > num2:
                                result = num1 - num2
                            elif num2 > num1:
                                result = num2 - num1
                                reversed = True
                            else:
                                continue
                        elif k == '*':
                            result = num1 * num2
                            if result > maximum:
                                continue
                        elif k == '/':
                            if num1 <= 1 or num2 <= 1:
                                continue
                            if num1 > num2:
                                result = num1 / num2
                            elif num1 < num2:
                                result = num2 / num1
                                reversed = True
                            else:
                                continue
                            if result % 1 == 0:
                                result = int(result)
                            else:
                                continue
                        elif k == '^':
                            result = 1
                            p = num2
                            b = num1
                            if p < 12 and b < 12:
                                while p:
                                    if p & 0x1:
                                        result *= b
                                    b *= b
                                    p >>= 1
                                    if b > maximum:
                                        break
                                if result > maximum:
                                    continue
                            else:
                                continue
                        if result not in found_numbers:
                            if reversed:
                                rows[n].append(Expression(k, result, j, i))
                            else:
                                rows[n].append(Expression(k, result, i, j))
                            found_numbers.add(result)
                            if result == target_number:
                                print("Number of Digits:")
                                print(len(rows))
                                return rows[n][-1]
            n1 += 1
            n2 -= 1
        n += 1
    print("Program interrupted because number of combinated digtis is greater than 40")


def get_term(a, operator, b):

    if a.get_number() == 1100000:
        print(operator)

    if operator == '!' and (a.get_number() == digit or a.is_digit):
        return '(' + str(a.get_number()) + '!)'

    if operator == '!' and a.get_number() != digit and not a.is_digit:
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + '!)'
    #print(a.is_digit, a.get_number(), b.is_digit(), b.get_number())

    #if not a:
    #    print("NONE")

    if (a.get_number() == digit or a.is_digit) and b.get_number() != digit and not b.is_digit:
        return '(' + str(a.get_number()) + operator + get_term(b.child1, b.get_operator(), b.child2) + ')'

    if (b.get_number() == digit or b.is_digit) and a.get_number() != digit and not a.is_digit:
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + operator + str(b.get_number()) + ')'

    if b.get_number() != digit and not b.is_digit and a.get_number() != digit and not a.is_digit:
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + operator + get_term(b.child1, b.get_operator(),
                                                                                          b.child2) + ')'
    if (b.get_number() == digit or b.is_digit) and (a.get_number() == digit or a.is_digit):
        return '(' + str(a.get_number()) + operator + str(b.get_number()) + ')'


print("Geben Sie die zu berechnende Jahreszahl ein:")
target_number = int(input())
print("Geben sie eine Ziffer ein:")
digit = int(input())
time1 = timer()
#for digit in range(1, 10):
if digit == target_number or len(re.findall(str(digit), str(target_number))) == (len(str(target_number)) / (len(str(digit)))):
    print(target_number)
    print("Number of Digits:")
    print(int(len(str(target_number)) / (len(str(digit)))))
else:
    operations = ['^', '/', '*', '+', '-']
    res = create_numbers(target_number, digit, operations)
    print(get_term(res.child1, res.operator, res.child2))

print("In " + str(((timer() - time1))) + " Sekunden")
