# importing a function to make sure the functions cant be called if simp one of the simp functions did not get called
from .simp import HAS_CALLED_SIMP_FUNCTIONS

# function receives a number and return the sum of its digits
def sumofdigits():
    if not HAS_CALLED_SIMP_FUNCTIONS:
        return print("Please use simp function to allow the use of a comp function")
    
    number = input("Please enter a number to return the sum of its digits: ")
    if number.isdigit() == False:
        number = input("Please enter a number and not letters: ")
    sum_of_nums = 0
    for digit in number:
        sum_of_nums += int(digit)
    return sum_of_nums

# function receives a number and returns true if is palindrome and false if isnt.
def ispal(): 
    if not HAS_CALLED_SIMP_FUNCTIONS:
        return print("Please use simp function to allow the use of a comp function")
    
    number = input("Please enter a number to check if it is palindrome: ")
        
    if number.isdigit() == False:
        number = input("Please enter a number and not letters: ")
    if number == number[::-1]:
        return True
    return False
