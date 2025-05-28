import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from Python.supCp3 import SUBinterpol_lagrange
from Python.supCp3 import SUBinterpol_newton
from Python.supCp3 import SUBspln_cubico
#from Python.supCp3 import SUBspline_lineal
from Python.supCp3 import Subvandermonde

def spline_lineal_con_polinomios(ValoresX=None, ValoresY=None):
    
    # Entrada de datos
    x = ValoresX
    y = ValoresY
    x = np.array(x)
    y = np.array(y)

    # --- Construcción del Spline Lineal ---
    spline = interp1d(x, y, kind='linear')

    # --- Mostrar polinomios por tramo ---
    #print("\n🔹 POLINOMIOS POR TRAMO:")
    for i in range(len(x) - 1):
        x0, x1 = x[i], x[i + 1]
        y0, y1 = y[i], y[i + 1]
        pendiente = (y1 - y0) / (x1 - x0)
        polinomio = f"S_{i}(x) = {y0:.4f} + {pendiente:.4f}(x - {x0:.4f})"
        dominio = f"para x ∈ [{x0:.4f}, {x1:.4f}]"
        #print(f"- {polinomio} \t{dominio}")

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
    plt.show()

    if input("\n¿Desea comparar con otros metodos? (s/n): ").strip().lower() == 's':
        ILG = SUBinterpol_lagrange.interpol_lagrange(x,y)
        INT = SUBinterpol_newton.interpol_newton(x,y)
        SPCC =  SUBspln_cubico.CubicSpline(x,y)
        VAN = Subvandermonde.interpol_vandermonde(x,y)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'ro', label='Puntos dados')
        plt.plot(VAN[0], VAN[1], 'b-', label='Vandermonde')
        plt.plot(ILG[0],ILG[1], 'm--', label='Lagrange')
        plt.plot(INT[0], INT[1], 'c--', label='Newton')
        plt.plot(SPCC[0], SPCC[1], 'y--', label='Spline Cubico')
        plt.plot(x_plot, y_spline, 'g-', label='Spline Lineal')
        plt.title("Comparacion General")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show()
        print("comparacion general")

# Ejecutar
spline_lineal_con_polinomios()