import numpy as np
def bisection_method(FUN, init_lower, init_upper, target_value, tol, max_iterations=250):
    
    # A function that computes the input value x such that |FUN(x) - target_value|<tol using a binary search.

    # Method is guaranteed to work eventually if the init_lower < true root < init_upper, and the function is continuous.
    counter = 0
    # Error detection
    if (FUN(init_lower)-target_value) * (FUN(init_upper)-target_value)>0:
        return("No change of sign in interval")

    # Running until it reaches the maximum number of iterations or until the function's value is within tol of the target.
    midpoint = (init_lower + init_upper)/2
    while np.abs(FUN(midpoint) - target_value) > tol and counter < max_iterations:
        midpoint = (init_lower + init_upper)/2
        # Check which half of the interval the root is in
        if (FUN(init_lower)-target_value)* (FUN(midpoint)-target_value)<0:
            init_upper = midpoint
        else:
            init_lower = midpoint
        counter+=1
    
    return(midpoint, counter)

def example_polynomial(x):
    return(100*x**5 - 4*x**3 + x-1)

#Testing
init_lower = 0
init_upper = 100
target_value = 13.49546
max_iterations = 50

for i in range(8):
    acceptable_error = 10**(-1-i)
    root, iterations = bisection_method(example_polynomial,init_lower, init_upper, target_value, acceptable_error)
    if abs(example_polynomial(root) - target_value) < acceptable_error:
        print(f"Error less than 10^({-1-i}) achieved in {iterations} steps")
    else:
        print(f"Method failed to converge in {max_iterations} steps")