import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from Python.supCp3 import SUBinterpol_lagrange
from Python.supCp3 import SUBinterpol_newton
from Python.supCp3 import SUBspln_cubico
from Python.supCp3 import Subvandermonde

def spline_lineal_con_polinomios(ValoresX=None, ValoresY=None):
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

    # --- Construcción del Spline Lineal ---
    spline = interp1d(x, y, kind='linear')

    # --- Mostrar polinomios por tramo ---
    polinomios = []
    for i in range(len(x) - 1):
        x0, x1 = x[i], x[i + 1]
        y0, y1 = y[i], y[i + 1]
        pendiente = (y1 - y0) / (x1 - x0)
        polinomio = (
            f"S_{i}(x) = {y0:.4f} + {pendiente:.4f}(x - {x0:.4f})\n"
            f"    para x ∈ [{x0:.4f}, {x1:.4f}]"
        )
        polinomios.append(polinomio)

    # --- Evaluación y gráfica ---
    x_plot = np.linspace(min(x), max(x), 100)
    y_spline = spline(x_plot)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', label='Puntos dados', markersize=8)
    plt.plot(x_plot, y_spline, 'b-', label='Spline Lineal', linewidth=2)
    plt.title("Interpolación con Spline Lineal", fontsize=14)
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
        SPCC = SUBspln_cubico.CubicSpline(x, y)
        VAN = Subvandermonde.interpol_vandermonde(x, y)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'ro', label='Puntos dados')
        plt.plot(VAN[0], VAN[1], 'b-', label='Vandermonde')
        plt.plot(ILG[0], ILG[1], 'm--', label='Lagrange')
        plt.plot(INT[0], INT[1], 'c--', label='Newton')
        plt.plot(SPCC[0], SPCC[1], 'y--', label='Spline Cúbico')
        plt.plot(x_plot, y_spline, 'g-', label='Spline Lineal')
        plt.title("Comparación General")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show(block=False)
        resultado += "\nComparación general mostrada en la gráfica."

    

# Ejecutar solo si es script principal
if __name__ == "__main__":
    print(spline_lineal_con_polinomios())