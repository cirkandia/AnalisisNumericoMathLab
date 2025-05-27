import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import supCp3.interpoloacion_lagrange
import supCp3.interpolacion_newton
import supCp3.spline_cubico
#import supCp3.spline_lineal
import supCp3.Vandermonde

def spline_lineal_con_polinomios():
    print("=== MÉTODO DE SPLINE LINEAL ===")
    print("Interpolación por segmentos de recta entre puntos dados.\n")
    
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

    # --- Construcción del Spline Lineal ---
    spline = interp1d(x, y, kind='linear')

    # --- Mostrar polinomios por tramo ---
    print("\n🔹 POLINOMIOS POR TRAMO:")
    for i in range(len(x) - 1):
        x0, x1 = x[i], x[i + 1]
        y0, y1 = y[i], y[i + 1]
        pendiente = (y1 - y0) / (x1 - x0)
        polinomio = f"S_{i}(x) = {y0:.4f} + {pendiente:.4f}(x - {x0:.4f})"
        dominio = f"para x ∈ [{x0:.4f}, {x1:.4f}]"
        print(f"- {polinomio} \t{dominio}")

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
        supCp3.interpoloacion_lagrange.interpolacion_lagrange()
        supCp3.interpolacion_newton.interpolacion_newton()
        supCp3.spline_cubico.spline_cubico()
        supCp3.Vandermonde.interpolacion_vandermonde()

# Ejecutar
spline_lineal_con_polinomios()