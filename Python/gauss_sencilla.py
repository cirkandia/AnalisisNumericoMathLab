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

def sustreg(Ab, n):
    x = np.zeros(n)
    if Ab[n-1, n-1] == 0:
        print("Error: división por 0")
        return x
    x[n-1] = Ab[n-1, n] / Ab[n-1, n-1]

    for i in range(n-2, -1, -1):
        sum = 0
        for p in range(i+1, n):
            sum = sum + Ab[i, p] * x[p]
        if Ab[i, i] == 0:
            print("Error: división por 0")
            continue

        x[i] = (Ab[i, n] - sum) / Ab[i, i]
    return x

def gauss_sen(A, b):
    A = str_to_numpy_matrix(A) # Convertir la matriz a cadena
    b = str_to_numpy_matrix(b)
    A = A.astype(np.float64)
    b = b.astype(np.float64)
    
    n = len(A)
    M = np.hstack([A, b.reshape(-1, 1)])
    print(f'Initial M = \n', M)
    # Eliminación hacia adelante
    for i in range(n):
        for j in range(i+1, n):
            if M[j, i] != 0:
                factor = M[j, i] / M[i, i]
                M[j, i:] -= factor * M[i, i:]
        print(f'After forward elimination step {i+1}, M = \n', M)

    # Sustitución hacia atrás
    x = sustreg(M, n)
    print(f'After back substitution, x = ', x)

    return x

 

#A1="[[4, 2, 3], [3, 4, 2], [2, -1, 5]]"
#b1="[8, -1, 3]"

 
 
 
 
# Convertir las cadenas a listas


#x = gauss_sen(A1, b1) # Debería imprimir [1, 1, 1]
#print('Final result: x = ', x)