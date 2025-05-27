import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def spline_cubico(xin, yin):
    x= xin
    y= yin

    # --- Construcción del Spline Cúbico Natural ---
    spline = CubicSpline(x, y, bc_type='natural')  # bc_type='natural' -> Segunda derivada = 0 en los extremos

    # --- Coeficientes de los polinomios por tramo ---
    coeficientes = spline.c  # Forma (4, n-1): [a_i, b_i, c_i, d_i] para cada tramo i

    #print("\n🔹 POLINOMIOS POR TRAMO (S_i(x) = a_i + b_i(x-x_i) + c_i(x-x_i)^2 + d_i(x-x_i)^3):")
    for i in range(len(x) - 1):
        a, b, c, d = coeficientes[:, i]
        x_i = x[i]
        #print(f"- S_{i}(x) = {a:.4f} + {b:.4f}(x-{x_i:.4f}) + {c:.4f}(x-{x_i:.4f})² + {d:.4f}(x-{x_i:.4f})³ \t para x ∈ [{x_i:.4f}, {x[i+1]:.4f}]")

    # --- Evaluación y gráfica ---
    x_plot = np.linspace(min(x), max(x), 500)
    y_spline = spline(x_plot)

    return [x_plot, y_spline,[a, b, c, d]]

# Ejecutar
#spline_cubico()