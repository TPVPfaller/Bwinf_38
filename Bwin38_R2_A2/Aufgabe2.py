from timeit import default_timer as timer
import sys

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
        return set(str(self.number)).pop() == str(digit) and len(set(str(self.number))) == 1

    def __add__(self, other):
        return self.number + other.number

    def __sub__(self, other):
        return self.number - other.number

    def __mul__(self, other):
        return self.number * other.number

    def __truediv__(self, other):
        return self.number / other.number


def factorial(n):
    if n == 0:
        return 1
    if n == 1:
        return n
    else:
        return n * factorial(n - 1)


def create_numbers(target_number, digit, operations):
    rows = [[Expression(None, digit, None, None)]]
    rows[0].append(Expression('!', factorial(digit), rows[0][0], None))
    n = 1
    maximum = 10**9
    found_numbers = set()
    found_numbers.add(digit)
    found_numbers.add(factorial(digit))
    while target_number not in found_numbers:
        rows.append([Expression(None, rows[n - 1][0].get_number() * 10 + digit, None, None)])
        rows[-1].append(Expression('/', 1, rows[0][0], rows[0][0]))
        found_numbers.add(rows[n - 1][0].get_number() * 10 + digit)
        found_numbers.add(1)
        for e in rows[n - 1]:
            result = e.get_number()
            count = 0
            while result < 10:
                result = factorial(result)
                if isinstance(result, int) and result > 0 and result not in found_numbers:
                    if count > 0:
                        rows[n - 1].append(Expression('!', result, rows[n-1][-1], None))
                    else:
                        rows[n-1].append(Expression('!', result, e, None))
                    found_numbers.add(result)
                count += 1
                if result <= 2:
                    break
        n1 = 0
        n2 = n - 1
        r = []
        while not n2 < n1:
            for i in rows[n1]:
                for j in rows[n2]:
                    for k in operations:
                        reversed = False
                        calc = True
                        num1 = i.get_number()
                        num2 = j.get_number()

                        if k == '+':
                            result = num1 + num2
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
                            if num1 == 1 or num2 == 1:
                                continue
                            if num1 > num2:
                                result = num1 / num2
                            elif num1 < num2:
                                result = num2 / num1
                                reversed = True
                            else:
                                continue
                            if result > maximum:
                                continue
                            if result % 1 == 0:
                                result = int(result)
                        elif k == '^':
                            result = 1
                            p = num2
                            b = num1
                            if p < 9 and b < 10:
                                while p:
                                    if p & 0x1:
                                        result *= b
                                    b *= b
                                    p >>= 1
                                    if result > sys.maxsize:
                                        calc = False
                                        break
                            else:
                                calc = False
                        if isinstance(result, int) and result > 0 and calc and result not in found_numbers:
                            if reversed:
                                rows[n].append(Expression(k, result, j, i))
                            else:
                                rows[n].append(Expression(k, result, i, j))
                            found_numbers.add(result)
                        #else:
                        #    r.append(result)
                        if result == target_number:
                            print("Number of Digits:")
                            print(len(rows))
                            return rows[n][-1]
            n1 += 1
            n2 -= 1
            if n2 == n - 3 and n1 != n2:
                break

        #print("n = " + str(n) + ":")

        r.sort()
        #print(r)
        n += 1


def get_term(a, operator, b):
    if operator == '!' and (a.get_number() == digit or a.same_digits()):
        return '(' + str(a.get_number()) + '!)'

    if operator == '!' and a.get_number() != digit and not a.same_digits():
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + '!)'

    if (a.get_number() == digit or a.same_digits()) and b.get_number() != digit and not b.same_digits():
        return '(' + str(a.get_number()) + operator + get_term(b.child1, b.get_operator(), b.child2) + ')'

    if (b.get_number() == digit or b.same_digits()) and a.get_number() != digit and not a.same_digits():
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + operator + str(b.get_number()) + ')'

    if b.get_number() != digit and not b.same_digits() and a.get_number() != digit and not a.same_digits():
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + operator + get_term(b.child1, b.get_operator(),
                                                                                          b.child2) + ')'
    if (b.get_number() == digit or b.same_digits()) and (a.get_number() == digit or a.same_digits()):
        return '(' + str(a.get_number()) + operator + str(b.get_number()) + ')'


print("Geben sie die zu berechnende Jahreszahl ein:")
target_number = int(input())
#print("Geben sie eine Ziffer ein:")
#digit = int(input())
count = 1
time1 = timer()
#if target_number == digit:
#    print(target_number)

operations = ['^', '+', '-', '*', '/']
for digit in range(1, 10):
    res = create_numbers(target_number, digit, operations)
    print(get_term(res.child1, res.operator, res.child2))
print("In " + str(((timer() - time1)) / count) + " Sekunden")
