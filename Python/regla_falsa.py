from tabulate import tabulate


def C3_reglaFalsa(f, a,b, tol,Nmax ):

    fa=f(a)
    fb=f(b)
    denom = f(b) - f(a)
    if denom == 0:
        print("Error: division por 0")
        return a, b, 0, []
    pm=(f(b)*a-f(a)*b) / denom
    fpm=f(pm)
    E=1000 
    cont=0
    matriz = []
    

    while E>tol and cont<Nmax:
        if fb*fpm<0:
            a=pm; 
        else:
            b=pm;    

        p0=pm 
        denom = f(b) - f(a)
        if denom == 0:
            print("Error: division por cero")
            break
        pm=(f(b)*a-f(a)*b) / denom
        fpm=f(pm) 
        E=abs(pm-p0) 
        cont=cont+1 

        matriz.append([cont, a, fa, pm, fpm, b, fb, E ])

    return a, b, cont, matriz
      

#def f(x):
    #return x**3 - 7.51*x**2+18.4239*x-14.8331

#a, b, iter, matriz = C3_reglaFalsa(f, 3, 3.5, 0.0001, 30)

#print(tabulate(matriz, headers=["Iteración", "a", "f(a)", "pm", "f(pm)", "b" , "f(b)" , "Error Abs." ], tablefmt="fancy_grid"))    
      
        
 