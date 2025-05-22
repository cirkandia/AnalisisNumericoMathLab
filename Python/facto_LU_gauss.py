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

def sustprgr(A, b):
    # Inicialización
    n = A.shape[0]
    x = np.zeros(n)
    
    # Sustitución progresiva
    for i in range(n):
        sum_ax = 0
        for j in range(i):
            sum_ax += A[i, j] * x[j]
        
        # Verificar si el denominador es cero
        if A[i, i] == 0:
            print("Error: division by zero")
            continue

        x[i] = (b[i] - sum_ax) / A[i, i]
    
    return x

def sustregr(U, b):
    # Inicialización
    n = U.shape[0]
    x = np.zeros(n)
    
    # Sustitución regresiva
    for i in range(n-1, -1, -1):
        sum_ux = 0
        for j in range(i+1, n):
            sum_ux += U[i, j] * x[j]
        
        # Verificar si el denominador es cero
        if U[i, i] == 0:
            print("Error: division by zero")
            continue

        x[i] = (b[i] - sum_ux) / U[i, i]
    
    return x

def C11_lusimpl(A, b):
    A = str_to_numpy_matrix(A)   
    b = str_to_numpy_matrix(b)
    n = A.shape[0]
    L = np.eye(n, dtype=float)
    U = np.zeros((n, n), dtype=float)
    M = A.astype(float)  # Asegura que M sea de tipo float
    
    # Factorización
    for i in range(n-1):
        for j in range(i+1, n):
            if M[j, i] != 0:
                # Verificar si el denominador es cero
                if M[i, i] == 0:
                    print("Error: division by zero")
                    continue

                L[j, i] = M[j, i] / M[i, i]
                M[j, i:n] = M[j, i:n] - (M[j, i] / M[i, i]) * M[i, i:n]
        U[i, i:n] = M[i, i:n]
        U[i+1, i+1:n] = M[i+1, i+1:n]
    U[n-1, n-1] = M[n-1, n-1]
    
    z = sustprgr(L, b)
    x= sustregr(U, z)
    
    return x, L, U
