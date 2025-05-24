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


def gauss_seidel_method(matrix_a_str, vector_b_str, initial_guess_str, tolerance, max_iterations, error_type):
    matrix_a = str_to_numpy_matrix(matrix_a_str)   
    vector_b = str_to_numpy_matrix(vector_b_str)
    initial_guess = str_to_numpy_matrix(initial_guess_str)
    results_matrix=[]
    
    diagonal_matrix = np.diag(np.diag(matrix_a))
    lu_matrix = matrix_a - diagonal_matrix
    solution_vector = initial_guess
    
    for iteration_count in range(max_iterations):
        previous_solution = solution_vector.copy()
        for j in range(matrix_a.shape[0]):
            solution_vector[j] = safe_divide((vector_b[j] - np.dot(lu_matrix[j, :], solution_vector)), diagonal_matrix[j, j])
        solution_vector = np.round(solution_vector, decimals=5)
        absolute_error = np.linalg.norm(solution_vector - previous_solution)
        
        # Verificar si la norma de x es cero
        if np.linalg.norm(solution_vector) != 0:
            relative_error = absolute_error / np.linalg.norm(solution_vector)
        else:
            print("Error: División por 0")
            relative_error = float('inf')
            
        if error_type=="rela":
            error=relative_error
        else:
            error=absolute_error  
        results_matrix.append([iteration_count, solution_vector.tolist(), absolute_error, relative_error])
        if error < tolerance:
            break
    return results_matrix

matrix_a_str = input("Ingresa la matriz A (e.g., [[4,1],[1,3]]): ")
vector_b_str = input("Ingresa el vector b (e.g., [1,2]): ")
initial_guess_str = input("Ingresa la estimación inicial x0 (e.g., [0,0]): ")
tolerance = float(input("Ingresa la tolerancia: "))
max_iterations = int(input("Ingresa el número máximo de iteraciones: "))
error_type = input("Ingresa el tipo de error (rela para relativo o abs para absoluto): ")

results = gauss_seidel_method(matrix_a_str, vector_b_str, initial_guess_str, tolerance, max_iterations, error_type)

print(tabulate(results, headers=["Iteración", "Solución", "Error absoluto", "Error relativo"], tablefmt="fancy_grid"))
