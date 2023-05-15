from .simp import HAS_CALLED_SIMP_FUNCTIONS

def sumofdigits(number):
    if not HAS_CALLED_SIMP_FUNCTIONS[0]:
        return print("Please use simp function to allow the use of a comp function")

    sum_of_nums = 0
    number = str(number)
    for digit in number:
        sum_of_nums += int(digit)
    return sum_of_nums

def ispal(number): 
    if not HAS_CALLED_SIMP_FUNCTIONS[0]:
        return print("Please use simp function to allow the use of a comp function")
    number = str(number)
    if number == number[::-1]:
        return True
    return False
