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

 



def punto_f(g,x0,tol,Nmax,error):
  
    g =conversion(g) 
    
    def evaluate_expression(x):
        return eval(g)
    
    xant=x0
    E=0
    cont=0
    matriz=[]
    gxant=evaluate_expression(xant)
    print(gxant, "gxant",xant,)
    print(gxant)
     
    Eabs=abs(gxant-xant) 
    
    if error=="rela":
        if gxant != 0:
            E=Eabs/gxant
            err=Eabs/gxant
            print("esa fue")
        else:
            print("Error: division by zero")
            E= float('inf')
            err=float('inf')
        
    else:
        E=Eabs
         
    

     
    
    while E>tol and cont<Nmax:
        
            
         
        xact=evaluate_expression(float(xant))
        Eabs=abs(xact-xant)
        if error=="abs":
            E=abs(xact-xant)
        
        # Verificar si xact es cero
        if xact != 0:
            err=Eabs/xact
            if error=="rela":
                E=Eabs/xact
        else:
            print("Error: division by zero")
            err = float('inf')
            if error=="rela":
                E = float('inf')
            
        
        gxant=evaluate_expression(xant)   
        matriz.append([cont,xant,gxant,Eabs, err])
        cont+=1
        xant=xact
        
    
    gxant=evaluate_expression(xant)  
      
    return xant,gxant, cont, matriz




 
 
 
 

 
 
 
 
 
   
 
#g="e**-x"
#xant, gxant, cont, matriz = punto_f(g, 1, 10**-4, 100)
#print(matriz)  
 