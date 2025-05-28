import numpy as np
import time
import matplotlib.pyplot as plt
import supCp3.SUBinterpol_lagrange
#import supCp3.SUBinterpol_newton
import supCp3.SUBspln_cubico
import supCp3.SUBspline_lineal
import supCp3.Subvandermonde

def interpolacion_newton(ValoresX=None, ValoresY=None):
    print("=== INTERPOLACIÓN DE NEWTON CON DIFERENCIAS DIVIDIDAS ===")
    x = ValoresX
    y = ValoresY
    x = np.array(x)
    y = np.array(y)

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
        polinomio += f" + {a[i]:.4f}" + termino

    end_time = time.time()
    tiempo_ejecucion = end_time - start_time

    # --- Evaluar el polinomio (para gráfica) ---
    def P_newton(x_eval):
        result = a[-1]
        for i in range(len(a) - 2, -1, -1):
            result = result * (x_eval - x[i]) + a[i]
        return result

    # --- Resultados ---
    print("\n🔹 POLINOMIO DE NEWTON:")
    print(polinomio)
    print(f"\n🔹 TIEMPO DE EJECUCIÓN: {tiempo_ejecucion:.6f} segundos")

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
    plt.show()

    if input("\n¿Desea comparar con otros metodos? (s/n): ").strip().lower() == 's':
        ILG = supCp3.SUBinterpol_lagrange.interpol_lagrange(x,y)
        SPCC = supCp3.SUBspln_cubico.SUBSUBspline_cubico(x,y)
        SPL = supCp3.SUBspline_lineal.SUBSUBspline_lineal(x,y)
        VAN = supCp3.Subvandermonde.interpol_vandermonde(x,y)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'ro', label='Puntos dados')
        plt.plot(x_plot, y_newton, 'b-', label='Newton')
        plt.plot(SPL[0], SPL[1], 'g--', label='Pline lineal')
        plt.plot(ILG[0],ILG[1], 'm--', label='Lagrange')
        plt.plot(VAN[0], VAN[1], 'k-', label='Vandermonde')
        plt.plot(SPCC[0], SPCC[1], 'y--', label='Spline Cubico')
        plt.title("Comparacion General")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show()
        print("comparacion general")

# Ejecutar
interpolacion_newton()