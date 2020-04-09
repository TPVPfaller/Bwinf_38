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


def optimize_digits(target_number, digit, operations):
    found_numbers = set()
    rows = [[Expression(None, digit, None, None, True)]]
    if digit < 14:
        result = math.factorial(digit)
        rows[0].append(Expression('!', result, rows[0][0], None))
        found_numbers.add(result)
        if result == target_number:
            print("Anzahl an verwendeten Ziffern:")
            print(len(rows))
            print("Ergebnis:")
            return rows[0][1]
    found_numbers.add(digit)

    exponent = 7
    if digit > 9:
        exponent = 12
    maximum = 10**exponent    # Performance depends on this number
    for n in range(1, 30):    # n := number of digits containing a term
        if rows[n-1][0].is_digit:
            result = int(str(rows[n - 1][0].get_number()) + str(digit))     # Add number containing the only the digit
                                                                            # multiple times
            if result < maximum:
                rows.append([Expression(None, result, None, None, True)])
                found_numbers.add(result)
            else:
                rows.append([])
        else:
            rows.append([])

        if n == 1 and digit != 1:   #
            rows[-1].append(Expression('/', 1, rows[0][0], rows[0][0]))
            found_numbers.add(1)
        for e in rows[n - 1]:
            result = e.get_number()
            if result <= 2:
                continue
            count = False
            while result <= 10:
                result = math.factorial(result)
                if result not in found_numbers:
                    if count:
                        rows[n-1].append(Expression('!', result, rows[n-1][-1], None))
                    else:
                        rows[n-1].append(Expression('!', result, e, None))
                    if result == target_number:
                        print("Anzahl an verwendeten Ziffern:")
                        print(len(rows) - 1)
                        print("Ergebnis:")
                        return rows[n-1][-1]
                count = True
        n1 = 0
        n2 = n - 1
        while not n2 < n1:
            for i in rows[n1]:
                num1 = i.get_number()
                for j in rows[n2]:
                    num2 = j.get_number()
                    for k in operations:
                        reversed = False
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
                                print("Anzahl an verwendeten Ziffern:")
                                print(len(rows))
                                print("Ergebnis:")
                                return rows[n][-1]
            n1 += 1
            n2 -= 1
    print("Program interrupted because number of combinated digtis is greater than 30")


def optimize_operators_and_digits(target_number, digit, operations):
    found_numbers = set()
    rows = [[Expression(None, digit, None, None, True)]]
    found_numbers.add(digit)
    if rows[0][0].get_number() == target_number:
        print("Anzahl an verwendeten Ziffern + Operatoren:")
        print(len(rows))
        print("Ergebnis:")
        return rows[0][0]
    exponent = 7
    if digit > 9:
        exponent = 12
    maximum = 10**exponent    # Performance depends on this number
    for n in range(1, 70):
        if len(rows[n-1]) != 0 and rows[n-1][0].is_digit:
            result = int(str(rows[n - 1][0].get_number()) + str(digit))
            if result < maximum:
                rows.append([Expression(None, result, None, None, True)])
                found_numbers.add(result)
            else:
                rows.append([])
        else:
            rows.append([])

        if n == 2 and digit != 1:
            rows[-1].append(Expression('/', 1, rows[0][0], rows[0][0]))
            found_numbers.add(1)

        for e in rows[n - 1]:
            result = e.get_number()
            if result <= 2 or result > 10:
                continue
            result = math.factorial(result)
            if result not in found_numbers:
                rows[n].append(Expression('!', result, e, None))
                if result == target_number:
                    print("Anzahl an verwendeten Ziffern + Operatoren:")
                    print(len(rows))
                    print("Ergebnis:")
                    return rows[n][-1]
        n1 = 0
        n2 = n - 2
        while not n2 < n1:
            for i in rows[n1]:
                num1 = i.get_number()
                for j in rows[n2]:
                    num2 = j.get_number()
                    for k in operations:
                        reversed = False
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
                                print("Anzahl an verwendeten Ziffern + Operatoren:")
                                print(len(rows))
                                print("Ergebnis:")
                                return rows[n][-1]
            n1 += 1
            n2 -= 1
    print("Program interrupted because the number of combinated digtis is greater than 30")


def get_term(a, operator, b):

    if operator == '!' and a.is_digit:
        return '(' + str(a.get_number()) + '!)'

    if operator == '!' and not a.is_digit:
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + '!)'

    if a.is_digit and not b.is_digit:
        return '(' + str(a.get_number()) + operator + get_term(b.child1, b.get_operator(), b.child2) + ')'

    if b.is_digit and not a.is_digit:
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + operator + str(b.get_number()) + ')'

    if not b.is_digit and not a.is_digit:
        return '(' + get_term(a.child1, a.get_operator(), a.child2) + operator + get_term(b.child1, b.get_operator(),
                                                                                          b.child2) + ')'
    if b.is_digit and a.is_digit:
        return '(' + str(a.get_number()) + operator + str(b.get_number()) + ')'


print("Geben Sie die zu berechnende Jahreszahl ein:")
target_number = int(input())
print("Geben sie eine Ziffer ein:")
digit = int(input())
print("Wollen sie die Anzahl an Zeichen optimieren? [y/n]")
optimization = input()

time1 = timer()
if digit == target_number or len(re.findall(str(digit), str(target_number))) == (len(str(target_number)) / (len(str(digit)))):
    print("Anzahl an verwendeten Ziffern:")
    print(int(len(str(target_number)) / (len(str(digit)))))
    print("Ergebnis:")
    print(target_number)
else:
    operations = ['^', '/', '*', '+', '-']
    if optimization == 'y':
        res = optimize_operators_and_digits(target_number, digit, operations)
    elif optimization == 'n':
        res = optimize_digits(target_number, digit, operations)
    else:
        print("Geben Sie bitte entweder n für nein oder y für ja ein.")
    print(get_term(res.child1, res.operator, res.child2))

print("In " + str(((timer() - time1))) + " Sekunden")
