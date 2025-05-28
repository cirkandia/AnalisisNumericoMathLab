import numpy as np
import time
import matplotlib.pyplot as plt
#from Python.supCp3 import SUBinterpol_lagrange
from Python.supCp3 import SUBinterpol_newton
from Python.supCp3 import SUBspln_cubico
from Python.supCp3 import SUBspline_lineal
from Python.supCp3 import Subvandermonde

def interpolacion_lagrange(ValoresX=None, ValoresY=None):
    x = ValoresX
    y = ValoresY
    x = np.array(x)
    y = np.array(y)

    # --- Construcción del polinomio de Lagrange ---
    start_time = time.time()

    # Función para calcular el polinomio base L_i(x)
    def L(i, x_eval):
        result = 1.0
        for j in range(len(x)):
            if j != i:
                result *= (x_eval - x[j]) / (x[i] - x[j])
        return result

    # Función para evaluar el polinomio interpolador P(x)
    def P_lagrange(x_eval):
        return sum(y[i] * L(i, x_eval) for i in range(len(x)))

    # --- Formatear el polinomio como string ---
    polinomio = "P(x) = "
    for i in range(len(x)):
        term = f"{y[i]:.4f} * L_{i}(x)"
        if i > 0:
            polinomio += " + " + term
        else:
            polinomio += term

    # Opcional: Mostrar polinomios base L_i(x)
    print("\n🔹 POLINOMIOS BASE DE LAGRANGE:")
    for i in range(len(x)):
        L_i = "L_" + str(i) + "(x) = "
        for j in range(len(x)):
            if j != i:
                L_i += f"(x - {x[j]:.4f}) / ({x[i]:.4f} - {x[j]:.4f}) * "
        L_i = L_i[:-3]  # Eliminar el último " * "
        print(L_i)

    end_time = time.time()
    tiempo_ejecucion = end_time - start_time

    # --- Resultados ---
    print("\n🔹 POLINOMIO INTERPOLADOR DE LAGRANGE:")
    print(polinomio)
    print(f"\n🔹 TIEMPO DE EJECUCIÓN: {tiempo_ejecucion:.6f} segundos")

    # --- Gráfica ---
    x_plot = np.linspace(min(x), max(x), 100)
    y_lagrange = [P_lagrange(xi) for xi in x_plot]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', label='Puntos dados')
    plt.plot(x_plot, y_lagrange, 'b-', label='Polinomio de Lagrange')
    plt.title("Interpolación de Lagrange", fontsize=14)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()

    if input("\n¿Desea comparar con otros metodos? (s/n): ").strip().lower() == 's':
        SPCC = SUBspln_cubico.SUBSUBspline_cubico(x,y)
        SPL = SUBspline_lineal.SUBSUBspline_lineal(x,y)
        VAN = Subvandermonde.interpol_vandermonde(x,y)
        INT = SUBinterpol_newton.interpol_newton(x,y)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'ro', label='Puntos dados')
        plt.plot(x_plot, y_lagrange, 'b-', label='Lagrange')
        plt.plot(VAN[0], VAN[1], 'k-', label='Vandermonde')
        plt.plot(SPL[0], SPL[1], 'g--', label='Pline lineal')
        plt.plot(INT[0], INT[1], 'c--', label='Newton')
        plt.plot(SPCC[0], SPCC[1], 'y--', label='Spline Cubico')
        plt.title("Comparacion General")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show()
        print("comparacion general")


# Ejecutar
interpolacion_lagrange()