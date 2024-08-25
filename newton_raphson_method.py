import numpy as np
from bisection_method_with_tol import example_polynomial
import matplotlib.pyplot as plt

def newton_raphson(FUN, deriv_FUN, init_point, target_value, tol, max_iterations=250):
    """Applying Newton Raphson Method for finding the roots"""
    current_point = init_point
    counter = 0
    function_val = FUN(current_point) - target_value
    while counter < max_iterations and abs(function_val) > tol:
        function_val = FUN(current_point) - target_value
        deriv_val = deriv_FUN(current_point)
        current_point = current_point - function_val / deriv_val
        counter +=1
    return(current_point, counter)

def example_poly_derivative(x):
    return(500*x**4 - 12*x**2 +1)

"""
init_point = 100
target_value = 13.49546
max_iterations = 35
# Test  for Newton Raphson
for i in range(8):
    acceptable_error = 10**(-1-i)
    root, iterations = newton_raphson(example_polynomial,example_poly_derivative,init_point, target_value, acceptable_error)
    if abs(example_polynomial(root) - target_value) < acceptable_error:
        print(f"Error less than 10^({-1-i}) achieved in {iterations} steps")
    else:
        print(f"Method failed to converge in {max_iterations} steps")

# Demonstrating inaccuracies in Newton Raphson Method
def tanh(x):
    e_to_pos_x = np.exp(x)
    e_to_neg_x = np.exp(-x)
    numerator = e_to_pos_x-e_to_neg_x
    denominator = e_to_pos_x+e_to_neg_x
    return numerator/denominator

def deriv_tanh(x):
    e_to_pos_x = np.exp(x)
    e_to_neg_x = np.exp(-x)
    numerator = 4
    denominator = (e_to_pos_x+e_to_neg_x)**2
    return numerator/denominator


# The true root (for a target value of 0) is 0. To show the behaviour, we start with a point a bit larger than 1
init_point = 1.15
iterations = 3

# Running the NR method and saving the points:
current_point = init_point
iterates = [init_point]*(iterations+1)
for i in range(iterations):
    function_val = tanh(current_point)
    deriv_val = deriv_tanh(current_point)
    current_point = current_point - function_val / deriv_val
    iterates[i+1] = current_point
print(iterates) #Increasing iterations causes it to diverge

x_range = 20
x_vals = np.linspace(-x_range,x_range,500)
y_vals = tanh(x_vals)

plt.plot(x_vals, y_vals, label = "tanh(x)", color = "red")

for i in range(iterations):
    x_tangent = [iterates[i], iterates[i+1]]
    y_tangent = [tanh(iterates[i]),0]
    plt.plot(x_tangent, y_tangent, color = "blue", label = "Tangnet" if i == 0 else "", linestyle='--')

for i in range(iterations + 1):
    plt.plot([iterates[i], iterates[i]], [0, np.tanh(iterates[i])], color="green", label="Function evaluations" if i == 0 else "", linestyle=':')
plt.legend()
plt.show()
"""
