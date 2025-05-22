from tabulate import tabulate
import numpy as np

def biseccion(f, lower_bound, upper_bound, tolerance, max_iterations):
    """

    Encuentra una raíz de la función f en el intervalo [límite_inferior, límite_superior] utilizando el método de bisección.

    Argumentos:
        f (función): La función de la que buscar la raíz.
        límite_inferior (float): El extremo izquierdo del intervalo.
        upper_bound (float): El punto final derecho del intervalo.
        tolerancia (float): La tolerancia para la raíz.
        max_iterations (int): El número máximo de iteraciones.

    Devuelve:
        tupla: Una tupla que contiene:
            - lower_bound (float): El punto final izquierdo del intervalo.
            - upper_bound (float): El punto final derecho del intervalo.
            - iteration_count (int): El número de iteraciones realizadas.
            - matriz (lista): Una lista que contiene los detalles de la iteración.
    """

    f_a = f(lower_bound)
    f_b = f(upper_bound)

    if f_a * f_b >= 0:
        return "Error: f(lower_bound) y f(upper_bound) deben tener signos opuestos", None, None, None

    matriz = []
    midpoint = (lower_bound + upper_bound) / 2
    f_midpoint = f(midpoint)
    error = abs(upper_bound - lower_bound)
    iteration_count = 0

    matriz.append([iteration_count, lower_bound, f_a, midpoint, f_midpoint, upper_bound, f_b, error])

    while error > tolerance and iteration_count < max_iterations:
        if f_a * f_midpoint < 0:
            upper_bound = midpoint
            f_b = f(upper_bound)
        else:
            lower_bound = midpoint
            f_a = f(lower_bound)

        previous_midpoint = midpoint
        midpoint = (lower_bound + upper_bound) / 2
        f_midpoint = f(midpoint)
        error = abs(midpoint - previous_midpoint)
        iteration_count = iteration_count + 1

        matriz.append([iteration_count, lower_bound, f_a, midpoint, f_midpoint, upper_bound, f_b, error])

    return lower_bound, upper_bound, iteration_count, matriz


# Get inputs from the user
try:
    function_str = input("Ingrese la función f(x) como una expresión en Python: ")
    f = lambda x: eval(function_str)
    lower_bound = float(input("Ingresa el extremo izquierdo a: "))
    upper_bound = float(input("Ingresa el extremo derecho b: "))
    tolerance = float(input("Ingresa la tolerancia: "))
    max_iterations = int(input("Ingresa el número máximo de iteraciones: "))

    lower_bound, upper_bound, iteration_count, matriz = biseccion(f, lower_bound, upper_bound, tolerance, max_iterations)

    if lower_bound == "Error: f(lower_bound) y f(upper_bound) deben tener signos opuestos":
        print(lower_bound)
    else:
        print(tabulate(matriz, headers=["Iteración", "a", "f(a)", "pm", "f(pm)", "b", "f(b)", "Error Abs."], tablefmt="fancy_grid"))

except Exception as e:
    print(f"Error: Invalid input. Please check your function definition and numerical inputs. {e}")
