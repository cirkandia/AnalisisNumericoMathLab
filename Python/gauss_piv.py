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
    
    # Verificar si el denominador es cero
    if Ab[n-1, n-1] == 0:
        print("Error: División por 0")
        return x

    x[n-1] = Ab[n-1, n] / Ab[n-1, n-1]
    for i in range(n-2, -1, -1):
        sum = 0
        for p in range(i+1, n):
            sum = sum + Ab[i, p] * x[p]
        
        # Verificar si el denominador es cero
        if Ab[i, i] == 0:
            print("Error: División por 0")
            continue

        x[i] = (Ab[i, n] - sum) / Ab[i, i]
    return x

def print_matrix(label, M):
    print(f'{label}:\n', M, '\n')

def gauss_piv(A, b):
    A = str_to_numpy_matrix(A) 
    b = str_to_numpy_matrix(b)
    A = A.astype(np.float64)
    b = b.astype(np.float64)
    
    n = len(A)
    M = np.hstack([A, b.reshape(-1, 1)])
    print_matrix('Initial M', M)
    for i in range(n):
        # Eliminación hacia adelante con pivoteo parcial
        maximo = np.argmax(np.abs(M[i:n, i])) + i
        if i != maximo:
            M[[i, maximo]] = M[[maximo, i]]
            print_matrix(f'After pivoting step {i+1}', M)
        for j in range(i+1, n):
            # Verificar si el denominador es cero
            if M[i, i] == 0:
                print("Error: División por 0")
                continue

            factor = M[j, i] / M[i, i]
            M[j, i:] -= factor * M[i, i:]
        print(f'factor = {factor}')
        print_matrix(f'After step {i+1}', M)
        

    # Sustitución hacia atrás
    x = sustreg(M, n)
    print(f'After back substitution, x = ', x)

    return x