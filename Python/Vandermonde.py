import numpy as np
import time
import matplotlib.pyplot as plt
import supCp3.interpoloacion_lagrange
import supCp3.interpolacion_newton
import supCp3.spline_cubico
import supCp3.SUBspline_lineal
#import supCp3.Vandermonde

def interpolacion_vandermonde(ValoresX=None, ValoresY=None):  #  Parámetros opcionales añadidos
    print(ValoresX, ValoresY)
    print("=== MÉTODO DE VANDERMONDE ===")
    print("Incluye análisis de tiempo, precisión y número de condición.\n")
    
    # Entrada de datos
    if ValoresX is None or ValoresY is None:  #  Lógica para entrada manual/automática
        n = int(input("Ingrese el número de puntos (n+1): ")) - 1
        x = []
        y = []
        print("\nIngrese los puntos (x_i, y_i):")
        for i in range(n + 1):
            #  Validación incremental de x
            while True:
                x_val = float(input(f"x_{i}: "))
                if i > 0 and x_val <= x[-1]:
                    print(f"Error: x debe ser mayor que {x[-1]}")
                    continue
                y_val = float(input(f"y_{i}: "))
                x.append(x_val)
                y.append(y_val)
                break
    else:
        #  Validación para arrays de entrada
        x = np.array(ValoresX)
        y = np.array(ValoresY)
        if not np.all(np.diff(x) > 0):
            raise ValueError("Los valores de x deben estar en orden creciente")

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

    # --- Resultados ---
    print("\n🔹 RESULTADOS:")
    print(f"- Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos")
    print(f"- Número de condición de la matriz: {cond_num:.2e} (valores altos indican inestabilidad)")

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

    if input("\n¿Desea comparar con otros métodos? (s/n): ").strip().lower() == 's':
        ILG=supCp3.interpoloacion_lagrange.interpolacion_lagrange(x,y)
        INT=supCp3.interpolacion_newton.interpolacion_newton(x,y)
        SPCC=supCp3.spline_cubico.spline_cubico(x,y)
        SPL=supCp3.SUBspline_lineal.spline_lineal(x,y)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'ro', label='Puntos dados')
        plt.plot(x_plot, y_vander, 'b-', label='Vandermonde')
        plt.plot(SPL[0], SPL[1], 'g--', label='Pline lineal')
        plt.plot(ILG[0],ILG[1], 'm--', label='Lagrange')
        plt.plot(INT[0], INT[1], 'c--', label='Newton')
        plt.plot(SPCC[0], SPCC[1], 'y--', label='Spline Cubico')
        plt.title("Comparacion General")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show()
        print("comparacion general")
        print("polinomios", SPL[2])
        #print("numero de condicion", SPL[3])

# Ejecutar
interpolacion_vandermonde()
