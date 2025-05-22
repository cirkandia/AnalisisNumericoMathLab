from tabulate import tabulate
import math
import sympy as sp
import re


def conversion(expr):
    expr = re.sub(r'(?<!\w)e', 'E', expr)


    expr = re.sub(r'\bln\b', 'log', expr)

    sympy_expr = sp.sympify(expr)


    converted_expr = str(sympy_expr).replace('E', 'math.exp(1)')


    converted_expr = converted_expr.replace('exp(', 'math.exp(')
    converted_expr = converted_expr.replace('log(', 'math.log(')

    return converted_expr

def C5_raices_mult(f, df, d2f, x0, tol, Nmax,error12):
    
    f = conversion(f)
    df = conversion(df)
    d2f = conversion(d2f)
    
    def evaluate_expression(x):
        return eval(f)
    def evaluate_expression2(x):
        return eval(df)
    def evaluate_expression3(x):
        return eval(d2f)
    
    xant = x0
    fant = evaluate_expression(xant)
    cont = 0
    matriz = []
   
     

    while True:

        dfx = evaluate_expression2(xant)
        d2fx = evaluate_expression3(xant)
        
        denom = (dfx)**2 - fant * d2fx
        if denom == 0:
            print("Error: division by zero")
            break
        
        xact = xant - fant * dfx / denom
        Eabs=abs(xact-xant)
        err=Eabs/xact
         
        fact = evaluate_expression(xact)
         
         
        
        if error12=="rela":
            if xant != 0:
                E=Eabs/xact
                 
           
            else:
                print("Error: division by zero")
                E= float('inf')
                err=float('inf')
        
        else:
            E=Eabs
         
        matriz.append([cont, xant, fant, dfx, d2fx, Eabs, err])
        xant = xact
        fant = fact
        cont += 1
        if E < tol or cont >= Nmax:
             
            break

    return matriz

 

 

 

 

f="e**(x-2)-log(x-1)-x**2+4*x-5"
df="-2*x+e**(x-2)-(1/(x-1))+4"
d2f="e**(x-2)+ 1/((x-1)**2)-2"

 
# Ejecutar el método

#print(matriz)

#print(tabulate(matriz, headers=["Iteración", "x", "f(x)", "df(x)", "d2f(x)", "Error Abs."], tablefmt="fancy_grid"))

      