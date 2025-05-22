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

def doolittle(A,b):
    A = str_to_numpy_matrix(A)   
    b = str_to_numpy_matrix(b)
    
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        for k in range(i, n):
            sum = 0
            for j in range(i):
                sum += (L[i][j] * U[j][k])
            U[i][k] = A[i][k] - sum

        for k in range(i, n):
            if (i == k):
                L[i][i] = 1  # Diagonal as 1
            else:
                sum = 0
                for j in range(i):
                    sum += (L[k][j] * U[j][i])
                
                # Verificar si el denominador es cero
                if U[i, i] == 0:
                    print("Error: division by zero")
                    continue

                L[k][i] = (A[k][i] - sum) / U[i][i]
                
    z = sustprgr(L, b)
    x= sustregr(U, z)            

    return L, U , x 