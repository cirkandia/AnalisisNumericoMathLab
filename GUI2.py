import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from tabulate import tabulate
import importlib
import inspect
import pandas as pd

# Diccionario de métodos con información completa
METHODS = {
    "Bisección": {
        "module": ("biseccion", "biseccion"),
        "description": "Encuentra la raíz de una función en un intervalo dado mediante división sucesiva del intervalo.",
        "required_inputs": ["Función f(x)", "Límite inferior (a)", "Límite superior (b)", "Tolerancia", "Máximo iteraciones"],
        "example": "f(x) = x^3 - x - 1, a = 1, b = 2"
    },
    "Regla Falsa": {
        "module": ("regla_falsa", "false_position_method"),
        "description": "Método de aproximación lineal para encontrar raíces, similar a bisección pero más eficiente.",
        "required_inputs": ["Función f(x)", "Límite inferior (a)", "Límite superior (b)", "Tolerancia", "Máximo iteraciones"],
        "example": "f(x) = x^2 - 2, a = 0, b = 2"
    },
    "Newton": {
        "module": ("newton", "newton_method"),
        "description": "Utiliza la tangente a la curva para aproximar la raíz mediante derivadas.",
        "required_inputs": ["Función f(x)", "Valor inicial (x0)", "Tolerancia", "Máximo iteraciones"],
        "example": "f(x) = x^2 - 2, x0 = 1.5"
    },
    "Secante": {
        "module": ("secante", "secante"),
        "description": "Aproxima la derivada usando dos puntos iniciales, no requiere calcular derivadas.",
        "required_inputs": ["Función f(x)", "Primer valor inicial (x0)", "Segundo valor inicial (x1)", "Tolerancia", "Máximo iteraciones"],
        "example": "f(x) = x^3 - 2, x0 = 1, x1 = 2"
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
            "required_inputs": ["Puntos x", "Valores y"],
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

# Ruta base donde están los scripts
MODULE_PATH = "Python"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Análisis Numérico - Métodos Computacionales")
        self.geometry("800x700")
        self.configure(bg='#f0f0f0')
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.method_var = tk.StringVar()
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        title = tk.Label(main_frame, text="MÉTODOS NUMÉRICOS", 
                        font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=(0, 10))

        subtitle = tk.Label(main_frame, text="Seleccione el método a utilizar", 
                           font=("Arial", 12), bg='#f0f0f0', fg='#7f8c8d')
        subtitle.pack(pady=(0, 20))

        # Frame para botones
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack()

        # Crear botones organizados en categorías
        categories = {
            "Ecuaciones No Lineales": ["Bisección", "Regla Falsa", "Newton", "Secante", "Punto Fijo", "Raíces Múltiples"],
            "Sistemas Lineales": ["Jacobi", "Gauss-Seidel", "SOR"],
            "Interpolación": ["Vandermonde", "Interpolación Newton", "Interpolación Lagrange", "Spline Lineal", "Spline Cúbico"]
        }

        for i, (category, methods) in enumerate(categories.items()):
            # Etiqueta de categoría
            cat_label = tk.Label(button_frame, text=category, 
                               font=("Arial", 14, "bold"), bg='#f0f0f0', fg='#34495e')
            cat_label.grid(row=i*10, column=0, columnspan=2, pady=(15, 5), sticky='w')

            # Botones de métodos
            for j, method in enumerate(methods):
                if method in METHODS:
                    btn = tk.Button(button_frame, text=method, width=25, height=2,
                                  font=("Arial", 10), bg='#3498db', fg='white',
                                  activebackground='#2980b9', cursor='hand2',
                                  command=lambda m=method: self.show_method_info(m))
                    btn.grid(row=i*10+1+j//2, column=j%2, padx=5, pady=2, sticky='ew')

        # Configurar grid
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def show_method_info(self, method_name):
        """Muestra información del método antes de cargar el formulario"""
        for widget in self.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título del método
        title = tk.Label(main_frame, text=f"MÉTODO: {method_name.upper()}", 
                        font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=(0, 15))

        # Información del método
        method_info = METHODS[method_name]
        
        # Descripción
        desc_frame = tk.LabelFrame(main_frame, text="Descripción", font=("Arial", 12, "bold"),
                                  bg='#f0f0f0', fg='#2c3e50', padx=10, pady=10)
        desc_frame.pack(fill='x', pady=(0, 15))
        
        desc_label = tk.Label(desc_frame, text=method_info["description"], 
                             font=("Arial", 10), bg='#f0f0f0', wraplength=600, justify='left')
        desc_label.pack()

        # Datos requeridos
        req_frame = tk.LabelFrame(main_frame, text="Datos Requeridos", font=("Arial", 12, "bold"),
                                 bg='#f0f0f0', fg='#2c3e50', padx=10, pady=10)
        req_frame.pack(fill='x', pady=(0, 15))

        for i, req in enumerate(method_info["required_inputs"]):
            tk.Label(req_frame, text=f"• {req}", font=("Arial", 10), 
                    bg='#f0f0f0', fg='#2c3e50').pack(anchor='w')

        # Ejemplo
        example_frame = tk.LabelFrame(main_frame, text="Ejemplo", font=("Arial", 12, "bold"),
                                     bg='#f0f0f0', fg='#2c3e50', padx=10, pady=10)
        example_frame.pack(fill='x', pady=(0, 20))
        
        example_label = tk.Label(example_frame, text=method_info["example"], 
                               font=("Arial", 10, "italic"), bg='#f0f0f0', fg='#7f8c8d')
        example_label.pack()

        # Botones
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

        # Título
        title = tk.Label(main_frame, text=f"{method_name} - Ingreso de Parámetros", 
                        font=("Arial", 14, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=(0, 20))

        # Frame para entradas
        input_frame = tk.LabelFrame(main_frame, text="Parámetros", font=("Arial", 12, "bold"),
                                   bg='#f0f0f0', fg='#2c3e50', padx=15, pady=15)
        input_frame.pack(fill='x', pady=(0, 20))

        entries = {}

        # Inspección de los parámetros
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        use_f = params and params[0] == 'f'

        # Campo para la función f(x)
        if use_f:
            tk.Label(input_frame, text="Función f(x) =", font=("Arial", 10, "bold"),
                    bg='#f0f0f0', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=5)
            f_entry = tk.Entry(input_frame, width=50, font=("Arial", 10))
            f_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='ew')
            
            # Ejemplo de función
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

        # Configurar grid
        input_frame.grid_columnconfigure(1, weight=1)

        def execute():
            try:
                args = []

                if use_f:
                    f_str = f_entry.get()
                    if not f_str.strip():
                        messagebox.showerror("Error", "Debe ingresar una función f(x)")
                        return
                    
                    # Función lambda más robusta
                    f = lambda x: eval(f_str, {
                        "np": np, "x": x, "math": __import__('math'),
                        "sin": np.sin, "cos": np.cos, "tan": np.tan,
                        "exp": np.exp, "log": np.log, "sqrt": np.sqrt
                    })
                    args.append(f)

                for param in params:
                    val = entries[param].get().strip()
                    if not val:
                        messagebox.showerror("Error", f"Debe ingresar un valor para {SPANISH_PARAMS.get(param, param)}")
                        return
                    
                    if param == "error_type":
                        args.append(val)
                    elif param in ["A", "b", "x_points", "y_points"]:
                        # Manejo de matrices y vectores
                        if param == "A":
                            # Matriz: filas separadas por ; y elementos por ,
                            rows = val.split(';')
                            matrix = []
                            for row in rows:
                                matrix.append([float(x.strip()) for x in row.split(',')])
                            args.append(np.array(matrix))
                        else:
                            # Vector: elementos separados por ,
                            vector = [float(x.strip()) for x in val.split(',')]
                            args.append(np.array(vector))
                    else:
                        try:
                            args.append(float(val))
                        except ValueError:
                            args.append(val)

                result = func(*args)
                self.show_result(method_name, result)

            except Exception as e:
                messagebox.showerror("Error", f"Error en la ejecución: {str(e)}")

        # Botones
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

        # Título
        title = tk.Label(main_frame, text=f"RESULTADOS - {method_name.upper()}", 
                        font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=(0, 20))

        # Frame para resultados
        result_frame = tk.LabelFrame(main_frame, text="Resultados del Método", 
                                   font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#2c3e50')
        result_frame.pack(fill='both', expand=True, pady=(0, 20))

        # Crear Treeview para mostrar tabla
        if self.is_tabular_result(result):
            self.create_result_table(result_frame, result)
        else:
            # Mostrar resultado simple
            text_widget = scrolledtext.ScrolledText(result_frame, height=20, width=80, 
                                                  font=("Courier", 10), bg='white')
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            text_widget.insert('1.0', str(result))
            text_widget.config(state='disabled')

        # Botones
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack()

        tk.Button(button_frame, text="Nuevo Cálculo", font=("Arial", 12, "bold"),
                 bg='#3498db', fg='white', padx=20, pady=8, cursor='hand2',
                 command=lambda: self.show_method_info(method_name)).pack(side='left', padx=10)

        tk.Button(button_frame, text="Menú Principal", font=("Arial", 12),
                 bg='#95a5a6', fg='white', padx=20, pady=8, cursor='hand2',
                 command=self.show_main_menu).pack(side='left')

    def is_tabular_result(self, result):
        """Determina si el resultado debe mostrarse como tabla"""
        if isinstance(result, tuple) and len(result) >= 2:
            last_element = result[-1]
            return isinstance(last_element, list) and len(last_element) > 0
        return isinstance(result, list) and len(result) > 0

    def create_result_table(self, parent_frame, result):
        """Crea una tabla organizada para mostrar los resultados"""
        
        # Extraer datos tabulares
        if isinstance(result, tuple):
            table_data = result[-1]
            # Mostrar información adicional si existe
            if len(result) > 1:
                info_text = scrolledtext.ScrolledText(parent_frame, height=4, width=80, 
                                                    font=("Arial", 10), bg='#ecf0f1')
                info_text.pack(fill='x', padx=10, pady=(10, 5))
                
                info_str = "Información adicional:\n"
                for i, item in enumerate(result[:-1]):
                    info_str += f"• {item}\n"
                
                info_text.insert('1.0', info_str)
                info_text.config(state='disabled')
        else:
            table_data = result

        # Frame para la tabla
        table_frame = tk.Frame(parent_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Determinar columnas
        if isinstance(table_data[0], dict):
            columns = list(table_data[0].keys())
        elif isinstance(table_data[0], list):
            columns = [f"Col_{i+1}" for i in range(len(table_data[0]))]
        else:
            columns = ["Iteración", "Valor"]

        # Crear Treeview
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col.replace('_', ' ').title())
            tree.column(col, width=120, anchor='center')

        # Insertar datos
        for i, row in enumerate(table_data):
            if isinstance(row, dict):
                values = [str(row.get(col, '')) for col in columns]
            elif isinstance(row, list):
                values = [str(val) for val in row]
            else:
                values = [str(i+1), str(row)]
            
            tree.insert('', 'end', values=values)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Empaquetar
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Mostrar resumen
        summary_frame = tk.Frame(parent_frame, bg='#f0f0f0')
        summary_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(summary_frame, text=f"Total de iteraciones: {len(table_data)}", 
                font=("Arial", 10, "bold"), bg='#f0f0f0', fg='#2c3e50').pack(side='left')

if __name__ == "__main__":
    app = App()
    app.mainloop()
