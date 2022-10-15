"""Test 1

Date of beggining 13/10/2022
"""

from random import randint as rdt


"""Para eliminar"""
def OrdenarDiccionario(diccionario:dict)->dict:
    
    dic_ord = {}
    list_ord = sorted(diccionario.copy().values())
    
    for i in list_ord:
        for k in diccionario.keys():
            if diccionario[k] == i:
                dic_ord[k] = diccionario[k]
                
    return dic_ord





def CrearFichero(nom:str,
                 num:int,
                 peso_m1:int,
                 peso_m2:int)-> (bool):
    try:
        g = open(nom, "w", encoding = "UTF-8")
    except:
        print("Error")
    else:
        
        g.write(str(peso_m1) + ";" + str(peso_m2) + "\n")
        for i in range(num):
            peso = rdt(1, int(min(peso_m1, peso_m2) * 0.8))
            valor = rdt(0, int(max(peso_m1, peso_m2) * 2.5))
            g.write(str(i + 1) + ";" + str(peso) + ";" +\
                    str(valor) + "\n")
        
        g.close()
        
    return


class Instancia: #Definicion del problema

    def __init__(self):
        self.maleta1 = int() #Peso maximo maleta 1
        self.maleta2 = int() #Peso maximo maleta2
        self.objetos = list() #De Objeto 
        
        
    def LeerFichero(self, nom:str):
        
        try:
            f = open(nom, "r", encoding = "UTF-8")
        except:
            print("Error")
        else:
            
            objetos = []
            
            s = f.readline()
            s = s.strip("\n").split(";")
            mlt1 = max(int(s[0]), int(s[1]))
            mlt2 = min(int(s[0]), int(s[1]))
            
            for linea in f:
                
                o = Objeto()
                l = linea.strip("\n").split(";")
                o.id = int(l[0])
                o.peso = float(l[1])
                o.valor = float(l[2])
                
                objetos.append(o)
                
            f.close()
            
            self.maleta1 = mlt1
            self.maleta2 = mlt2
            self.objetos = objetos            
            
        return


class Objeto:
    
    def __init__(self):
        self.id = int() #Identificador del objeto
        self.peso = float() #Peso del objeto
        self.valor = float() #Valor del objeto
        
    def __str__ (self):
        s = "ID: " + str(self.id) + "\n"
        s += "PESO: " + str(self.peso) + "\n"
        s += "VALOR: " + str(self.valor)
        
        return s
    

class Solucion:
    
    def __init__(self):
        self.lista1 = [] #De Objeto, lo que lleva la maleta 1
        self.lista2 = [] #De Objeto, lo que lleva la maleta 2
        
    def __str__ (self):
        
        p1 = 0
        p2 = 0
        v = 0
        s = "Lista 1: "
        for r in self.lista1:
            p1 += r.peso
            v += r.valor
            s += str(r.id) + ", "
        s += "\nLista 2: "
        for r in self.lista2:
            p2 += r.peso
            v += r.valor
            s += str(r.id) + ", "
        s += "\nPeso Lista 1: " + str(p1) + "\n"
        s += "Peso Lista 2: " + str(p2) + "\n"
        s += "Valor Total: " + str(v)
        
        return s

class AlgoritmoTabuSearch:
    
    def Resolver(self):
        a = "a"
        print(a)
        
        
def CrearRelacion(l:list)->dict:
    
    relacion = {}
    for obj in l:
        relacion[obj.id] = obj.valor / obj.peso
            

    return relacion


def CrearMaletaConstructivo(inst, relacion, relacion_destruible,
                            peso_maximo):
    
    maleta = []
    
    i = 1
    """
    while peso_maximo > 0 and i < len(relacion) and \
        len(relacion_destruible) > 0:
    Este codigo podría ser util si se teme que todos los objetos 
    puedan entrar en las listas, pero eso supondría hacer una comparacion 
    más, y no nos es necesario en la mayoria de ocasiones
    """
    while peso_maximo > 0 and i < len(relacion):
        id_relacion = list(relacion_destruible.keys())\
            [len(relacion_destruible) - i]
        if peso_maximo >= inst.objetos[id_relacion - 1].peso:
            maleta.append(id_relacion)
            peso_maximo -= inst.objetos[id_relacion - 1].peso
            del relacion_destruible[id_relacion]
            i -= 1
        i +=1
        
    return maleta

        
def Constructivo(inst:Instancia, relacion)-> Solucion:

    peso_maleta1 = inst.maleta1
    peso_maleta2 = inst.maleta2
    
    relacion_ordenada_uso = relacion.copy()
    
    maleta1 = CrearMaletaConstructivo(inst, relacion, 
                                      relacion_ordenada_uso, 
                                      peso_maleta1)
    print(relacion.keys())
    #print(relacion_ordenada_uso)
    maleta2 = CrearMaletaConstructivo(inst, relacion, 
                                      relacion_ordenada_uso, 
                                      peso_maleta2)
    #print(relacion_ordenada_uso)
    mlt1 = []
    mlt2 = []
    for k in maleta1:
        mlt1.append(inst.objetos[k-1])
    for l in maleta2:
        mlt2.append(inst.objetos[l-1])
        
    sol = Solucion()
    sol.lista1 = mlt1
    sol.lista2 = mlt2
    print(maleta2)
    
    return sol


def main():
    
    print(__doc__)
    
    inst = Instancia()
    inst.LeerFichero("Objetos.txt")
    
    lista_ord = sorted(inst.objetos.copy(), 
                       key = lambda x: x.valor / x.peso)
    proporciones_ord = CrearRelacion(lista_ord)
    #Solucion inicial de donde buscaremos mejoras
    #print(proporciones_ordenadas)
    a = Constructivo(inst, proporciones_ord)
    print(a)
    
if __name__ == '__main__': 
    main()

