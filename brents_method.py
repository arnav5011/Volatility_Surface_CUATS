import numpy as np


def conditions(s, a, b, b_prev, b_2_prev, bisect_flag, delta):
    """Condition when applying bisection method"""
    if bisect_flag:
        if abs(b - b_prev) < delta:
            return True
        if abs(s - b) > 0.5 * abs(b - b_prev):
            return True
    else:
        if abs(b_prev - b_2_prev) < delta:
            return True
        if abs(s - b) > 0.5 * abs(b_prev - b_2_prev):
            return True

    if (s - b) * (s - (3 * a + b) / 4) >= 0:
        return True
    return False

def secant_method(a, b, f_a, f_b):
    """Apply Secant method if cannot use bisection method and inverse quadratic interpolation"""
    return b - f_b * (b - a) / (f_b - f_a)

def inverse_quadratic_interp(a, b, c, f_a, f_b, f_c):
    term_1 = a * f_b * f_c / ((f_a - f_b) * (f_a - f_c))
    term_2 = b * f_a * f_c / ((f_b - f_a) * (f_b - f_c))
    term_3 = c * f_a * f_b / ((f_c - f_a) * (f_c - f_b))
    s = term_1 + term_2 + term_3
    return s

def swap(a, b):
    return b, a

def brent_method(FUN, a, b, target_value, tol_height, tol_width, delta=0.001):
    """Application of Brents Method to find roots"""
    def f(x):
        return FUN(x) - target_value

    f_a = f(a)
    f_b = f(b)
    
    if f_a * f_b >= 0:
        return f"Error: No change of sign between {a} and {b}, can't perform method."
    
    if abs(f_a) < abs(f_b):
        a, b = swap(a, b)
        f_a, f_b = swap(f_a, f_b)
    
    b_prev = a
    b_2_prev = a
    f_b_prev = f_a
    f_b_2_prev = f_a
    bisect_flag = True
    s = b
    f_s = f(s)
    while abs(f_s) > tol_height and abs(b - a) > tol_width:
        if f_b != f_b_prev and f_b != f_b_2_prev and f_b_prev != f_b_2_prev:
            s = inverse_quadratic_interp(b, b_prev, b_2_prev, f_b, f_b_prev, f_b_2_prev)
        else:
            s = secant_method(b_prev, b, f_b_prev, f_b)
        
        if conditions(s, a, b, b_prev, b_2_prev, bisect_flag, delta):
            bisect_flag = True
            s = (a + b) / 2
        else:
            bisect_flag = False
        
        f_s = f(s)
        b_2_prev = b_prev
        b_prev = b
        f_b_prev = f_b
        f_b_2_prev = f_b_prev
        
        if f_a * f_s > 0:
            a = s
            f_a = f_s
        else:
            b = s
            f_b = f_s
        
        if abs(f_a) < abs(f_b):
            a, b = swap(a, b)
            f_a, f_b = swap(f_a, f_b)
    
    return s
