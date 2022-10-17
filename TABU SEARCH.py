"""Test 1

Date of beggining 13/10/2022
"""

from random import randint as rdt
import matplotlib.pyplot as plt
import pandas as pd


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


def ElementosUnicos(l:list) -> list:

    lista_unicos = []

    numeros_unicos = set(l)

    for elem in numeros_unicos:
        lista_unicos.append(elem)

    return lista_unicos


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


class TabuSearch:
    
    def Resolver(self, inst:Instancia, intentos, seleccion, minimo_iter):
        nl = 1
        lista_ord = sorted(inst.objetos.copy(), 
                       key = lambda x: x.valor / x.peso)
        proporciones_ord = CrearRelacion(lista_ord)
        #Solucion inicial de donde buscaremos mejoras

        sol_buena = Constructivo(inst, proporciones_ord)
        print(CalcularValorTotal(sol_buena))
        itinerario_soluciones1 = []
        itinerario_inserciones1 = []
        nueva_mercancia1, inserciones1 = self.Mejorar(sol_buena, 
                                              lista_ord,
                                              inst.maleta1,
                                              inst.maleta2, nl = nl)
        elegir = int(len(nueva_mercancia1) * seleccion)
        
        cantera = []
        inserciones_cantera = []
        top = [CalcularValorTotal(nueva_mercancia1[y]) \
               for y in range(elegir)]
        indices = [y for y in range(elegir)]
        for m in range(len(nueva_mercancia1) - elegir):
            valor = CalcularValorTotal(nueva_mercancia1[m + elegir])
            for v in range(len(top)):
                if valor > top[v]:
                    indices[v] = m + elegir
                    
        for g in indices:
            cantera.append(nueva_mercancia1[g])
            inserciones_cantera.append(inserciones1[g])
            
        itinerario_soluciones1 += cantera
        itinerario_inserciones1 += inserciones_cantera
        
        itn = 0
        while itn < intentos:
            nl += 1
            ctn = cantera.copy()
            ins_ctn = inserciones_cantera.copy()
            for r in range(len(cantera)):
                if itn > minimo_iter:
                    ins_ctn[r] = ins_ctn[r][int(len(ins_ctn[r]) * 0.3):]
                    
                
                nueva_mercancia1, inserciones1 = self.Mejorar(ctn[r], 
                                                              lista_ord,
                                                              inst.maleta1,
                                                              inst.maleta2, 
                                                              indescartables = ins_ctn[r],
                                                              nl = nl)
            
                elegir = int(len(nueva_mercancia1) * seleccion)
                cantera = []
                inserciones_cantera = []
                top = [CalcularValorTotal(nueva_mercancia1[y]) \
                       for y in range(elegir)]
                indices = [y for y in range(elegir)]
                for m in range(len(nueva_mercancia1) - 10):
                    valor = CalcularValorTotal(nueva_mercancia1[m + 10])
                    for v in range(len(top)):
                        if valor > top[v]:
                            indices[v] = m + 10
                            
                for g in indices:
                    cantera.append(nueva_mercancia1[g])
                    inserciones_cantera.append(inserciones1[g])
                    
                itinerario_soluciones1 += cantera
                
            itn += 1
            
        return itinerario_soluciones1
    
        
    def Mejorar(self, sol:Solucion, l:list, 
                peso_max1, peso_max2, indescartables = [], nl = 1):
        
        factor_decisivo = nl % 2
        if factor_decisivo:
            lista_elegida = sol.lista1
        else:
            lista_elegida = sol.lista2
            
        soluciones_pasadas = []
        lista_inserciones = []
        h = 1
        while h <= len(lista_elegida):
            insertados = [] + indescartables
            eliminados = []
            peso_restante1 = peso_max1 - sum([x.peso for x in sol.lista1])
            peso_restante2 = peso_max2 - sum([x.peso for x in sol.lista2])
            modificable = lista_elegida.copy()

            if factor_decisivo:
                peso_util = peso_restante1
            else:
                peso_util = peso_restante2
            elegido = modificable[len(modificable) - h]            
            
            if elegido not in insertados:
                modificable.pop(len(modificable) - h)
                peso_util += elegido.peso
                eliminados.append(elegido)
                
                if factor_decisivo:
                    lista_negra = modificable + eliminados + sol.lista2
                else:
                    lista_negra = modificable + eliminados + sol.lista1

                itera = len(l)

                while itera and peso_util > 0:
                    candidato = l[itera - 1]
        
                    if candidato.peso <= peso_util and \
                        candidato not in  lista_negra:
                        modificable.append(candidato)
                        peso_util -= candidato.peso
                        insertados.append(candidato)
                    itera -= 1
    
                nueva_sol = Solucion()
                if factor_decisivo:
                    nueva_sol.lista1 = modificable
                    nueva_sol.lista2 = sol.lista2
                else:
                    nueva_sol.lista1 = sol.lista1
                    nueva_sol.lista2 = modificable
                soluciones_pasadas.append(nueva_sol)
                lista_inserciones.append(insertados)

            h += 1
            
        return soluciones_pasadas, lista_inserciones
    
    def MostrarResultado(self, inst:Instancia, intentos, seleccion, minimo_iter):
        
        sol = self.Resolver(inst, intentos, seleccion, minimo_iter)
        sol_unicas = ElementosUnicos(sol)
        
        graf = []
        for s in sol_unicas:
            graf.append(CalcularValorTotal(s))
            
        df = pd.DataFrame({
                "index":list(range(len(sol_unicas))),
                "solucion":graf
                })
        df.plot(x = "index", y = "solucion", kind = "line",
                title = "Intentos:" + str(intentos) + "Seleccion:" + str(seleccion) + "Minimo_iter:" + str(minimo_iter))
        plt.show()
        print(graf[0], max(graf))
        
def CalcularValorTotal(sol:Solucion) -> int:
    
    valor_total = 0
    for obj in sol.lista1:
        valor_total += obj.valor
    for obj in sol.lista2:
        valor_total += obj.valor
        
    return valor_total
        
        
def CrearRelacion(l:list)->dict:
    
    relacion = {}
    for obj in l:
        relacion[obj.id] = obj.valor / obj.peso
            

    return relacion


def CrearMaletaConstructivo(inst, relacion, relacion_destruible,
                            peso_maximo):
    
    maleta = []
    
    i = 1

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
    maleta2 = CrearMaletaConstructivo(inst, relacion, 
                                      relacion_ordenada_uso, 
                                      peso_maleta2)

    mlt1 = []
    mlt2 = []
    for k in maleta1:
        mlt1.append(inst.objetos[k-1])
    for l in maleta2:
        mlt2.append(inst.objetos[l-1])
        
    sol = Solucion()
    sol.lista1 = mlt1
    sol.lista2 = mlt2
    
    return sol


def main():
    
    print(__doc__)
    
    inst = Instancia()
    inst.LeerFichero("datos_aleatorios_problema_optimizacion.txt")
    
    tabu = TabuSearch()
    tabu.MostrarResultado(inst, intentos = 1000, seleccion = 0.3, minimo_iter = 50)
    
    
if __name__ == '__main__':
    main()

