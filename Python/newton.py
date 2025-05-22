from sympy import symbols, log
import math
from tabulate import tabulate
import numpy as np
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

def C5_newton(f,df, x0, tol,Nmax,error12):
    f =conversion(f) 
    df =conversion(df) 
    
    def evaluate_expression(x):
        return eval(f)
    
    def evaluate_expression2(x):
        return eval(df)
    
    xant=x0 
    fant=evaluate_expression(xant)
    cont=0 
    matriz = []
    dfx=evaluate_expression2(xant)
   
    if dfx == 0:
        print("Error: division por cero")
        return matriz

    xact=xant-fant/dfx 
    Eabs=abs(xact-xant)
 
    if error12=="rela":
        if xact != 0:
            E=Eabs/xact
            err=Eabs/xact
            print("esa fue")
        else:
            print("Error: division by zero")
            E= float('inf')
            err=float('inf')
    else:
        E=Eabs

    while E>tol and cont<Nmax:
        if dfx == 0:
            print("Error: division por cero")
            break
            
        xact=xant-fant/dfx 
        fact=evaluate_expression(xact)
        Eabs=abs(xact-xant) 
        err=Eabs/xact    
        if error12=="rela":
            if xact != 0:
                E=Eabs/xact
                err=Eabs/xact
                print("esa fue")
            else:
                print("Error: division by zero")
                E= float('inf')
                err=float('inf')
            
        else:
            E=Eabs
        matriz.append([cont, xant,fant,dfx,  Eabs, err ])
        cont=cont+1 
        xant=xact 
        fant=fact 
        dfx=evaluate_expression2(xant)

    return  matriz

