import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from Python.supCp3 import SUBinterpol_lagrange
from Python.supCp3 import SUBinterpol_newton
#from Python.supCp3 import SUBspln_cubico
from Python.supCp3 import SUBspline_lineal
from Python.supCp3 import Subvandermonde

def spline_cubico(ValoresX=None, ValoresY=None):
    x = ValoresX
    y = ValoresY
    x = np.array(x)
    y = np.array(y)

    # --- Construcción del Spline Cúbico Natural ---
    spline = CubicSpline(x, y, bc_type='natural')  # bc_type='natural' -> Segunda derivada = 0 en los extremos

    # --- Coeficientes de los polinomios por tramo ---
    coeficientes = spline.c  # Forma (4, n-1): [a_i, b_i, c_i, d_i] para cada tramo i

    print("\n🔹 POLINOMIOS POR TRAMO (S_i(x) = a_i + b_i(x-x_i) + c_i(x-x_i)^2 + d_i(x-x_i)^3):")
    for i in range(len(x) - 1):
        a, b, c, d = coeficientes[:, i]
        x_i = x[i]
        print(f"- S_{i}(x) = {a:.4f} + {b:.4f}(x-{x_i:.4f}) + {c:.4f}(x-{x_i:.4f})² + {d:.4f}(x-{x_i:.4f})³ \t para x ∈ [{x_i:.4f}, {x[i+1]:.4f}]")

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
    plt.show()

    if input("\n¿Desea comparar con otros metodos? (s/n): ").strip().lower() == 's':
        ILG = SUBinterpol_lagrange.interpol_lagrange(x,y)
        INT = SUBinterpol_newton.interpol_newton(x,y)
        SPL = SUBspline_lineal.SUBSUBspline_lineal(x,y)
        VAN = Subvandermonde.interpol_vandermonde(x,y)
            
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'ro', label='Puntos dados')
        plt.plot(x_plot, y_spline, 'b-', label='Spline Cúbico')
        plt.plot(VAN[0], VAN[1], 'k-', label='Vandermonde')
        plt.plot(SPL[0], SPL[1], 'g--', label='Pline lineal')
        plt.plot(ILG[0],ILG[1], 'm--', label='Lagrange')
        plt.plot(INT[0], INT[1], 'c--', label='Newton')
        plt.title("Comparacion General")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show()
        print("comparacion general")

# Ejecutar
spline_cubico()