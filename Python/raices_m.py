from tabulate import tabulate
import math
import sympy as sp
import re


def conversion(expr):
    expr = re.sub(r'(?<!\w)e', 'E', expr)
    expr = re.sub(r'\bln\b', 'log', expr)
    sympy_expr = sp.sympify(expr)
    converted_expr = str(sympy_expr).replace('E', 'math.exp(1)')
    converted_expr = converted_expr.replace('exp(', 'math.exp(')
    converted_expr = converted_expr.replace('log(', 'math.log(')

    return converted_expr

def multiple_roots(function_str, derivative_1_str, derivative_2_str, initial_guess, tolerance, max_iterations, error_type):
    
    function_str = conversion(function_str)
    derivative_1_str = conversion(derivative_1_str)
    derivative_2_str = conversion(derivative_2_str)
    
    def evaluate_function(x):
        return eval(function_str)
    def evaluate_derivative_1(x):
        return eval(derivative_1_str)
    def evaluate_derivative_2(x):
        return eval(derivative_2_str)
    
    previous_root = initial_guess
    previous_function_value = evaluate_function(previous_root)
    iteration_count = 0
    results_matrix = []

    while True:

        derivative_1_value = evaluate_derivative_1(previous_root)
        derivative_2_value = evaluate_derivative_2(previous_root)
        
        denominator = (derivative_1_value)**2 - previous_function_value * derivative_2_value
        if denominator == 0:
            print("Error: División por 0")
            break
        
        current_root = previous_root - previous_function_value * derivative_1_value / denominator
        absolute_error=abs(current_root-previous_root)
        relative_error=absolute_error/current_root
        current_function_value = evaluate_function(current_root)
        
        if error_type=="rela":
            if previous_root != 0:
                error=absolute_error/current_root
            else:
                print("Error: División por 0")
                error= float('inf')
                relative_error=float('inf')
        
        else:
            error=absolute_error
        results_matrix.append([iteration_count, previous_root, previous_function_value, derivative_1_value, derivative_2_value, absolute_error, relative_error])
        previous_root = current_root
        previous_function_value = current_function_value
        iteration_count += 1
        if error < tolerance or iteration_count >= max_iterations:
            break

    return results_matrix

function_str = input("Ingresa la función f(x): ")
derivative_1_str = input("Ingresa la primera derivada df(x): ")
derivative_2_str = input("Ingresa la segunda derivada d2f(x): ")
initial_guess = float(input("Ingresa la estimación inicial x0: "))
tolerance = float(input("Ingresa la tolerancia: "))
max_iterations = int(input("Ingresa el número máximo de iteraciones: "))
error_type = input("Ingresa el tipo de error (rela para relativo o abs para absoluto): ")

results = multiple_roots(function_str, derivative_1_str, derivative_2_str, initial_guess, tolerance, max_iterations, error_type)

print(tabulate(results, headers=["Iteración", "x", "f(x)", "df(x)", "d2f(x)", "Error absoluto", "Error relativo"], tablefmt="fancy_grid"))