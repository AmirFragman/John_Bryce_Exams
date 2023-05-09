# boolian function to make sure the functions cant be called if one of the simp functions did not get called
# from .comp import HAS_CALLED_SIMP_FUNCTIONS

# function asking for two numbers and prints its sum
def sum_of_nums():
    # global HAS_CALLED_SIMP_FUNCTIONS
    # HAS_CALLED_SIMP_FUNCTIONS = True

    num1 = input("Please enter first number: ")
    if not num1.isdigit():
        num1 = input("Please enter a number and not letters: ")
    int_num1 = int(num1)

    num2 = input("Please enter second number: ")
    if num2.isdigit() == False:
        num2 = input("Please enter a number and not letters: ")
    int_num2 = int(num2)

    return print("The sum of your chosen numbers is: " + str(int_num1 + int_num2))
    

# function asking for two numbers and prints its subtraction   
def subtraction_of_nums():
    # global HAS_CALLED_SIMP_FUNCTIONS
    # HAS_CALLED_SIMP_FUNCTIONS = True
    num1 = input("Please enter first number: ")
    if not num1.isdigit():
      num1 = input("Please enter a number and not letters: ")
    int_num1 = int(num1)

    num2 = input("Please enter second number: ")
    if num2.isdigit() == False:
        num2 = input("Please enter a number and not letters: ")
    int_num2 = int(num2)

    return print("The subtraction of your chosen numbers is: " + str(int_num1 - int_num2))
