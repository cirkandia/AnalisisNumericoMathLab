import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from tabulate import tabulate
import importlib
import inspect

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
    "vandermonde" : ("Vandermonde", "interpolacion_vandermonde"),
}

# Ruta base donde están los scripts
MODULE_PATH = "Python"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos")
        self.geometry("400x500")
        self.method_var = tk.StringVar()
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Seleccione un Método", font=("Arial", 16)).pack(pady=20)

        for name in METHODS:
            tk.Button(self, text=name, width=30, command=lambda m=name: self.load_method_form(m)).pack(pady=5)

    def load_method_form(self, method_name):
        method_info = METHODS[method_name]

        if isinstance(method_info, tuple):
            module_name, function_name = method_info
        else:
            module_name = function_name = method_info

        try:
            module = importlib.import_module(f"{MODULE_PATH}.{module_name}")
            func = getattr(module, function_name)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el método: {e}")
            return

        self.show_input_form(method_name, func)

    def show_input_form(self, method_name, func):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=f"{method_name} - Parámetros", font=("Arial", 14)).pack(pady=10)

        entries = {}

        # Campo especial para la función f(x)
        tk.Label(self, text="f(x) =").pack()
        f_entry = tk.Entry(self)
        f_entry.pack(pady=5)

        # Inspeccionamos parámetros (ignoramos 'f' si está primero)
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        if params and params[0] == 'f':
            params = params[1:]
            use_f = True
        else:
            use_f = False

        for param in params:
            tk.Label(self, text=param).pack()
            entry = tk.Entry(self)
            entry.pack(pady=2)
            entries[param] = entry

        def execute():
            try:
                args = []

                if use_f:
                    f_str = f_entry.get()
                    f = lambda x: eval(f_str, {"np": np, "x": x})
                    args.append(f)

                for param in params:
                    value = float(entries[param].get())
                    args.append(value)

                result = func(*args)
                self.show_result(method_name, result)

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self, text="Ejecutar", command=execute).pack(pady=20)
        tk.Button(self, text="Volver", command=self.show_main_menu).pack()

    def show_result(self, method_name, result):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=f"Resultados - {method_name}", font=("Arial", 14)).pack(pady=10)

        text = tk.Text(self, wrap="word", height=20, width=50)
        text.pack(padx=10, pady=10)

        if isinstance(result, tuple) and isinstance(result[-1], list):
            try:
                table = tabulate(result[-1], headers="keys" if isinstance(result[-1][0], dict) else "firstrow", tablefmt="grid")
                text.insert("1.0", table)
            except Exception:
                text.insert("1.0", str(result))
        else:
            text.insert("1.0", str(result))

        tk.Button(self, text="Volver al inicio", command=self.show_main_menu).pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()