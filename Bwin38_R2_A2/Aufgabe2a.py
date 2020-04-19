from timeit import default_timer as timer
import re
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
    rows = [[Expression(None, digit, None, None, True)]]
    found_numbers.add(digit)
    exponent = 7
    if target_number == 0:
        rows[0].append(Expression('-', 0, rows[0][0], rows[0][0]))
        return rows[0][1], 2
    if digit > 9:
        exponent = 12
    maximum = 10 ** exponent  # Performance depends on this number
    for n in range(1, 40):  # n := number of digits containing a term
        i = n + 1
        sys.stdout.write("\rBerechnet gerade für n = %i" % i)
        sys.stdout.flush()
        if rows[n - 1][0].is_digit:
            result = int(str(rows[n - 1][0].number) + str(digit))  # Add number containing only the digit
            # multiple times
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
            if 1 == target_number:
                return rows[-1][-1], 2
        n1 = 0
        n2 = n - 1
        while not n2 < n1:
            for i in rows[n1]:
                num1 = i.number
                for j in rows[n2]:
                    num2 = j.number
                    for k in operations:  # Combining numbers with all operations
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
                        else:  # (bigger number) / (smaller number)
                            if num1 <= 1 or num2 <= 1:
                                continue
                            if num1 > num2:
                                result = num1 / num2
                            elif num1 < num2:
                                result = num2 / num1
                                reversed = True
                            else:
                                continue
                            if result % 1 == 0:  # checking if number has a decimal place
                                result = int(result)
                            else:
                                continue
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

    sys.exit("Program interrupted because number of combinated digtis is greater than 40")


def optimize_operators_and_digits(target_number, digit, operations):
    found_numbers = set()
    rows = [[Expression(None, digit, None, None, True)]]
    if target_number == 0:
        rows[0].append(Expression('-', 0, rows[0][0], rows[0][0]))
        return rows[0][1], 3
    found_numbers.add(digit)
    if rows[0][0].number == target_number:
        return rows[0][0], len(rows)
    exponent = 7
    if digit > 9:
        exponent = 12
    maximum = 10 ** exponent  # Performance depends on this number
    for n in range(1, 70):
        i = n + 1
        sys.stdout.write("\rBerechnet gerade für n = %i" % i)
        sys.stdout.flush()
        if len(rows[n - 1]) != 0 and rows[n - 1][0].is_digit:
            result = int(str(rows[n - 1][0].number) + str(digit))
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
            if 1 == target_number:
                return rows[-1][-1], 3
        n1 = 0
        n2 = n - 2
        while not n2 < n1:
            for i in rows[n1]:
                num1 = i.number
                for j in rows[n2]:
                    num2 = j.number
                    for k in operations:  # Combining numbers with all operations
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
                        else:  # (bigger number) / (smaller number)
                            if num1 <= 1 or num2 <= 1:
                                continue
                            if num1 > num2:
                                result = num1 / num2
                            elif num1 < num2:
                                result = num2 / num1
                                reversed = True
                            else:
                                continue
                            if result % 1 == 0:  # checking if number has a decimal place
                                result = int(result)
                            else:
                                continue
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

    sys.exit("Program interrupted because the number of combinated digtis is greater than 70")


def get_term(a, operator, b):  # Rekursive Umwandlung in mathematische Notation

    if a.is_digit and not b.is_digit:
        return '(' + str(a.number) + operator + get_term(b.child1, b.operator, b.child2) + ')'

    if b.is_digit and not a.is_digit:
        return '(' + get_term(a.child1, a.operator, a.child2) + operator + str(b.number) + ')'

    if not b.is_digit and not a.is_digit:
        return '(' + get_term(a.child1, a.operator, a.child2) + operator + get_term(b.child1, b.operator,b.child2) + ')'

    if b.is_digit and a.is_digit:
        return '(' + str(a.number) + operator + str(b.number) + ')'


# output
print("Geben Sie die zu berechnende Jahreszahl ein:")
target_number = int(input())
print("Geben Sie eine Ziffer ein:")
digit = int(input())
print("Wollen Sie auch die Anzahl an Rechenzeichen optimieren? [y/n]")
optimization = input()

time1 = timer()
# checking if target_number only contains the digit
if digit == target_number or len(re.findall(str(digit), str(target_number))) == (
        len(str(target_number)) / (len(str(digit)))):

    amount = int(len(str(target_number)) / (len(str(digit))))
    term = target_number
else:
    operations = ['/', '*', '+', '-']
    if digit == 0:
        sys.exit("Not possible")
    if optimization == 'y':
        res, amount = optimize_operators_and_digits(target_number, digit, operations)
    elif optimization == 'n':
        res, amount = optimize_digits(target_number, digit, operations)
    else:
        sys.exit("Geben Sie bitte entweder n für nein oder y für ja ein.")
    term = get_term(res.child1, res.operator, res.child2)

print("")
print("Anzahl:")
print(amount)
print("Term:")
print(term)
print("In " + str(round(timer() - time1, 5)) + " Sekunden")
