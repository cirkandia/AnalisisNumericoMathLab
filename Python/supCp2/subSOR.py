import numpy as np
from tabulate import tabulate
import ast

def safe_divide(a, b):
    if b == 0:
        raise ZeroDivisionError(f"Intento de dividir por cero: {a} / {b}")
    return a / b

def str_to_numpy_matrix(matrix_str):
    """
    Convierte una cadena de texto que representa una matriz o vector en un objeto numpy array.
    """
    try:
        matrix_list = ast.literal_eval(matrix_str)
        matrix_np = np.array(matrix_list, dtype=np.float64)
        return matrix_np
    except Exception as e:
        print(f"Error al convertir cadena a matriz numpy: {e}")
        return None

def sor_method(matrix_a_str, vector_b_str, initial_guess_str, relaxation_factor, tolerance, max_iterations, error_type):
    matrix_a = str_to_numpy_matrix(matrix_a_str)
    vector_b = str_to_numpy_matrix(vector_b_str)
    initial_guess = str_to_numpy_matrix(initial_guess_str)
    
    results_matrix = []
    solution_vector = initial_guess.copy()
    
    for iteration_count in range(max_iterations):
        previous_solution = solution_vector.copy()
        
        for i in range(matrix_a.shape[0]):
            sigma = 0
            for j in range(matrix_a.shape[1]):
                if i != j:
                    sigma += matrix_a[i, j] * solution_vector[j]
            
            solution_vector[i] = (1 - relaxation_factor) * previous_solution[i] + (relaxation_factor / matrix_a[i, i]) * (vector_b[i] - sigma)
        
        absolute_error = np.linalg.norm(solution_vector - previous_solution)
        relative_error = safe_divide(absolute_error, np.linalg.norm(solution_vector))
        
        if error_type == "rela":
            error = relative_error
        else:
            error = absolute_error
        
        results_matrix.append([iteration_count, solution_vector.tolist(), absolute_error, relative_error])
        
        if error < tolerance:
            break
            
    return results_matrix

matrix_a_str = input("Ingresa la matriz A (e.g., [[4,1],[1,3]]): ")
vector_b_str = input("Ingresa el vector b (e.g., [1,2]): ")
initial_guess_str = input("Introduzca la estimación inicial x0 (e.g., [0,0]): ")
relaxation_factor = float(input("Introduzca el factor de relajación omega: "))
tolerance = float(input("Ingresa la tolerancia: "))
max_iterations = int(input("Ingresa el número máximo de iteraciones: "))
error_type = input("Ingresa el tipo de error (rela para relativo o abs para absoluto): ")

results = sor_method(matrix_a_str, vector_b_str, initial_guess_str, relaxation_factor, tolerance, max_iterations, error_type)

print(tabulate(results, headers=["Iteración", "Solución", "Error absoluto", "Error relativo"], tablefmt="fancy_grid"))
