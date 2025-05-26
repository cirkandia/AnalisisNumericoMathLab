import numpy as np
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
        raise ValueError(f"Error al convertir cadena a matriz numpy: {e}")

def gauss_seidel_method(matrix_a_str, vector_b_str, initial_guess_str, tolerance, max_iterations, error_type):
    matrix_a = str_to_numpy_matrix(matrix_a_str)   
    vector_b = str_to_numpy_matrix(vector_b_str)
    initial_guess = str_to_numpy_matrix(initial_guess_str)
    results_matrix = []

    diagonal_matrix = np.diag(np.diag(matrix_a))
    lu_matrix = matrix_a - diagonal_matrix
    solution_vector = initial_guess

    for iteration_count in range(max_iterations):
        previous_solution = solution_vector.copy()
        for j in range(matrix_a.shape[0]):
            solution_vector[j] = safe_divide(
                (vector_b[j] - np.dot(lu_matrix[j, :], solution_vector)),
                diagonal_matrix[j, j]
            )
        solution_vector = np.round(solution_vector, decimals=5)
        absolute_error = np.linalg.norm(solution_vector - previous_solution)

        if np.linalg.norm(solution_vector) != 0:
            relative_error = absolute_error / np.linalg.norm(solution_vector)
        else:
            relative_error = float('inf')

        results_matrix.append([
            iteration_count,
            solution_vector.copy().tolist(),
            round(float(absolute_error), 6),
            round(float(relative_error), 6)
        ])

        if (relative_error if error_type == "rela" else absolute_error) < tolerance:
            break

    headers = ["Iteración", "Solución", "Error absoluto", "Error relativo"]
    return (headers, results_matrix)