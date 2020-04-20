from timeit import default_timer as timer
import re
import math
import sys


class Expression:

    def __init__(self, operator, number, child1, child2, is_digit=False):
        self.operator = operator
        self.number = number
        self.child1 = child1
        self.child2 = child2
        self.is_digit = is_digit


def optimize_digits(target_number, digit, operations):
    found_numbers = set()
    decimal_places = 3
    rows = [[Expression(None, digit, None, None, True)]]
    if target_number == 0:
        rows[0].append(Expression('-', 0, rows[0][0], rows[0][0]))
        return rows[0][1], 2
    if digit < 14:
        result = math.factorial(digit)
        rows[0].append(Expression('!', result, rows[0][0], None))
        found_numbers.add(result)
        if result == target_number:
            return rows[0][1], len(rows)
    found_numbers.add(digit)

    exponent = 7
    if digit > 9:
        exponent = 12
    maximum = 10 ** exponent  # Performance depends on this number
    for n in range(1, 30):  # n+1 := number of digits containing a term
        i = n+1
        sys.stdout.write("\rBerechnet gerade für n = %i" % i)
        sys.stdout.flush()

        if rows[n - 1][0].is_digit:
            result = int(str(rows[n - 1][0].number) + str(digit))  # Add number containing the only the digit
            # multiple times
            if result < maximum:
                rows.append([Expression(None, result, None, None, True)])
                found_numbers.add(result)
            else:
                rows.append([])
        else:
            rows.append([])

        if n == 1 and digit != 1:  # digit / digit
            rows[-1].append(Expression('/', 1, rows[0][0], rows[0][0]))
            found_numbers.add(1)
            if 1 == target_number:
                return rows[-1][-1], 2

        for e in rows[n - 1]:
            result = e.number
            if result <= 2 or result % 1 != 0:
                continue
            count = False
            while result <= 10:
                result = math.factorial(int(result))
                if result <= 2:
                    break
                if result not in found_numbers:
                    if count:
                        rows[n - 1].append(Expression('!', result, rows[n - 1][-1], None))
                    else:
                        rows[n - 1].append(Expression('!', result, e, None))
                    found_numbers.add(result)
                    if result == target_number:
                        return rows[n - 1][-1], len(rows) - 1
                count = True

        n1 = 0
        n2 = n - 1
        while not n2 < n1:
            for i in rows[n1]:
                num1 = i.number
                for j in rows[n2]:
                    num2 = j.number
                    for k in operations:  # Zahlen mit allen Rechenarten kombinieren
                        reversed = False

                        if k == '+':
                            result = num1 + num2
                            if result > maximum:
                                continue
                            if result % 1 == 0:  # checking if number has a decimal place like .0
                                result = int(result)
                            elif len(str(result).split(".")[1]) > decimal_places:
                                continue
                        elif k == '-':
                            if num1 > num2:
                                result = num1 - num2
                            elif num2 > num1:
                                result = num2 - num1
                                reversed = True
                            else:
                                continue
                            if not 0.001 < result < maximum:
                                continue
                            if result % 1 == 0:  # checking if number has a decimal place like .0
                                result = int(result)
                            elif len(str(result).split(".")[1]) > decimal_places:
                                continue
                        elif k == '*':
                            result = num1 * num2
                            if not 0.001 < result < maximum:
                                continue
                            if result % 1 == 0:  # checking if number has a decimal place like .0
                                result = int(result)
                            elif len(str(result).split(".")[1]) > decimal_places:
                                continue
                        elif k == '/':
                            if num1 == 0:
                                continue
                            result = num2 / num1
                            if not 0.001 < result < maximum:
                                result = None
                            elif result % 1 == 0:  # checking if number has a decimal place like .0
                                result = int(result)
                            elif len(str(result).split(".")[1]) > decimal_places:
                                result = None
                            if result not in found_numbers and result is not None:
                                rows[n].append(Expression(k, result, j, i))
                                found_numbers.add(result)
                                if result == target_number:
                                    return rows[n][-1], len(rows)
                            if num2 == 0:
                                continue
                            result = num1 / num2
                            if not 0.001 < result < maximum:
                                continue
                            if result % 1.0 == 0:  # checking if number has a decimal place like .0
                                result = int(result)
                            elif len(str(result).split(".")[1]) > decimal_places:
                                continue
                        elif k == '^':
                            result = power(num1, num2, exponent)

                            if result is None or not 0.001 < result < maximum:
                                pass
                            else:
                                if result % 1 == 0:  # checking if number has a decimal place like .0
                                    result = int(result)
                                elif len(str(result).split(".")[1]) > decimal_places:
                                    result = None
                                if result not in found_numbers and result is not None:
                                    rows[n].append(Expression(k, result, i, j))
                                    found_numbers.add(result)
                                    if result == target_number:
                                        return rows[n][-1], len(rows)
                            result = power(num2, num1, exponent)
                            if result is None:
                                continue
                            if not 0.001 < result < maximum:
                                continue
                            if result % 1 == 0:  # checking if number has a decimal place like .0
                                result = int(result)
                            elif len(str(result).split(".")[1]) > decimal_places:
                                continue
                            reversed = True

                        if result not in found_numbers:
                            if reversed:
                                rows[n].append(Expression(k, result, j, i))
                            else:
                                rows[n].append(Expression(k, result, i, j))
                            found_numbers.add(result)
                            if result == target_number:
                                return rows[n][-1], len(rows)
            n1 += 1
            n2 -= 1

    sys.exit("Program interrupted because number of combinated digtis is greater than 30")


def power(p, b, exponent):
    if p <= exponent and b <= 10:
        result = math.pow(b, p)
    else:
        return
    return result


def optimize_operators_and_digits(target_number, digit, operations):
    found_numbers = set()
    rows = [[Expression(None, digit, None, None, True)]]
    if target_number == 0:
        rows[0].append(Expression('-', 0, rows[0][0], rows[0][0]))
        return rows[0][1], 2
    if digit < 14:
        result = math.factorial(digit)
        rows[0].append(Expression('!', result, rows[0][0], None))
        found_numbers.add(result)
        if result == target_number:
            return rows[0][1], len(rows)
    found_numbers.add(digit)

    exponent = 7
    if digit > 9:
        exponent = 12
    maximum = 10 ** exponent  # Performance depends on this number
    for n in range(1, 30):  # n+1 := amount of digits containing a term
        i = n + 1
        sys.stdout.write("\rBerechnet gerade für n = %i" % i)
        sys.stdout.flush()
        if rows[n - 1][0].is_digit:
            result = int(str(rows[n - 1][0].number) + str(digit))  # Add number containing the only the digit
            # multiple times
            if result < maximum:
                rows.append([Expression(None, result, None, None, True)])
                found_numbers.add(result)
            else:
                rows.append([])
        else:
            rows.append([])

        if n == 1 and digit != 1:  # digit / digit
            rows[-1].append(Expression('/', 1, rows[0][0], rows[0][0]))
            found_numbers.add(1)
            if 1 == target_number:
                return rows[-1][-1], 2

        for e in rows[n - 1]:  # calculate factorial of numbers from last row
            result = e.number
            if result <= 2:
                continue
            count = False
            while result <= 10:
                result = math.factorial(result)
                if result not in found_numbers:
                    if count:
                        rows[n - 1].append(Expression('!', result, rows[n - 1][-1], None))
                    else:
                        rows[n - 1].append(Expression('!', result, e, None))
                    found_numbers.add(result)
                    if result == target_number:
                        return rows[n - 1][-1], len(rows) - 1
                count = True
        n1 = 0
        n2 = n - 1
        while not n2 < n1:
            for i in rows[n1]:
                num1 = i.number
                for j in rows[n2]:
                    num2 = j.number
                    for k in operations:  # Combine with all operations
                        reversed = False
                        if k == '+':
                            result = num1 + num2
                            if result > maximum:
                                continue
                        elif k == '-':  # (bigger number) - (smaller number)
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
                        elif k == '/':  # (bigger number) / (smaller number)
                            if num1 <= 1 or num2 <= 1 or num1 == num2:
                                continue
                            if num1 > num2:
                                result = num1 / num2
                            else:
                                result = num2 / num1
                                reversed = True
                            if result % 1 == 0:
                                result = int(result)
                            else:
                                continue
                        elif k == '^':
                            result = power(num1, num2, exponent)
                            if result is None:
                                pass
                            elif result not in found_numbers:
                                rows[n].append(Expression(k, result, i, j))
                                found_numbers.add(result)
                                if result == target_number:
                                    return rows[n][-1], len(rows)
                            result = power(num2, num1, exponent)
                            if result is None:
                                continue
                            reversed = True
                        if result not in found_numbers:  # check if result is new
                            if reversed:
                                rows[n].append(Expression(k, result, j, i))
                            else:
                                rows[n].append(Expression(k, result, i, j))
                            found_numbers.add(result)
                            if result == target_number:
                                return rows[n][-1], len(rows)
            n1 += 1
            n2 -= 1
    sys.exit("Program interrupted because number of combinated digtis is greater than 30")


def get_term(a, operator, b):  # recursive conversion in mathematical Notation

    if operator == '!' and a.is_digit:
        return '(' + str(a.number) + '!)'

    if operator == '!' and not a.is_digit:
        return '(' + get_term(a.child1, a.operator, a.child2) + '!)'

    if a.is_digit and not b.is_digit:
        return '(' + str(a.number) + operator + get_term(b.child1, b.operator, b.child2) + ')'

    if b.is_digit and not a.is_digit:
        return '(' + get_term(a.child1, a.operator, a.child2) + operator + str(b.number) + ')'

    if not b.is_digit and not a.is_digit:
        return '(' + get_term(a.child1, a.operator, a.child2) + operator + get_term(b.child1, b.operator,b.child2) + ')'

    if b.is_digit and a.is_digit:
        return '(' + str(a.number) + operator + str(b.number) + ')'


# input
#print("Geben Sie die zu berechnende Jahreszahl ein: (max 3 Nachkommastellen, Dezimalzahlen mit <.> eingeben)")
#target_number = round(float(input()), 3)
amount2 = float("Inf")
for target_number in range(1000, 3000):
    if target_number % 10 == 0:
        print(target_number)
    for digit in range(1, 10):
        for optimization in ['n', 'y']:
            if target_number % 1 == 0:
                target_number = int(target_number)
            #print("Geben Sie eine Ziffer ein: (max 3 Nachkommastellen, Dezimalzahlen mit <.> eingeben)")
            #digit = round(float(input()), 3)
            if digit % 1 == 0:
                digit = int(digit)

            # checking if target_number only contains the digit
            if digit == target_number or len(re.findall(str(digit), str(target_number))) == (
                    len(str(target_number)) / (len(str(digit)))):

                amount1 = int(len(str(target_number)) / (len(str(digit))))
                amount2 = int(len(str(target_number)) / (len(str(digit))))
                term = target_number
            else:
                operations = ['^', '/', '*', '+', '-']
                if optimization == 'y':
                    res, amount1 = optimize_operators_and_digits(target_number, digit, operations)
                    term1 = get_term(res.child1, res.operator, res.child2)
                elif optimization == 'n':
                    res, amount2 = optimize_digits(target_number, digit, operations)
                    term2 = get_term(res.child1, res.operator, res.child2)
                else:
                    sys.exit("Geben Sie bitte entweder 'n' für nein oder 'y' für ja ein.")

            if optimization == 'y':
                if amount2 > amount1:
                    print("Dezimalstelle war besser")
                    print("Amount1 ", amount1)
                    print("Amount2 ", amount2)
                    print("Term1:", end=" ")
                    print(term1)
                    print("Term2:", end=" ")
                    print(term2)