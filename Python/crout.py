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
            print("Error: Division por 0")
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
            print("Error: Division por 0")
            continue

        x[i] = (b[i] - sum_ux) / U[i, i]
    
    return x

def crout(A,b):
    A = str_to_numpy_matrix(A)   
    b = str_to_numpy_matrix(b)
    
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for j in range(n):
        U[j, j] = 1
        for i in range(j, n):
            alpha = float(A[i, j])
            for k in range(j):
                alpha -= L[i, k] * U[k, j]
            L[i, j] = alpha

        for i in range(j+1, n):
            tempU = float(A[j, i])
            for k in range(j):
                tempU -= L[j, k] * U[k, i]
            
            # Verificar si el denominador es cero
            if L[j, j] == 0:
                print("Error: Division por 0")
                continue

            U[j, i] = tempU / L[j, j]
            
    z = sustprgr(L, b)
    x= sustregr(U, z)
    return L, U ,x

A1="[[4, 2, 3], [3, 4, 2], [2, -1, 5]]"
b1="[8, -1, 3]"
L, U, x = crout(A1,b1)
print(L, U, x)