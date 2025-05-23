from tabulate import tabulate
import numpy as np
import math

def fixed_point_iteration(g, x0, tolerance, max_iterations, error_type="abs"):
    """
    Encuentra la raíz de una función g utilizando el método de iteración de punto fijo.

    Args:
        g (función): La función para encontrar el punto fijo de.
        x0 (float): La estimación inicial.
        tolerance (float): La tolerancia para la raíz.
        max_iteraciones (int): El número máximo de iteraciones.
        tipo_error (str): El tipo de error a utilizar («abs» para absoluto, «rel» para relativo).

    Devuelve:
        tupla: Una tupla que contiene el valor final de x, el valor de g(x), el número de iteraciones y la matriz de iteraciones.
    """
    x_current = x0
    iteration_count = 0
    iteration_data = []

    while iteration_count < max_iterations:
        x_next = g(x_current)
        
        if error_type == "abs":
            error = abs(x_next - x_current)
        elif error_type == "rel":
            if x_next != 0:
                error = abs((x_next - x_current) / x_next)
            else:
                print("Error: División por 0 en el cálculo del error relativo.")
                return x_current, g(x_current), iteration_count, iteration_data
        else:
            print("Error: Tipo de error no válido. Escoge 'abs' o 'rel'.")
            return x_current, g(x_current), iteration_count, iteration_data

        iteration_data.append([iteration_count, x_current, g(x_current), error])

        if error < tolerance:
            return x_next, g(x_next), iteration_count, iteration_data

        x_current = x_next
        iteration_count += 1

    print("Alerta: Número máximo de iteraciones alcanzado.")
    return x_current, g(x_current), iteration_count, iteration_data


if __name__ == '__main__':
    function_str = input("Ingresa la función g(x) (e.g., math.exp(-x)): ")
    x0 = float(input("Ingresa la estimación inicial x0: "))
    tolerance = float(input("Ingresa la tolerancia: "))
    max_iterations = int(input("Ingresa el número máximo de iteraciones: "))
    error_type = input("Ingresa el tipo de error ('abs' para absoluto, 'rel' para relativo): ")

    def g(x):
        return eval(function_str)

    if tolerance <= 0:
        print("Error: La tolerancia debe ser un número positivo.")
        exit()
    if max_iterations <= 0:
        print("Error: El número máximo de iteraciones debe ser un número positivo.")
        exit()

    x, gx, iteration_count, iteration_data = fixed_point_iteration(g, x0, tolerance, max_iterations, error_type)

    if iteration_count > 0:
        print(tabulate(iteration_data, headers=["Iteration", "x_current", "g(x_current)", "Error"], tablefmt="fancy_grid"))
        print(f"\nPunto fijo encontrado: x = {x}, g(x) = {gx} después de {iteration_count} iteraciones.")
    else:
        print("\nNo se ha encontrado ningún punto fijo dentro de la tolerancia y las iteraciones máximas dadas.")