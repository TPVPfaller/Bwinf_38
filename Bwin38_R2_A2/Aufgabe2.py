from timeit import default_timer as timer
import sys
import math

class Expression:

    def __init__(self, operator, number, child1, child2):
        self.operator = operator
        self.number = number
        self.child1 = child1
        self.child2 = child2

    def get_number(self):
        return self.number

    def get_operator(self):
        return self.operator

    def same_digits(self):
        #print(''.join(set(str(self.number))))
        return (set(str(self.number))) == set(str(digit)) and len(set(str(self.number))) == len(set(str(digit)))

    def __add__(self, other):
        return self.number + other.number

    def __sub__(self, other):
        return self.number - other.number

    def __mul__(self, other):
        return self.number * other.number

    def __truediv__(self, other):
        return self.number / other.number


def create_numbers(target_number, digit, operations):
    rows = [[Expression(None, digit, None, None)]]
    found_numbers = set()
    if digit < 14:
        result = math.factorial(digit)
        rows[0].append(Expression('!', result, rows[0][0], None))
        found_numbers.add(result)
    n = 1
    maximum = 10**10
    found_numbers.add(digit)
    while n < 40:
        result = int(str(rows[n - 1][0].get_number()) + str(digit))
        if result < maximum:
            rows.append([Expression(None, result, None, None)])
            found_numbers.add(result)
        else:
            rows.append([])
        if n == 2 and digit != 1:
            rows[-1].append(Expression('/', 1, rows[0][0], rows[0][0]))
            found_numbers.add(1)

        for e in rows[n - 1]:
            result = e.get_number()
            if result <= 2:
                continue
            count = 0
            while result < 10:
                result = math.factorial(result)
                if result > maximum:
                    break
                if isinstance(result, int) and result not in found_numbers:

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
                        calc = True
                        num1 = i.get_number()
                        num2 = j.get_number()
                        if num1 > maximum or num2 > maximum:
                            print(num1, num2)
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
                                        calc = False
                                        break
                            else:
                                calc = False

                        if result not in found_numbers and isinstance(result, int) and result < maximum and calc:
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
            if n2 == n - 3 and n1 == n2:
                break
        n += 1


def get_term(a, operator, b):

    if operator == '!' and (a.get_number() == digit or a.same_digits()):
        return '(' + str(a.get_number()) + '!)'

    if operator == '!' and a.get_number() != digit and not a.same_digits():
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + '!)'
    #print(a.same_digits, a.get_number(), b.same_digits(), b.get_number())

    #if not a:
    #    print("NONE")

    if (a.get_number() == digit or a.same_digits()) and b.get_number() != digit and not b.same_digits():
        return '(' + str(a.get_number()) + operator + get_term(b.child1, b.get_operator(), b.child2) + ')'

    if (b.get_number() == digit or b.same_digits()) and a.get_number() != digit and not a.same_digits():
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + operator + str(b.get_number()) + ')'

    if b.get_number() != digit and not b.same_digits() and a.get_number() != digit and not a.same_digits():
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + operator + get_term(b.child1, b.get_operator(),
                                                                                          b.child2) + ')'
    if (b.get_number() == digit or b.same_digits()) and (a.get_number() == digit or a.same_digits()):
        return '(' + str(a.get_number()) + operator + str(b.get_number()) + ')'


print("Geben Sie die zu berechnende Jahreszahl ein:")
target_number = int(input())
print("Geben sie eine Ziffer ein:")
digit = int(input())
count = 1
if digit == target_number or ((set(str(target_number))) == set(str(digit)) and len(set(str(target_number))) == 1):
    print(target_number)
else:
    time1 = timer()
    operations = ['^', '+', '-', '*', '/']
    #for digit in range(1, 10):
    res = create_numbers(target_number, digit, operations)
    print(get_term(res.child1, res.operator, res.child2))
    print("In " + str(((timer() - time1)) / count) + " Sekunden")
