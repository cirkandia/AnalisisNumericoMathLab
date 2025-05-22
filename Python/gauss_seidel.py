import numpy as np
import ast

def safe_divide(a, b):
    if b == 0:
        raise ZeroDivisionError(f"Attempted to divide by zero: {a} / {b}")
    return a / b

    
def str_to_numpy_matrix(matrix_str):
    """
    Convierte una cadena de texto que representa una matriz o vector en un objeto numpy array.
    """
    try:
        # Evaluar la cadena para convertirla en una lista de listas (matriz) o una lista (vector)
        matrix_list = ast.literal_eval(matrix_str)
        
        # Convertir la lista en un array de numpy
        matrix_np = np.array(matrix_list, dtype=np.float64)
        
        return matrix_np
    except Exception as e:
        print(f"Error converting string to numpy matrix: {e}")
        return None


def gauss_seidel(A, b, x0, tol, max_iter,error12):
    A = str_to_numpy_matrix(A)   
    b = str_to_numpy_matrix(b)
    x0 = str_to_numpy_matrix(x0)
    matriz=[]
    D = np.diag(np.diag(A))
    LU = A - D
    x = x0
    
    for i in range(max_iter):
        x_aux = x.copy()
        for j in range(A.shape[0]):
            x[j] = (b[j] - np.dot(LU[j, :], x)) / D[j, j]
        x = np.round(x, decimals=5)
        errorabs = np.linalg.norm(x - x_aux)
        relative_error = errorabs / np.linalg.norm(x)
        if error12=="rela":
            error=relative_error
        else:
            error=errorabs  
         
        matriz.append([i, x, errorabs, relative_error])
        if error < tol:
            break
    return matriz


