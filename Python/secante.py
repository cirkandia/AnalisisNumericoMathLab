import math
from tabulate import tabulate
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

def secante():
    function_str = input("Ingresa la función f(x): ")
    x0 = float(input("Ingresa la estimación inicial x0: "))
    x1 = float(input("Ingresa la estimación inicial x1: "))
    tolerance = float(input("Ingresa la tolerancia: "))
    max_iterations = int(input("Ingresa el número máximo de iteraciones: "))

    f = conversion(function_str)

    def evaluate_expression(x):
        return eval(f)

    # Initial values
    previous_x = x0
    current_x = x1
    previous_f = evaluate_expression(previous_x)
    current_f = evaluate_expression(current_x)
    iteration_number = 0
    results_matrix = []
    absolute_error = "-"
    relative_error = "-"

    results_matrix.append([iteration_number, previous_x, previous_f, absolute_error, relative_error])

    iteration_number = 1
    results_matrix.append([iteration_number, current_x, current_f, absolute_error, relative_error])

    while iteration_number <= max_iterations:
        denominator = current_f - previous_f
        if denominator == 0:
            print("Error: División por 0!")
            break

        next_x = current_x - current_f * (current_x - previous_x) / denominator
        next_f = evaluate_expression(next_x)

        absolute_error = abs(next_x - current_x)
        if next_x != 0:
            relative_error = abs(next_x - current_x) / abs(next_x)
        else:
            relative_error = float('inf')

        results_matrix.append([iteration_number + 1, next_x, next_f, absolute_error, relative_error])

        if absolute_error < tolerance:
            print(f"El método secante convergió después de {iteration_number} iteraciones.")
            break

        previous_x = current_x
        current_x = next_x
        previous_f = current_f
        current_f = next_f

        iteration_number += 1

    else:
        print("El método de la secante no convergió en el número máximo de iteraciones.")

    headers = ["Iteración", "x", "f(x)", "Error absoluto", "Error relativo"]
    table = tabulate(results_matrix, headers=headers, tablefmt="grid")
    print(table)

# Ejemplo de uso:
secante()