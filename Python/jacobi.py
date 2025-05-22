import numpy as np
import ast

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
    

def jacobi(A, b, x0, tol, max_iter,error12):
    A = str_to_numpy_matrix(A)
    b = str_to_numpy_matrix(b)
    x0 = str_to_numpy_matrix(x0)
    matriz = []
     
    D = np.diag(np.diag(A))
    LU = A - D
    x = x0
    
    for i in range(max_iter):
        D_inv = np.linalg.inv(D)
        x_aux = x
        x = np.dot(D_inv, np.dot(-LU, x)) + np.dot(D_inv, b)
        errorabs = np.linalg.norm(x - x_aux)
        
        # Verificar si la norma de x es cero
        if np.linalg.norm(x) != 0:
            relative_error = errorabs / np.linalg.norm(x)
        else:
            print("Error: division by zero")
            relative_error = float('inf')
        
        matriz.append([i, x.copy(), errorabs, relative_error]) 
        if error12=="rela":
            error=relative_error
        else:
            error=errorabs
            
        if error < tol:
            break
    return matriz



#A = np.array([[10, -1, 2, 0], [-1, 11, -1, 3], [2, -1, 10, -1], [0, 3, -1, 8]])
#b = np.array([[6], [25], [-11], [15]])
#x0 = np.zeros(4)

#x = jacobi(A, b, x0, 10**-6, 500)
#print("Solution:", x)
