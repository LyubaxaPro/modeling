from prettytable import PrettyTable
from itertools import islice

COUNT = 10000
m = 2. ** 31
a = 1664525
c = 1013904223

theor_koef_one_digit = {'1': 2.088, '5': 3.325, '25': 5.899, '50': 8.343, '75': 11.39, '95': 16.92, '99': 21.67}
theor_koef_two_digits = {'1': 60.93, '5': 68.25, '25': 79.68, '50': 88.33, '75': 97.60, '95': 112.02, '99': 122.94}
theor_koef_three_digits = {'1': 803.31, '5': 830.41, '25': 870.05, '50': 898.33, '75': 927.23, '95': 969.86, '99': 1000.57}
theor_koefs = {'one_digit': theor_koef_one_digit, 'two_digits': theor_koef_two_digits, 'three_digits': theor_koef_three_digits}

class RandomGenerator:
    def __init__(self):
        self.current = 10

    def get_random_number(self, low, high):
        self.current = (a * self.current + c) % m
        result = int(low + self.current % (high - low))
        return result

def table_rand():
    numbers = set()
    with open('digits.txt') as file:
        line_num = 0
        lines = islice(file, line_num, None)
        for l in lines:
            numbers.update(set(l.split(" ")[1:-1]))
            line_num += 1
            if len(numbers) >= 3 * COUNT + 1:
                break
        numbers.remove("")
        numbers = list(numbers)[:3 * COUNT]
    one_digit = [int(i) % 10 for i in numbers[:COUNT]]
    two_digits = [int(i) % 90 + 10 for i in numbers[COUNT:COUNT * 2]]
    three_digits = [int(i) % 900 + 100 for i in numbers[COUNT * 2:3 * COUNT]]
    return one_digit, two_digits, three_digits


def alg_rand():
    random = RandomGenerator()
    one_digit = [random.get_random_number(0, 10) for i in range(COUNT)]
    two_digits = [random.get_random_number(10, 100) for i in range(COUNT)]
    three_digits = [random.get_random_number(100, 1000) for i in range(COUNT)]
    return one_digit, two_digits, three_digits


def calc_hi(arr, start, end):
    n = len(arr)
    tab = [0 for i in range(start + end)]
    for i in range(n):
        tab[arr[i]] += 1
    s = 0
    for i in tab:
        s += i * i
    return s * (end - start) / n - n

def check_with_criterion(prac_koef, digit_str):
    if prac_koef < theor_koefs[digit_str]['1'] or prac_koef > theor_koefs[digit_str]['99']:
        return "Числа не случайные"

    if prac_koef >= theor_koefs[digit_str]['1'] and prac_koef <= theor_koefs[digit_str]['5']:
        return "Числа подозрительные"

    if prac_koef <= theor_koefs[digit_str]['99'] and prac_koef >= theor_koefs[digit_str]['95']:
        return "Числа подозрительные"
    return "Числа случайные"
def main():
    numbers = [i for i in range(10)]
    table_tbl = PrettyTable()
    one_tbl, two_tbl, three_tbl = table_rand()

    table_tbl.add_column("№", numbers)
    table_tbl.add_column('1 разряд', one_tbl[:10])
    table_tbl.add_column('2 разряда', two_tbl[:10])
    table_tbl.add_column('3 разряда', three_tbl[:10])

    one_alg, two_alg, three_alg = alg_rand()
    table_tbl.add_column('1 разряд', one_alg[:10])
    table_tbl.add_column('2 разряда', two_alg[:10])
    table_tbl.add_column('3 разряда', three_alg[:10])

    koef_tbl_one = calc_hi(one_tbl, 0, 10)
    koef_tbl_two = calc_hi(two_tbl, 10, 100)
    koef_tbl_three = calc_hi(three_tbl, 100, 1000)
    koef_alg_one = calc_hi(one_alg, 0, 10)
    koef_alg_two = calc_hi(two_alg, 10, 100)
    koef_alg_three = calc_hi(three_alg, 100, 1000)

    table_tbl.add_row(['Коэффициент', koef_tbl_one, koef_tbl_two, koef_tbl_three, koef_alg_one, koef_alg_two, koef_alg_three])

    table_tbl.add_row(['Критерий',
                      check_with_criterion(koef_tbl_one, 'one_digit'),
                      check_with_criterion(koef_tbl_two, 'two_digits'),
                      check_with_criterion(koef_tbl_three, 'three_digits'),
                      check_with_criterion(koef_alg_one, 'one_digit'),
                      check_with_criterion(koef_alg_two, 'two_digits'),
                      check_with_criterion(koef_alg_three, 'three_digits')])
    print("\t\t\t                    Табличный метод\t\t\t\t\t                                    Алгоритмический метод")

    print(table_tbl)

    flag = input("Введите 1 если хотите проанализировать свою последовательность: ")
    if flag == '1':
        print("Выберите размерность вводимой последовательности")
        digit_str = input("Одноразрядные - введите 1, двухразрядные - введите 2, трехразрядные - введите 3: ")
        arr = []
        if digit_str in ['1', '2', '3']:
            print("Введите последовательность чисел (через пробел)")
            arr_str = list(input().split())
            for digit in arr_str:
                if len(digit) != int(digit_str):
                    print("Некорректная разрядность")
                    return
                try:
                    d = int(digit)
                except:
                    print("Некорректное значение")
                    return
                arr.append(d)
            if digit_str == '1':
                hi_koef = calc_hi(arr, 0, 10)
            elif digit_str == '2':
                hi_koef = calc_hi(arr, 10, 100)
            else:
                hi_koef = calc_hi(arr, 100, 1000)
            print("Коэффициент: ", hi_koef)
            s = ['one_digit', 'two_digits', 'three_digits']
            print(check_with_criterion(hi_koef, s[int(digit_str) - 1]))
        else:
            print("Некорректный ввод")
            return

if __name__ == '__main__':
    main()
