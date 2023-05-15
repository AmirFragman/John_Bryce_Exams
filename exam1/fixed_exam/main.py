import tools.col as col
from tools.numbers import simp
from tools.numbers import comp

it1 = ["Amir", "Uri", "Yotam", "Tamar"]
it2 = ["Jenny", "Christy", "Monica", "Vicky"]
num1 = 10
num2 = 5
number = 1221

if __name__ == "__main__":
    print(simp.sum_of_nums(num1, num2))
    print(simp.subtraction_of_nums(num1, num2))
    print(col.myzip(it1, it2))
    print(comp.sumofdigits(number))
    print(comp.ispal(number))