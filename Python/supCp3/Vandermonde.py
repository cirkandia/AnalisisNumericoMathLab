import numpy as np
import time
import matplotlib.pyplot as plt

def interpolacion_vandermonde():
    print("=== MÉTODO DE VANDERMONDE ===")
    print("Incluye análisis de tiempo, precisión y número de condición.\n")
    
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

    # --- Análisis de tiempo ---
    start_time = time.time()
    
    # Construir matriz de Vandermonde
    V = np.vander(x, increasing=True)
    
    # Calcular número de condición (estabilidad numérica)
    cond_num = np.linalg.cond(V)
    
    # Resolver el sistema
    a = np.linalg.solve(V, y)
    
    end_time = time.time()
    tiempo_ejecucion = end_time - start_time

    # --- Precisión: comparación con numpy.polyfit (referencia) ---
    a_polyfit = np.polyfit(x, y, n)[::-1]  # polyfit devuelve coeficientes en orden descendente
    error = np.linalg.norm(a - a_polyfit)  # Norma de la diferencia

    # --- Resultados ---
    print("\n🔹 RESULTADOS:")
    print(f"- Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")
    print(f"- Número de condición de la matriz: {cond_num:.2e} (valores altos indican inestabilidad)")
    print(f"- Error respecto a numpy.polyfit: {error:.2e} (idealmente cercano a 0)")

    # --- Gráfica ---
    x_plot = np.linspace(min(x), max(x), 100)
    y_vander = np.polyval(a[::-1], x_plot)  # polyval espera orden descendente
    y_polyfit = np.polyval(a_polyfit[::-1], x_plot)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', label='Puntos dados')
    plt.plot(x_plot, y_vander, 'b-', label='Vandermonde')
    #plt.plot(x_plot, y_polyfit, 'g--', label='numpy.polyfit (ref)')
    plt.title("Interpolación con Vandermonde")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid()
    plt.show()

# Ejecutar
interpolacion_vandermonde()