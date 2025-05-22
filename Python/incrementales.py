from tabulate import tabulate

def C1_busquedas(f, x0, h, Nmax):
    xant = x0
    fant = f(xant)
    xact = xant + h
    fact = f(xact)
    matriz = []
    error_abs = abs(fact - fant)
    error_rel = error_abs / fact

    for i in range(1, Nmax+1):
        matriz.append([i, xant, xact, fant, fact, error_abs, error_rel])
        if fant * fact < 0:
            break
        
        xant = xact
        fant = fact
        xact = xant + h
        fact = f(xact)
        error_abs = abs(fact - fant)
        error_rel = error_abs / fact

    a = xant
    b = xact
    iter = i
     
    return a, b, iter, matriz,h,f

#def f(x):
    #return x**3 - 2*x**2 + 0.25*x + 0.75

#a, b, iter, matriz = C1_busquedas(f, -1, 0.1, 20)

#rint(tabulate(matriz, headers=["Iteración", "a", "b", "f(a)", "f(b)", "Error Abs.", "Error rel."], tablefmt="fancy_grid"))