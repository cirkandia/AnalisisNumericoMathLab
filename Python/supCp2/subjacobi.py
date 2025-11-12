import numpy as np
from tabulate import tabulate
import ast

def str_to_numpy_matrix(matrix_str):
    """
    Convierte una cadena de texto que representa una matriz o vector en un objeto numpy array.
    """
    try:
        matrix_list = ast.literal_eval(matrix_str)
        matrix_np = np.array(matrix_list, dtype=np.float64)
        
        return matrix_np
    except Exception as e:
        print(f"Error al convertir la cadena a matriz numpy: {e}")
        return None
    

def jacobi(matrix_a_str, vector_b_str, initial_guess_str, tolerance, max_iterations, error_type):
    matrix_a = str_to_numpy_matrix(matrix_a_str)
    vector_b = str_to_numpy_matrix(vector_b_str)
    initial_guess = str_to_numpy_matrix(initial_guess_str)
    results_matrix = []
    diagonal_matrix = np.diag(np.diag(matrix_a))
    lu_matrix = matrix_a - diagonal_matrix
    solution_vector = initial_guess
    
    for iteration_count in range(max_iterations):
        diagonal_inverse = np.linalg.inv(diagonal_matrix)
        previous_solution = solution_vector
        solution_vector = np.dot(diagonal_inverse, np.dot(-lu_matrix, solution_vector)) + np.dot(diagonal_inverse, vector_b)
        absolute_error = np.linalg.norm(solution_vector - previous_solution)
        
        if np.linalg.norm(solution_vector) != 0:
            relative_error = absolute_error / np.linalg.norm(solution_vector)
        else:
            print("Error: División por 0")
            relative_error = float('inf')
        
        results_matrix.append([iteration_count, solution_vector.copy().tolist(), absolute_error, relative_error]) 
        if error_type=="rela":
            error = relative_error
        else:
            error = absolute_error
            
        if error < tolerance:
            break

    headers = ["Iteración", "Solución", "Error absoluto", "Error relativo"]
    return (headers, results_matrix)