# boolean function to make sure the functions cant be called if one of the simp functions did not get called
HAS_CALLED_SIMP_FUNCTIONS = [False]

# function asking for two numbers and prints its sum
def sum_of_nums(num1, num2):
    HAS_CALLED_SIMP_FUNCTIONS[0] = True

    return num1 + num2
    

# function asking for two numbers and prints its subtraction   
def subtraction_of_nums(num1, num2):
    HAS_CALLED_SIMP_FUNCTIONS[0] = True

    return num1 - num2
