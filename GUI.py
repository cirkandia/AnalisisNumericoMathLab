import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from tabulate import tabulate
import importlib
import inspect
from Python.supCp3 import interpolacion_newton,interpoloacion_lagrange, spline_cubico, SUBspline_lineal, Vandermonde 

# Diccionario de métodos con nombre legible y nombre del módulo + función
METHODS = {
    "Bisección": ("biseccion", "biseccion"),
    "Regla Falsa": ("regla_falsa", "false_position_method"),
    "Newton": ("newton", "newton_method"),
    "Secante": ("secante", "secante"),
    "Punto Fijo": ("puntofijo", "fixed_point_iteration"),
    "Raíces Múltiples": ("raices_m", "multiple_roots"),
    "Jacobi": ("jacobi", "jacobi"),
    "Gauss-Seidel": ("gauss_seidel", "gauss_seidel_method"),
    "SOR": ("SOR", "sor_method"),
    "Gauss con Pivoteo": "gauss_piv",
    ###########################################################
    # Si se agregan Mas metodos aqui hay que revisar el método show_chapter3_menu
    ###########################################################
    "vandermonde" : ("Vandermonde", "interpolacion_vandermonde"),
    "Spline lineal": ("spline_lineal", "spline_lineal_con_polinomios"),
    "Spline cúbico": ("spline_cubico", "spline_cubico"),
    "Interp de Lagrange": ("interpoloacion_lagrange", "interpolacion_lagrange"),
    "Interp de Newton": ("interpolacion_newton", "interpolacion_newton"),
}

# Ruta base donde están los scripts
MODULE_PATH = "Python.supCp3"

# Traducción de parámetros comunes
SPANISH_PARAMS = {
    "x0": "Valor inicial (x0)",
    "x1": "Segundo valor inicial (x1)",
    "lower_bound": "Límite inferior (a)",
    "upper_bound": "Límite superior (b)",
    "tolerance": "Tolerancia",
    "max_iterations": "Máximo de iteraciones",
    "error_type": "Tipo de error (abs/rel)",
    "w": "Factor de relajación (w)"
}

CHAPTER3_METHODS = {"vandermonde" : ("Vandermonde", "interpolacion_vandermonde"),
    "Spline lineal": ("spline_lineal", "spline_lineal_con_polinomios"),
    "Spline cúbico": ("spline_cubico", "spline_cubico"),
    "Interp de Lagrange": ("interpoloacion_lagrange", "interpolacion_lagrange"),
    "Interp de Newton": ("interpolacion_newton", "interpolacion_newton")}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos")
        self.geometry("450x600")
        self.method_var = tk.StringVar()
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Seleccione un Método", font=("Arial", 16)).pack(pady=20)

        # Solo los métodos que NO están en CHAPTER3_METHODS
        for name in [n for n in METHODS if n not in CHAPTER3_METHODS]:
            tk.Button(self, text=name, width=35, command=lambda m=name: self.load_method_form(m, from_chapter3=False)).pack(pady=5)
        tk.Button(self, text="Capitulo 3", width=35, command=self.show_chapter3_menu).pack(pady=5)

    def show_chapter3_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Capítulo 3 - Interpolación", font=("Arial", 16)).pack(pady=20)

        # Solo los métodos de CHAPTER3_METHODS
        for name in CHAPTER3_METHODS:
            tk.Button(self, text=name, width=35, command=lambda m=name: self.load_method_form(m, from_chapter3=True)).pack(pady=5)
        tk.Button(self, text="Volver", width=35, command=self.show_main_menu).pack(pady=20)

    def load_method_form(self, method_name, from_chapter3=False):
        method_info = METHODS[method_name]

        if isinstance(method_info, tuple):
            module_name, function_name = method_info
        else:
            module_name = function_name = method_info

        MODULE_PATHS = ["Python.supCp3", "Python"]

        for base in MODULE_PATHS:
            try:
                module = importlib.import_module(f"{base}.{module_name}")
                func = getattr(module, function_name)
                break
            except Exception:
                func = None
        else:
            messagebox.showerror("Error", f"No se pudo cargar el método '{method_name}' desde ningún módulo.")
            return

        if from_chapter3:
            self.show_input_form_chapter3(method_name, func)
        else:
            self.show_input_form(method_name, func)

    def show_input_form(self, method_name, func):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=f"{method_name} - Parámetros", font=("Arial", 14)).pack(pady=10)

        entries = {}

        # Campo para la función f(x)
        tk.Label(self, text="f(x) =").pack()
        f_entry = tk.Entry(self, width=40)
        f_entry.pack(pady=5)

        # Inspección de los parámetros
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        use_f = params and params[0] == 'f'
        if use_f:
            params = params[1:]

        for param in params:
            label = SPANISH_PARAMS.get(param, param)
            tk.Label(self, text=label).pack()
            entry = tk.Entry(self, width=40)
            entry.pack(pady=2)
            entries[param] = entry

        def execute():
            try:
                args = []

                if use_f:
                    f_str = f_entry.get()
                    f = lambda x: eval(f_str, {"np": np, "x": x, "math": __import__('math')})
                    args.append(f)

                for param in params:
                    val = entries[param].get().strip()
                    if param == "error_type":
                        args.append(val)
                    else:
                        args.append(float(val))

                result = func(*args)
                self.show_result(method_name, result)

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self, text="Ejecutar", command=execute).pack(pady=20)
        tk.Button(self, text="Volver", command=self.show_main_menu).pack()

    def show_input_form_chapter3(self, method_name, func):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=f"{method_name} - Parámetros (Capítulo 3)", font=("Arial", 14)).pack(pady=10)

        entries = {}

        # Entradas para las listas de números
        tk.Label(self, text="Lista de X (ejemplo: 1,2,3,4)").pack()
        x_entry = tk.Entry(self, width=40)
        x_entry.pack(pady=5)

        tk.Label(self, text="Lista de Y (ejemplo: 5,6,7,8)").pack()
        y_entry = tk.Entry(self, width=40)
        y_entry.pack(pady=5)

        def execute():
            try:
                x_str = x_entry.get().strip()
                y_str = y_entry.get().strip()
                # Convierte las cadenas a listas de enteros
                x_vals = [int(val) for val in x_str.split(",") if val.strip() != ""]
                y_vals = [int(val) for val in y_str.split(",") if val.strip() != ""]

                result = func(x_vals, y_vals)
                self.show_result(method_name, result)

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self, text="Ejecutar", command=execute).pack(pady=20)
        tk.Button(self, text="Volver", command=self.show_main_menu).pack()

    def show_result(self, method_name, result):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=f"Resultados - {method_name}", font=("Arial", 14)).pack(pady=10)

        text = tk.Text(self, wrap="word", height=25, width=70)
        text.pack(padx=10, pady=10)

        if isinstance(result, tuple) and isinstance(result[-1], list):
            try:
                table = tabulate(result[-1], headers="keys" if isinstance(result[-1][0], dict) else "firstrow", tablefmt="fancy_grid")
                text.insert("1.0", table)
            except Exception:
                text.insert("1.0", str(result))
        else:
            text.insert("1.0", str(result))

        tk.Button(self, text="Volver al inicio", command=self.show_main_menu).pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
