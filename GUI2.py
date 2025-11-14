import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from tabulate import tabulate
import importlib
import inspect
import pandas as pd
import math

from Python.Vandermonde import comparar_metodos

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Diccionario de métodos con información completa
METHODS = {
    "Bisección": {
        "module": ("biseccion", "biseccion"),
        "description": "Encuentra la raíz de una función en un intervalo dado mediante división sucesiva del intervalo.",
        "required_inputs": [
            "Función f(x)",
            "Límite inferior (a)",
            "Límite superior (b)",
            "Tolerancia (Tol)",
            "Máximo iteraciones (it)"
        ],
        "example": "f(x) = x**3 - x - 1, a = 1, b = 2, Tol = 0.01, it = 100"
    },
    "Regla Falsa": {
        "module": ("regla_falsa", "false_position_method"),
        "description": "Método de aproximación lineal para encontrar raíces, similar a bisección pero más eficiente.",
        "required_inputs": ["Función f(x)", "Límite inferior (a)", "Límite superior (b)", "Tolerancia", "Máximo iteraciones"],
        "example": "f(x) = x**2 - 2, a = 0, b = 2"
    },
    "Newton": {
        "module": ("newton", "newton_method"),
        "description": "Utiliza la tangente a la curva para aproximar la raíz mediante derivadas.",
        "required_inputs": ["Función f(x)", "Valor inicial (x0)", "Tolerancia", "Máximo iteraciones"],
        "example": "f(x) = x**2 - 2, x0 = 1.5"
    },
    "Secante": {
        "module": ("secante", "secante"),
        "description": "Aproxima la derivada usando dos puntos iniciales, no requiere calcular derivadas.",
        "required_inputs": ["Función f(x)", "Primer valor inicial (x0)", "Segundo valor inicial (x1)", "Tolerancia", "Máximo iteraciones"],
        "example": "f(x) = x**3 - 2, x0 = 1, x1 = 2"
    },
    "Punto Fijo": {
        "module": ("puntofijo", "fixed_point_iteration"),
        "description": "Encuentra puntos donde f(x) = x mediante iteración de una función g(x).",
        "required_inputs": ["Función g(x)", "Valor inicial (x0)", "Tolerancia", "Máximo iteraciones"],
        "example": "g(x) = (x + 2/x)/2, x0 = 1"
    },
    "Raíces Múltiples": {
        "module": ("raices_m", "multiple_roots"),
        "description": "Encuentra raíces de multiplicidad mayor a 1 usando primera y segunda derivada.",
        "required_inputs": ["Función f(x)", "Valor inicial (x0)", "Tolerancia", "Máximo iteraciones"],
        "example": "f(x) = (x-1)^2, x0 = 0.5"
    },
    "Jacobi": {
        "module": ("jacobi", "jacobi"),
        "description": "Resuelve sistemas de ecuaciones lineales mediante iteración usando matriz diagonal.",
        "required_inputs": ["Matriz A", "Vector b", "Vector inicial x0", "Tolerancia", "Máximo iteraciones"],
        "example": "Sistema: 3x + y = 5, x + 2y = 4"
    },
    "Gauss-Seidel": {
        "module": ("gauss_seidel", "gauss_seidel_method"),
        "description": "Mejora del método Jacobi, usa valores actualizados inmediatamente.",
        "required_inputs": ["Matriz A", "Vector b", "Vector inicial x0", "Tolerancia", "Máximo iteraciones"],
        "example": "Sistema: 4x + y = 7, x + 3y = 8"
    },
    "SOR": {
        "module": ("SOR", "sor_method"),
        "description": "Método de sobre-relajación sucesiva, generalización de Gauss-Seidel con factor w.",
        "required_inputs": ["Matriz A", "Vector b", "Vector inicial x0", "Factor w", "Tolerancia", "Máximo iteraciones"],
        "example": "Sistema con w = 1.2 para acelerar convergencia"
    },
    "Vandermonde": {
        "module": ("Vandermonde", "interpolacion_vandermonde"),
        "description": "Interpolación polinomial usando matriz de Vandermonde.",
        "required_inputs": ["ValoresX", "ValoresY"],
        "example": "X: 1,2,3 \n Y: 2,4,5 \n dando (1,2), (2,4), (3,5) como puntos de interpolación"
    },
    "Interpolación Newton": {
        "module": ("interpolacion_newton", "interpolacion_newton"),
        "description": "Interpolación usando diferencias divididas de Newton.",
        "required_inputs": ["Puntos x", "Valores y", "Punto a evaluar"],
        "example": "X: 1,2,3 \n Y: 2,4,5 \n dando (1,2), (2,4), (3,5) como puntos de interpolación"
    },
    "Spline Lineal": {
        "module": ("spline_lineal", "spline_lineal_con_polinomios"),
        "description": "Interpolación lineal por tramos.",
        "required_inputs": ["Puntos x", "Valores y"],
        "example": "X: 1,2,3 \n Y: 2,4,5 \n dando (1,2), (2,4), (3,5) como puntos de interpolación"
    },
    "Spline Cúbico": {
        "module": ("spline_cubico", "spline_cubico"),
        "description": "Interpolación cúbica por tramos.",
        "required_inputs": ["Puntos x", "Valores y"],
        "example": "X: 1,2,3 \n Y: 2,4,5 \n dando (1,2), (2,4), (3,5) como puntos de interpolación"
    },
    "Interpolación Lagrange": {
        "module": ("interpolacion_lagrange", "interpolacion_lagrange"),
        "description": "Interpolación usando el polinomio de Lagrange.",
        "required_inputs": ["Puntos x", "Valores y"],
        "example": "X: 1,2,3 \n Y: 2,4,5 \n dando (1,2), (2,4), (3,5) como puntos de interpolación"
    }
}

# Traducción de parámetros comunes
SPANISH_PARAMS = {
    "x0": "Valor inicial (x0)",
    "x1": "Segundo valor inicial (x1)",
    "lower_bound": "Límite inferior (a)",
    "upper_bound": "Límite superior (b)",
    "tolerance": "Tolerancia",
    "max_iterations": "Máximo de iteraciones",
    "error_type": "Tipo de error (abs/rel)",
    "w": "Factor de relajación (w)",
    "A": "Matriz A (separar filas con ;)",
    "b": "Vector b (separar con ,)",
    "x_points": "Puntos x (separar con ,)",
    "y_points": "Puntos y (separar con ,)",
    "eval_point": "Punto a evaluar"
}

MODULE_PATH = "Python"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Análisis Numérico - Métodos Computacionales")
        self.geometry("800x700")
        self.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.method_var = tk.StringVar()
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title = tk.Label(main_frame, text="MÉTODOS NUMÉRICOS",
                         font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=(0, 10))

        subtitle = tk.Label(main_frame, text="Seleccione el método a utilizar",
                            font=("Arial", 12), bg='#f0f0f0', fg='#7f8c8d')
        subtitle.pack(pady=(0, 20))

        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack()

        categories = {
            "Ecuaciones No Lineales": ["Bisección", "Regla Falsa", "Newton", "Secante", "Punto Fijo", "Raíces Múltiples"],
            "Sistemas Lineales": ["Jacobi", "Gauss-Seidel", "SOR"],
            "Interpolación": ["Vandermonde", "Interpolación Newton", "Interpolación Lagrange", "Spline Lineal", "Spline Cúbico"]
        }

        for i, (category, methods) in enumerate(categories.items()):
            cat_label = tk.Label(button_frame, text=category,
                                 font=("Arial", 14, "bold"), bg='#f0f0f0', fg='#34495e')
            cat_label.grid(row=i * 10, column=0, columnspan=2, pady=(15, 5), sticky='w')

            for j, method in enumerate(methods):
                if method in METHODS:
                    btn = tk.Button(
                        button_frame,
                        text=method,
                        width=25, height=2,
                        font=("Arial", 10), bg='#3498db', fg='white',
                        activebackground='#2980b9', cursor='hand2',
                        command=lambda m=method: self.show_method_info(m)
                    )
                    btn.grid(row=i * 10 + 1 + j // 2, column=j % 2, padx=5, pady=2, sticky='ew')

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def show_method_info(self, method_name):
        for widget in self.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title = tk.Label(main_frame, text=f"MÉTODO: {method_name.upper()}",
                         font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=(0, 15))

        method_info = METHODS[method_name]

        desc_frame = tk.LabelFrame(main_frame, text="Descripción", font=("Arial", 12, "bold"),
                                   bg='#f0f0f0', fg='#2c3e50', padx=10, pady=10)
        desc_frame.pack(fill='x', pady=(0, 15))

        desc_label = tk.Label(desc_frame, text=method_info["description"],
                              font=("Arial", 10), bg='#f0f0f0', wraplength=600, justify='left')
        desc_label.pack()

        req_frame = tk.LabelFrame(main_frame, text="Datos Requeridos", font=("Arial", 12, "bold"),
                                  bg='#f0f0f0', fg='#2c3e50', padx=10, pady=10)
        req_frame.pack(fill='x', pady=(0, 15))

        for req in method_info["required_inputs"]:
            tk.Label(req_frame, text=f"• {req}", font=("Arial", 10),
                     bg='#f0f0f0', fg='#2c3e50').pack(anchor='w')

        example_frame = tk.LabelFrame(main_frame, text="Ejemplo", font=("Arial", 12, "bold"),
                                      bg='#f0f0f0', fg='#2c3e50', padx=10, pady=10)
        example_frame.pack(fill='x', pady=(0, 20))

        example_label = tk.Label(example_frame, text=method_info["example"],
                                 font=("Arial", 10, "italic"), bg='#f0f0f0', fg='#7f8c8d')
        example_label.pack()

        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack()

        tk.Button(button_frame, text="Continuar", font=("Arial", 12, "bold"),
                  bg='#27ae60', fg='white', padx=20, pady=5, cursor='hand2',
                  command=lambda: self.load_method_form(method_name)).pack(side='left', padx=10)

        tk.Button(button_frame, text="Volver", font=("Arial", 12),
                  bg='#95a5a6', fg='white', padx=20, pady=5, cursor='hand2',
                  command=self.show_main_menu).pack(side='left')

    def load_method_form(self, method_name):
        method_info = METHODS[method_name]["module"]
        package = METHODS[method_name].get("package", "")

        if isinstance(method_info, tuple):
            module_name, function_name = method_info
        else:
            module_name = function_name = method_info

        if package:
            full_module = f"Python.{package}.{module_name}"
        else:
            full_module = f"Python.{module_name}"

        try:
            module = importlib.import_module(full_module)
            func = getattr(module, function_name)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el método: {e}")
            return

        self.show_input_form(method_name, func)

    def show_input_form(self, method_name, func):
        for widget in self.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title = tk.Label(main_frame, text=f"{method_name} - Ingreso de Parámetros",
                         font=("Arial", 14, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=(0, 20))

        input_frame = tk.LabelFrame(main_frame, text="Parámetros", font=("Arial", 12, "bold"),
                                    bg='#f0f0f0', fg='#2c3e50', padx=15, pady=15)
        input_frame.pack(fill='x', pady=(0, 20))

        entries = {}

        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        use_f = params and params[0] == 'f'

        SKIP_PARAMS = {'show_report', 'eval_grid', 'auto_compare'}
        params = [p for p in params if p not in SKIP_PARAMS]

        if use_f:
            tk.Label(input_frame, text="Función f(x) =", font=("Arial", 10, "bold"),
                     bg='#f0f0f0', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=5)
            f_entry = tk.Entry(input_frame, width=50, font=("Arial", 10))
            f_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='ew')

            tk.Label(input_frame, text="Ej: x**2 - 2, np.sin(x), x**3 - x - 1",
                     font=("Arial", 8), bg='#f0f0f0', fg='#7f8c8d').grid(row=1, column=1, sticky='w')

            params = params[1:]

        row = 2
        for param in params:
            label = SPANISH_PARAMS.get(param, param)
            tk.Label(input_frame, text=f"{label}:", font=("Arial", 10, "bold"),
                     bg='#f0f0f0', fg='#2c3e50').grid(row=row, column=0, sticky='w', pady=5)
            entry = tk.Entry(input_frame, width=50, font=("Arial", 10))
            entry.grid(row=row, column=1, padx=(10, 0), pady=5, sticky='ew')
            entries[param] = entry
            row += 1

        input_frame.grid_columnconfigure(1, weight=1)

        self.last_called_show_report = False
        auto_cmp_var = tk.BooleanVar(value=True)
        eval_grid_var = tk.StringVar(value='500')

        opts_frame = tk.Frame(main_frame, bg='#f0f0f0')
        opts_frame.pack(fill='x', pady=(0, 10))
        tk.Checkbutton(opts_frame, text='Comparación automática', variable=auto_cmp_var,
                       bg='#f0f0f0').pack(side='left', padx=(0, 10))
        tk.Label(opts_frame, text='Eval grid:', bg='#f0f0f0').pack(side='left')
        tk.Entry(opts_frame, textvariable=eval_grid_var, width=6).pack(side='left', padx=(5, 0))

        def execute():
            try:
                args = []

                # reset valores para graficar
                self.last_function_str = None
                self.last_a = None
                self.last_b = None

                if use_f:
                    f_str = f_entry.get()
                    if not f_str.strip():
                        messagebox.showerror("Error", "Debe ingresar una función f(x)")
                        return

                    self.last_function_str = f_str

                    f = lambda x: eval(f_str, {
                        "np": np, "x": x, "math": math,
                        "sin": np.sin, "cos": np.cos, "tan": np.tan,
                        "exp": np.exp, "log": np.log, "sqrt": np.sqrt
                    })
                    args.append(f)

                x_vals = None
                y_vals = None

                for param in params:
                    val = entries[param].get().strip()
                    if not val:
                        messagebox.showerror("Error", f"Debe ingresar un valor para {SPANISH_PARAMS.get(param, param)}")
                        return

                    # guardar [a,b] para graficar en métodos de intervalo
                    if param == "lower_bound":
                        self.last_a = float(val)
                    elif param == "upper_bound":
                        self.last_b = float(val)

                    if param in ["max_iterations", "n_iter", "iteraciones"]:
                        try:
                            args.append(int(val))
                        except ValueError:
                            messagebox.showerror("Error", f"{SPANISH_PARAMS.get(param, param)} debe ser un número entero")
                            return
                    elif param.lower() in ["x_points", "puntos x", "valoresx"]:
                        x_vals = [float(x.strip()) for x in val.split(',') if x.strip() != ""]
                    elif param.lower() in ["y_points", "valores y", "valoresy"]:
                        y_vals = [float(y.strip()) for y in val.split(',') if y.strip() != ""]
                    elif param == "error_type":
                        args.append(val)
                    elif param == "A":
                        rows = val.split(';')
                        matrix = []
                        for row_ in rows:
                            matrix.append([float(x.strip()) for x in row_.split(',')])
                        args.append(np.array(matrix))
                    elif param == "b":
                        vector = [float(x.strip()) for x in val.split(',')]
                        args.append(np.array(vector))
                    else:
                        try:
                            args.append(float(val))
                        except ValueError:
                            args.append(val)

                if x_vals is not None and y_vals is not None:
                    self.ultimo_x = x_vals
                    self.ultimo_y = y_vals
                    args = [x_vals, y_vals] + args

                kwargs = {}
                try:
                    f_sig = inspect.signature(func)
                    if 'show_report' in f_sig.parameters:
                        kwargs['show_report'] = True
                        if 'eval_grid' in f_sig.parameters:
                            try:
                                kwargs['eval_grid'] = int(eval_grid_var.get())
                            except Exception:
                                kwargs['eval_grid'] = 500
                        if 'auto_compare' in f_sig.parameters:
                            kwargs['auto_compare'] = bool(auto_cmp_var.get())
                except Exception:
                    pass

                result = func(*args, **kwargs)
                self.last_called_show_report = bool(kwargs.get('show_report', False))
                self.show_result(method_name, result)

            except Exception as e:
                messagebox.showerror("Error", f"Error en la ejecución: {str(e)}")

        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Ejecutar Método", font=("Arial", 12, "bold"),
                  bg='#27ae60', fg='white', padx=20, pady=8, cursor='hand2',
                  command=execute).pack(side='left', padx=10)

        tk.Button(button_frame, text="Volver", font=("Arial", 12),
                  bg='#95a5a6', fg='white', padx=20, pady=8, cursor='hand2',
                  command=lambda: self.show_method_info(method_name)).pack(side='left')

    def show_result(self, method_name, result):
        for widget in self.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title = tk.Label(main_frame, text=f"RESULTADOS - {method_name.upper()}",
                         font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=(0, 20))

        result_frame = tk.LabelFrame(main_frame, text="Resultados del Método",
                                     font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#2c3e50')
        result_frame.pack(fill='both', expand=True, pady=(0, 20))

        if self.is_tabular_result(result):
            self.create_result_table(result_frame, result, method_name)
        else:
            text_widget = scrolledtext.ScrolledText(result_frame, height=20, width=80,
                                                    font=("Courier", 10), bg='white')
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            text_widget.insert('1.0', str(result))
            text_widget.config(state='disabled')

        if method_name in ["Vandermonde", "spline_lineal", "spline_cubico",
                           "interpolacion_lagrange", "interpolacion_newton"] \
                and not getattr(self, 'last_called_show_report', False):
            if messagebox.askyesno("Comparar", "¿Desea comparar con otros métodos de interpolación?"):
                comparar_metodos(self.ultimo_x, self.ultimo_y)

        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack()

        graficables = [
            "Bisección",
            "Regla Falsa",
            "Punto Fijo",
            "Newton",
            "Secante",
            "Raíces Múltiples"
        ]

        if method_name in graficables:
            tk.Button(
                button_frame,
                text="Graficar",
                font=("Arial", 12, "bold"),
                bg='#e67e22', fg='white',
                padx=20, pady=8, cursor='hand2',
                command=lambda m=method_name: self.plot_root_method(m, result)
            ).pack(side='left', padx=10)

        tk.Button(button_frame, text="Nuevo Cálculo", font=("Arial", 12, "bold"),
                  bg='#3498db', fg='white', padx=20, pady=8, cursor='hand2',
                  command=lambda: self.show_method_info(method_name)).pack(side='left', padx=10)

        tk.Button(button_frame, text="Menú Principal", font=("Arial", 12),
                  bg='#95a5a6', fg='white', padx=20, pady=8, cursor='hand2',
                  command=self.show_main_menu).pack(side='left')

    def is_tabular_result(self, result):
        if isinstance(result, tuple) and len(result) >= 2:
            last_element = result[-1]
            return (isinstance(last_element, list) and len(last_element) > 0) or \
                   (isinstance(last_element, dict) and len(last_element) > 0)
        if isinstance(result, dict) and len(result) > 0:
            return True
        return isinstance(result, list) and len(result) > 0

    def create_result_table(self, parent_frame, result, method_name):
        table_data = None
        header_text = None
        if isinstance(result, tuple):
            header_text = "\n".join([str(r) for r in result[:-1]]) if len(result) > 1 else None
            table_data = result[-1]
        elif isinstance(result, dict):
            table_data = result
        else:
            table_data = result

        if header_text:
            info_text = scrolledtext.ScrolledText(parent_frame, height=4, width=80,
                                                  font=("Courier", 10), bg='#ecf0f1')
            info_text.pack(fill='x', padx=10, pady=(10, 5))
            info_text.insert('1.0', header_text)
            info_text.config(state='disabled')

        table_frame = tk.Frame(parent_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        if isinstance(table_data, dict):
            columns = ["Propiedad", "Valor"]
            rows_iter = [(k, table_data[k]) for k in table_data]
        elif isinstance(table_data, list) and len(table_data) > 0 and isinstance(table_data[0], dict):
            columns = list(table_data[0].keys())
            rows_iter = [tuple(row.get(col, '') for col in columns) for row in table_data]
        elif isinstance(table_data, list) and len(table_data) > 0 and isinstance(table_data[0], list):
            if method_name == "Bisección" and len(table_data[0]) == 8:
                columns = ["Iteración", "a", "f(a)", "pm", "f(pm)", "b", "f(b)", "Error Abs."]
            else:
                columns = [f"Col_{i+1}" for i in range(len(table_data[0]))]
            rows_iter = table_data
        else:
            columns = ["Elemento"]
            rows_iter = [(str(r),) for r in table_data] if isinstance(table_data, list) else [(str(table_data),)]

        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        for col in columns:
            tree.heading(col, text=col.replace('_', ' ').title())
            tree.column(col, width=120, anchor='center')

        for row in rows_iter:
            if isinstance(row, dict):
                values = [str(row.get(col, '')) for col in columns]
            elif isinstance(row, (list, tuple)):
                values = [str(val) for val in row]
            else:
                values = [str(row)]
            tree.insert('', 'end', values=values)

        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        summary_frame = tk.Frame(parent_frame, bg='#f0f0f0')
        summary_frame.pack(fill='x', padx=10, pady=5)

        if isinstance(table_data, dict):
            tk.Label(summary_frame, text=f"Propiedades: {len(table_data)}",
                     font=("Arial", 10, "bold"), bg='#f0f0f0', fg='#2c3e50').pack(side='left')
        elif isinstance(table_data, list):
            tk.Label(summary_frame, text=f"Filas: {len(table_data)}",
                     font=("Arial", 10, "bold"), bg='#f0f0f0', fg='#2c3e50').pack(side='left')
        else:
            tk.Label(summary_frame, text="Resultado",
                     font=("Arial", 10, "bold"), bg='#f0f0f0', fg='#2c3e50').pack(side='left')

        poly_keys = ['polinomio_str', 'polinomios_por_tramo', 'polinomios_base']
        has_poly = False
        poly_text = None
        if isinstance(table_data, dict):
            for k in poly_keys:
                if k in table_data and table_data[k]:
                    has_poly = True
                    if k in ['polinomios_por_tramo', 'polinomios_base']:
                        entries = table_data[k]
                        if isinstance(entries, (list, tuple)):
                            poly_text = "\n\n".join(str(e) for e in entries)
                            break
                    else:
                        poly_text = str(table_data[k])
                        break

        if has_poly and poly_text:
            btn_frame = tk.Frame(parent_frame, bg='#f0f0f0')
            btn_frame.pack(fill='x', padx=10, pady=(0, 10))
            tk.Button(btn_frame, text="Ver polinomio(s) completos", font=("Arial", 10, "bold"),
                      bg='#8e44ad', fg='white', padx=10, pady=4, cursor='hand2',
                      command=lambda txt=poly_text: self.show_polynomials_modal(txt)).pack(side='right')

    def show_polynomials_modal(self, pol_text):
        modal = tk.Toplevel(self)
        modal.title("Polinomio(s) completos")
        modal.geometry("700x500")

        txt = scrolledtext.ScrolledText(modal, wrap='none', font=("Courier", 10))
        txt.pack(fill='both', expand=True, padx=10, pady=10)
        txt.insert('1.0', pol_text)
        txt.config(state='disabled')

        def copy_all():
            self.clipboard_clear()
            self.clipboard_append(pol_text)
            messagebox.showinfo("Copiado", "Polinomio(s) copiado(s) al portapapeles.")

        btn_frame = tk.Frame(modal)
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))
        tk.Button(btn_frame, text="Copiar todo", command=copy_all,
                  bg='#3498db', fg='white').pack(side='right')

    def plot_root_method(self, method_name, result):
        """Grafica f(x) y la sucesión de aproximaciones x_n para varios métodos de raíces."""

        if not hasattr(self, 'last_function_str') or self.last_function_str is None:
            messagebox.showerror("Error", "No se encontró la función para graficar.")
            return

        func_str = self.last_function_str

        def f(x):
            return eval(func_str, {
                "np": np, "x": x, "math": math,
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "exp": np.exp, "log": np.log, "sqrt": np.sqrt
            })

        table_data = result[-1] if isinstance(result, tuple) else result
        if not isinstance(table_data, list) or len(table_data) == 0:
            messagebox.showerror("Error", "No hay datos de iteraciones para graficar.")
            return

        # Ajusta estos índices según la forma de tus tablas:
        # Bisección: [iter, a, f(a), pm, f(pm), b, f(b), err]          -> x_n = pm (3)
        # Regla Falsa: [iter, a, f(a), b, f(b), xr, f(xr), err]       -> x_n = xr (5)
        # Newton: [iter, x, f(x), f'(x), err]                         -> x_n = x  (1)
        # Secante: [iter, x_{i-1}, x_i, f(x_i), err]                  -> x_n = x_i (2)
        # Punto Fijo: [iter, x, g(x), err]                            -> x_n = x  (1)
        # Raíces Múltiples: [iter, x, f, f', f'', err]                -> x_n = x  (1)
        x_col_map = {
            "Bisección": 3,
            "Regla Falsa": 5,
            "Newton": 1,
            "Secante": 2,
            "Punto Fijo": 1,
            "Raíces Múltiples": 1
        }

        if method_name not in x_col_map:
            messagebox.showerror("Error", f"No se ha configurado graficación para el método: {method_name}")
            return

        x_col = x_col_map[method_name]

        try:
            x_aprox = [row[x_col] for row in table_data]
        except Exception:
            messagebox.showerror("Error", "No se pudo extraer la columna de aproximaciones x_n.\nRevisa el formato de la tabla.")
            return

        # Intervalo para graficar
        if method_name in ["Bisección", "Regla Falsa"] and \
           hasattr(self, 'last_a') and hasattr(self, 'last_b') and \
           self.last_a is not None and self.last_b is not None:
            a = self.last_a
            b = self.last_b
        else:
            xmin = min(x_aprox)
            xmax = max(x_aprox)
            if xmin == xmax:
                a = xmin - 1
                b = xmax + 1
            else:
                margen = (xmax - xmin) * 0.4
                a = xmin - margen
                b = xmax + margen

        xs = np.linspace(a, b, 400)
        ys = [f(x) for x in xs]

        win = tk.Toplevel(self)
        win.title(f"Gráfica - Método de {method_name}")
        win.geometry("700x500")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.axhline(0, color='black', linewidth=0.8)
        ax.plot(xs, ys, label='f(x)')

        try:
            ax.scatter(x_aprox, [f(x) for x in x_aprox],
                       color='red', marker='o', label='Aproximaciones x_n')
        except Exception:
            pass

        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'Método de {method_name}')
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
