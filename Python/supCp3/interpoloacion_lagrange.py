import numpy as np
import time
import matplotlib.pyplot as plt

def interpolacion_lagrange():
    print("=== INTERPOLACIÓN DE LAGRANGE ===")
    print("Incluye el polinomio resultante, tiempo de ejecución y gráfica.\n")
    
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

# Ejecutar
interpolacion_lagrange()