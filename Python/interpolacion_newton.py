import numpy as np
import time
import matplotlib.pyplot as plt
from Python.supCp3 import SUBinterpol_lagrange
#from Python.supCp3 import SUBinterpol_newton
from Python.supCp3 import SUBspln_cubico
from Python.supCp3 import SUBspline_lineal
from Python.supCp3 import Subvandermonde

def interpolacion_newton(ValoresX=None, ValoresY=None):
    # Entrada de datos si no se pasan argumentos
    if ValoresX is None or ValoresY is None:
        x = input("Ingrese los valores de x separados por coma: ")
        y = input("Ingrese los valores de y separados por coma: ")
        x = np.array([float(val) for val in x.split(",")])
        y = np.array([float(val) for val in y.split(",")])
    else:
        x = np.array(ValoresX)
        y = np.array(ValoresY)

    # Validación
    if x.ndim == 0 or len(x) < 2:
        raise ValueError("Debe ingresar al menos dos puntos para interpolar.")
    if not np.all(np.diff(x) > 0):
        raise ValueError("Los valores de x deben estar en orden creciente")
    if len(x) != len(y):
        raise ValueError("Las listas de x e y deben tener la misma longitud.")

    # --- Construcción del polinomio de Newton ---
    start_time = time.time()

    # Tabla de diferencias divididas
    n_points = len(x)
    F = np.zeros((n_points, n_points))
    F[:, 0] = y  # Primera columna son las y_i

    for j in range(1, n_points):
        for i in range(n_points - j):
            F[i, j] = (F[i + 1, j - 1] - F[i, j - 1]) / (x[i + j] - x[i])

    # Coeficientes del polinomio (primera fila de F)
    a = F[0, :]

    # --- Formatear el polinomio como string ---
    polinomio = f"P(x) = {a[0]:.4f}"
    termino = ""
    for i in range(1, n_points):
        termino += f"(x - {x[i-1]:.4f})"
        polinomio += f" + {a[i]:.4f}{termino}"

    end_time = time.time()
    tiempo_ejecucion = end_time - start_time

    # --- Evaluar el polinomio (para gráfica) ---
    def P_newton(x_eval):
        result = a[-1]
        for i in range(len(a) - 2, -1, -1):
            result = result * (x_eval - x[i]) + a[i]
        return result

    # --- Gráfica ---
    x_plot = np.linspace(min(x), max(x), 100)
    y_newton = [P_newton(xi) for xi in x_plot]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', label='Puntos dados')
    plt.plot(x_plot, y_newton, 'b-', label='Polinomio de Newton')
    plt.title("Interpolación de Newton", fontsize=14)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.legend()
    plt.grid()
    plt.show(block=False)

    resultado = (
        f"Puntos ingresados: {list(zip(ValoresX,ValoresY))}\n"
        f"Polinomio de Newton:\n{polinomio}\n\n"
        f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos"
    )
    return resultado

    # Comparación con otros métodos (opcional)
    comparar = input("\n¿Desea comparar con otros métodos? (s/n): ").strip().lower()
    if comparar == 's':
        ILG = SUBinterpol_lagrange.interpol_lagrange(x, y)
        SPCC = SUBspln_cubico.SUBSUBspline_cubico(x, y)
        SPL = SUBspline_lineal.SUBSUBspline_lineal(x, y)
        VAN = Subvandermonde.interpol_vandermonde(x, y)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'ro', label='Puntos dados')
        plt.plot(x_plot, y_newton, 'b-', label='Newton')
        plt.plot(SPL[0], SPL[1], 'g--', label='Spline lineal')
        plt.plot(ILG[0], ILG[1], 'm--', label='Lagrange')
        plt.plot(VAN[0], VAN[1], 'k-', label='Vandermonde')
        plt.plot(SPCC[0], SPCC[1], 'y--', label='Spline Cúbico')
        plt.title("Comparación General")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show(block=False)
        resultado += "\nComparación general mostrada en la gráfica."


# Ejecutar solo si es script principal
if __name__ == "__main__":
    print(interpolacion_newton())