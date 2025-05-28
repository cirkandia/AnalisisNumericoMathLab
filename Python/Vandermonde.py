import numpy as np
import time
import matplotlib.pyplot as plt
from Python.supCp3 import SUBinterpol_lagrange
from Python.supCp3 import SUBinterpol_newton
from Python.supCp3 import SUBspln_cubico
from Python.supCp3 import SUBspline_lineal
#from Python.supCp3 import Subvandermonde


def interpolacion_vandermonde(ValoresX=None, ValoresY=None):
    # Validación de entrada
    x = np.array(ValoresX)
    y = np.array(ValoresY)
    if x.ndim == 0 or len(x) < 2:
        raise ValueError("Debe ingresar al menos dos puntos para interpolar.")
    if not np.all(np.diff(x) > 0):
        raise ValueError("Los valores de x deben estar en orden creciente")
    if len(x) != len(y):
        raise ValueError("Las listas de x e y deben tener la misma longitud.")

    # --- Análisis de tiempo ---
    start_time = time.time()
    V = np.vander(x, increasing=True)
    cond_num = np.linalg.cond(V)
    a = np.linalg.solve(V, y)
    end_time = time.time()
    tiempo_ejecucion = end_time - start_time

    # --- Gráfica ---
    x_plot = np.linspace(min(x), max(x), 100)
    y_vander = np.polyval(a[::-1], x_plot)  # polyval espera orden descendente

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', label='Puntos dados')
    plt.plot(x_plot, y_vander, 'b-', label='Vandermonde')
    plt.title("Interpolación con Vandermonde")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid()
    plt.show(block=False)

    # Prepara resultados para la GUI (sin coeficiente de referencia)
    resultado = (
        f"Puntos ingresados: {list(zip(x, y))}\n"
        f"Coeficientes del polinomio (Vandermonde): {a}\n"
        f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos\n"
        f"Número de condición de la matriz: {cond_num:.2e} (valores altos indican inestabilidad)\n"
    )
    return resultado

def comparar_metodos(ValoresX, ValoresY):
    x = np.array(ValoresX)
    y = np.array(ValoresY)
    x_plot = np.linspace(min(x), max(x), 100)
    V = np.vander(x, increasing=True)
    a = np.linalg.solve(V, y)
    y_vander = np.polyval(a[::-1], x_plot)

    ILG = SUBinterpol_lagrange.interpol_lagrange(x, y)
    INT = SUBinterpol_newton.interpol_newton(x, y)
    SPCC = SUBspln_cubico.SUBSUBspline_cubico(x, y)
    SPL = SUBspline_lineal.SUBSUBspline_lineal(x, y)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', label='Puntos dados')
    plt.plot(x_plot, y_vander, 'b-', label='Vandermonde')
    plt.plot(SPL[0], SPL[1], 'g--', label='Spline lineal')
    plt.plot(ILG[0], ILG[1], 'm--', label='Lagrange')
    plt.plot(INT[0], INT[1], 'c--', label='Newton')
    plt.plot(SPCC[0], SPCC[1], 'y--', label='Spline Cúbico')
    plt.title("Comparación General")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid()
    plt.show()
