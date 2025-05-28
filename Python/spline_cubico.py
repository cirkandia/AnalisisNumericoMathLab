import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from Python.supCp3 import SUBinterpol_lagrange
from Python.supCp3 import SUBinterpol_newton
#from Python.supCp3 import SUBspln_cubico
from Python.supCp3 import SUBspline_lineal
from Python.supCp3 import Subvandermonde

def spline_cubico(ValoresX=None, ValoresY=None):
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

    # --- Construcción del Spline Cúbico Natural ---
    spline = CubicSpline(x, y, bc_type='natural')  # Segunda derivada = 0 en los extremos

    # --- Coeficientes de los polinomios por tramo ---
    coeficientes = spline.c  # (4, n-1): [a_i, b_i, c_i, d_i] para cada tramo i
    polinomios = []
    for i in range(len(x) - 1):
        a, b, c, d = coeficientes[:, i]
        x_i = x[i]
        polinomio = (
            f"S_{i}(x) = {a:.4f} + {b:.4f}(x-{x_i:.4f}) + {c:.4f}(x-{x_i:.4f})² + {d:.4f}(x-{x_i:.4f})³\n"
            f"    para x ∈ [{x_i:.4f}, {x[i+1]:.4f}]"
        )
        polinomios.append(polinomio)

    # --- Evaluación y gráfica ---
    x_plot = np.linspace(min(x), max(x), 500)
    y_spline = spline(x_plot)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', label='Puntos dados', markersize=8)
    plt.plot(x_plot, y_spline, 'b-', label='Spline Cúbico', linewidth=2)
    plt.title("Interpolación con Spline Cúbico Natural", fontsize=14)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.legend()
    plt.grid()
    plt.show(block=False)

    resultado = (
        f"Puntos ingresados: {list(zip(ValoresX,ValoresY))}\n"
        f"Polinomios por tramo:\n\n" + "\n\n".join(polinomios)
    )
    return resultado

    # Comparación con otros métodos (opcional)
    comparar = input("\n¿Desea comparar con otros métodos? (s/n): ").strip().lower()
    if comparar == 's':
        ILG = SUBinterpol_lagrange.interpol_lagrange(x, y)
        INT = SUBinterpol_newton.interpol_newton(x, y)
        SPL = SUBspline_lineal.SUBSUBspline_lineal(x, y)
        VAN = Subvandermonde.interpol_vandermonde(x, y)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'ro', label='Puntos dados')
        plt.plot(x_plot, y_spline, 'b-', label='Spline Cúbico')
        plt.plot(VAN[0], VAN[1], 'k-', label='Vandermonde')
        plt.plot(SPL[0], SPL[1], 'g--', label='Spline lineal')
        plt.plot(ILG[0], ILG[1], 'm--', label='Lagrange')
        plt.plot(INT[0], INT[1], 'c--', label='Newton')
        plt.title("Comparación General")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show(block=False)
        resultado += "\nComparación general mostrada en la gráfica."

    

# Ejecutar solo si es script principal
if __name__ == "__main__":
    print(spline_cubico())