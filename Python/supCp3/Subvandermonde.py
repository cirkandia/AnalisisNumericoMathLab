import numpy as np
import time
import matplotlib.pyplot as plt

def interpol_vandermonde(inx,iny):
    x = inx
    y = iny

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
    #a_polyfit = np.polyfit(x, y, n)[::-1]  # polyfit devuelve coeficientes en orden descendente

    # --- Resultados ---

    # --- Gráfica ---
    x_plot = np.linspace(min(x), max(x), 100)
    y_vander = np.polyval(a[::-1], x_plot)  # polyval espera orden descendente
   # y_polyfit = np.polyval(a_polyfit[::-1], x_plot)

    return [x_plot, y_vander,tiempo_ejecucion,cond_num]

# Ejecutar
#interpolacion_vandermonde()