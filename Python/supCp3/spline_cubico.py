import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def spline_cubico():
    print("=== MÉTODO DE SPLINE CÚBICO ===")
    print("Interpolación con polinomios cúbicos por tramos (suaves).\n")
    
    # Entrada de datos
    n = int(input("Ingrese el número de puntos (n+1): ")) - 1
    x = []
    y = []
    print("\nIngrese los puntos (x_i, y_i):")
    for i in range(n + 1):
        x.append(float(input(f"x_{i}: ")))
        y.append(float(input(f"y_{i}: ")))
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

# Ejecutar
spline_cubico()