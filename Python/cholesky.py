import numpy as np
import ast

def cholesky_decomposition(A):
    """
    Calculates the Cholesky decomposition of a symmetric, positive definite matrix A.

    Args:
        A (numpy.ndarray): A symmetric, positive definite matrix.

    Returns:
        numpy.ndarray: The lower triangular matrix L such that A = LL^T.
                       Returns None if the matrix is not symmetric or not positive definite.
    """
    n = A.shape[0]

    # Check if the matrix is square
    if A.shape[0] != A.shape[1]:
        print("Error: Matrix A must be square.")
        return None

    # Check if the matrix is symmetric
    if not np.allclose(A, A.T):
        print("Error: Matrix A must be symmetric.")
        return None

    # Check if the matrix is positive definite
    try:
        np.linalg.cholesky(A)
    except np.linalg.LinAlgError:
        print("Error: Matrix A must be positive definite.")
        return None

    L = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1):
            sum_k = sum(L[i][k] * L[j][k] for k in range(j))
            if (i == j):
                L[i][j] = np.sqrt(A[i, i] - sum_k)
            else:
                L[i][j] = (1.0 / L[j][j] * (A[i, j] - sum_k))
    return L

if __name__ == '__main__':
    # Get matrix A as input from the user
    matrix_str = input("Ingresa la matriz A cómo una lista de listas (e.g., [[4, 12, -16], [12, 37, -43], [-16, -43, 98]]): ")
    try:
        A = np.array(ast.literal_eval(matrix_str), dtype=float)
    except (SyntaxError, ValueError):
        print("Error: Formato de la matriz invalido. Por favor ingresa una lista de listas con valores numéricos válidos.")
        exit()

    L = cholesky_decomposition(A)

    if L is not None:
        print("Matriz A:")
        print(A)
        print("\nDescomposición de Cholesky (L):")
        print(L)

        # Verify that A = LL^T
        A_reconstructed = np.dot(L, L.T)
        print("\nMatriz reconstruida (LL^T):")
        print(A_reconstructed)

        # Check if the reconstructed matrix is close to the original matrix
        if np.allclose(A, A_reconstructed):
            print("\nLa descomposición de Cholesky es correcta.")
        else:
            print("\nLa descomposición de Cholesky es incorrecta.")
