from tabulate import tabulate
import numpy as np
import math
import sympy as sp

def newton_method(f_str, x0, tolerance, max_iterations, error_type="abs"):
    """
    Encuentra la raíz de una función f utilizando el método de Newton.

    Argumentos:
        f_str (str): La función como string, por ejemplo "x**3 - x - 2".
        x0 (float): Estimación inicial.
        tolerance (float): Tolerancia para la raíz.
        max_iterations (int): Número máximo de iteraciones.
        error_type (str): 'abs' para error absoluto, 'rel' para relativo.

    Devuelve:
        tupla: (raíz, f(raíz), iteraciones, tabla de iteraciones)
    """
    x = sp.symbols('x')
    f_sym = sp.sympify(f_str)
    df_sym = sp.diff(f_sym, x)
    f = sp.lambdify(x, f_sym, modules=['numpy', 'math'])
    df = sp.lambdify(x, df_sym, modules=['numpy', 'math'])

    x_current = x0
    iteration_count = 0
    iteration_data = []

    while iteration_count < max_iterations:
        try:
            f_current = f(x_current)
            df_current = df(x_current)
        except ZeroDivisionError:
            print("Error: División por cero durante la evaluación de funciones.")
            return x_current, f(x_current), iteration_count, iteration_data

        if df_current == 0:
            print("Error: La derivada es 0. El método de Newton puede fallar.")
            return x_current, f(x_current), iteration_count, iteration_data

        x_next = x_current - f_current / df_current

        if error_type == "abs":
            error = abs(x_next - x_current)
        elif error_type == "rel":
            if x_next != 0:
                error = abs((x_next - x_current) / x_next)
            else:
                print("Error: División por cero en el cálculo del error relativo.")
                return x_current, f(x_current), iteration_count, iteration_data
        else:
            raise ValueError("Tipo de error inválido. Usa 'abs' o 'rel'.")

        iteration_data.append([iteration_count, x_current, f_current, df_current, error])

        if error < tolerance:
            return x_next, f(x_next), iteration_count + 1, iteration_data

        x_current = x_next
        iteration_count += 1
    return x_current, f(x_current), iteration_count, iteration_data

if __name__ == '__main__':
    function_str = input("Ingresa la función f(x) (e.g., x**3 - 7.51*x**2 + 18.4239*x - 14.8331): ")
    derivative_str = input("Ingresa la derivada df(x) (e.g., 3*x**2 - 15.02*x + 18.4239): ")
    x0 = float(input("Ingresa la estimación inicial x0: "))
    tolerance = float(input("Ingresa la tolerancia: "))
    max_iterations = int(input("Ingresa el número máximo de iteraciones: "))
    error_type = input("Ingresa el tipo de error ('abs' para absoluto, 'rel' para relativo): ")

    def f(x):
        return eval(function_str)

    def df(x):
        return eval(derivative_str)

    if tolerance <= 0:
        print("Error: La tolerancia debe ser un número positivo.")
        exit()
    if max_iterations <= 0:
        print("Error: El número máximo de iteraciones debe ser un número positivo.")
        exit()

    x, fx, iteration_count, iteration_data = newton_method(f, df, x0, tolerance, max_iterations, error_type)

    if iteration_count > 0:
        print(tabulate(iteration_data, headers=["Iteration", "x_current", "f(x_current)", "df(x_current)", "Error"], tablefmt="fancy_grid"))
        print(f"\nRaiz encontrada en: x = {x}, f(x) = {fx} después de {iteration_count} iteraciones.")
    else:
        print("\nNo se ha encontrado ninguna raíz dentro de la tolerancia y las iteraciones máximas dadas.")

# --- Bloque de pruebas por consola ---
if __name__ == '__main__':
    from tabulate import tabulate

    function_str = input("Ingresa la función f(x) (e.g., x**3 - 7.51*x**2 + 18.4239*x - 14.8331): ")
    x0 = float(input("Ingresa la estimación inicial x0: "))
    tolerance = float(input("Ingresa la tolerancia: "))
    max_iterations = int(input("Ingresa el número máximo de iteraciones: "))
    error_type = input("Ingresa el tipo de error ('abs' para absoluto, 'rel' para relativo): ")

    if tolerance <= 0 or max_iterations <= 0:
        print("Error: La tolerancia y el número de iteraciones deben ser positivos.")
        exit()

    try:
        x, fx, iteration_count, iteration_data = newton_method(function_str, x0, tolerance, max_iterations, error_type)

        if iteration_count > 0:
            print(tabulate(iteration_data, headers=["Iteración", "x", "f(x)", "f'(x)", "Error"], tablefmt="fancy_grid"))
            print(f"\nRaíz encontrada: x = {x}, f(x) = {fx} después de {iteration_count} iteraciones.")
        else:
            print("No se ha encontrado ninguna raíz dentro de las condiciones dadas.")

    except Exception as e:
        print(f"Se produjo un error: {e}")