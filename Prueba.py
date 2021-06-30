import re
from Nodo import Nodo

entrada = ""
exit = True

operadores = ['<', '>', '=']

# Lista de reglas que va generando el usuario
reglas = {}

# Lista de listas de precedencias generadas por el usuario
precedencias = {
    '$' : {

    }
}

funcionF = {}

funcionG = {}

# ======================================== Clases

# Para diferenciar los simbolos en un mismo nodo
class Simbolo():

    def __init__(self, funcion, simbolo):

        self.funcion = funcion
        self.simbolo = simbolo
        self.nodo = None
    
    def getSimbolo(self):

        return self.simbolo

    def getFuncion(self):

        return self.funcion

    def getNodo(self):

        return self.nodo
    
    def asigNodo(self, nodo):

        self.nodo = nodo



# ======================================== Funciones 

# Funcion para determinar si es no-terminal (Mayúscula, un caracter)
def isValidNonTerminal(nonTerminal):

    if(len(nonTerminal) != 1 or (not nonTerminal.isupper()) ): return False
    else: return True

# Chequea si contiene el caracter $ y si es ascii
def isValidTerminal(terminal):

    return all(ord(c) < 128 and not c.isupper() for c in terminal)

# Determina si una cadena es valida para ser regla
def isValidRule(cadena):

    if(re.search("[A-Z][A-Z]+", cadena) is not None):
        return False
    else: return True

# Define una regla de la gramática
def definirRegla(nonTerminal, regla):

    reglas[regla] = nonTerminal
    print("Regla \"" + nonTerminal + " -> " + regla + "\" agregada a la gramática")

# Define una precedencia en la gramática
def setPrecedencia(terminal1, operador, terminal2):

    if(operador == '>'):
        operadorString = "tiene mayor precedencia que"
    if(operador == '<'):
        operadorString = "tiene menor precedencia que"
    if(operador == '='):
        operadorString = "tiene igual precedencia que"


    # Si no existe...
    if not terminal1 in precedencias:
        # Crea la entrada en el diccionario de 
        precedencias[terminal1] = {}

    precedenciasTerminal1 = precedencias[terminal1]

    # Se no existe el terminal2 dentro de las precedencias de terminal1, se crea
    if not terminal2 in precedenciasTerminal1:
        precedenciasTerminal1[terminal2] = {}

    precedenciasTerminal1[terminal2] = operador

    print("\"" + terminal1 + "\" " + operadorString + " \"" + terminal2 + "\"")

# Define el símbolo inicial de la gramática
def setInitSymbol(initSymbol):

    print("\"" + initSymbol + "\" es ahora el símbolo inicial de la gramática")

def build():

    for key in precedencias:

        simboloI = Simbolo('f', key)
        nodoF = Nodo('f'+key)
        simboloI.asigNodo(nodoF)
        funcionF[key] = nodoF

        precedenciaF = precedencias[key]

        for key2 in precedenciaF:
            simboloD = Simbolo('g', key2)
            
            if (precedenciaF[key2] == '='):
                nodoF.agregarSimbolo('g'+key2)
                simboloD.asigNodo(nodoF)
                funcionG[key2] = nodoF

            if (precedenciaF[key2]) == '>':
                if(key2 in funcionG):
                    nodoG = funcionG[key2]
                    nodoF.agregarAdy(nodoG)
                else:
                    nodoG = Nodo('g'+key2)
                    simboloD.asigNodo(nodoG)
                    funcionG[key2] = nodoG
                    nodoF.agregarAdy(nodoG)
            if (precedenciaF[key2] == '<'):
                if(key2 in funcionG):
                    nodoG = funcionG[key2]
                    nodoG.agregarAdy(nodoF)
                else:
                    nodoG = Nodo('g'+key2)
                    simboloD.asigNodo(nodoG)
                    funcionG[key2] = nodoG
                    nodoG.agregarAdy(nodoF)

    camino = []

    # Saca los caminos de la funcion F
    for key in funcionF:
        nodo = funcionF[key]
        resultado = nodo.calcularCaminoMasLargo(camino)

        if (resultado == "ERROR"):
            print("ERROR: No se pudo construir la gramática")
            break
    
    # Saca los caminos de la funcion G
    for key in funcionG:
        nodo = funcionG[key]
        resultado = nodo.calcularCaminoMasLargo(camino)

        if (resultado == "ERROR"):
            print("ERROR: No se pudo construr la gramática")
            break

    if(isinstance(resultado, int)):
        # Printing
        print("Analizador sintáctico construido")
        print('Valores para f: \n')
        for key in funcionF:
            print(key + ': ' + str(funcionF[key].getCaminoMasLargo()))
        
        # Printing
        print('Valores para g: \n')
        for key in funcionG:
            print(key + ': ' + str(funcionG[key].getCaminoMasLargo()))

        return True
    else:
        return False
    

    
def parse(frase):

    listaFrase = ['$']

    # Contruccion de la frase (ya me di cuenta que esto ya no sirve para nada)
    for simbolo in frase:
        ultimoFrase = listaFrase[len(listaFrase)-1]
        if (simbolo in precedencias[ultimoFrase]):
            precedenciasUltimoFrase = precedencias[ultimoFrase]
            listaFrase += [precedenciasUltimoFrase[simbolo], simbolo]
        else:
            print("El simbolo "+simbolo+" y "+ultimoFrase+" no son comparables")

    if('$' in precedencias[frase[len(frase)-1]]):
        precedenciasPenultimoSimbolo = precedencias[frase[len(frase)-1]]
        listaFrase += [precedenciasPenultimoSimbolo['$'], '$']
    else:
        print("El simbolo "+frase[len(frase)-1]+" y $ no son comparables")    

    # Te imprime la frase bien bonita
    print(listaFrase)

    # Now heavy machine gun

    pila = []
    accion = []
    
    pila.append(listaFrase[0])

    lector = 2

    while(True):
        p = pila[len(pila)-1]

        e = listaFrase[lector]

        if (p == '$' and e == '$'):
            print("Aceptar")
        elif(precedencias[p][e] == '<' or precedencias[p][e] == '=' ):
            pila.append(e)
            lector += 2
        elif (precedencias[p][e] == '>'):
            x = pila[len(pila)-1]
            while(not precedencias[pila[len(pila)-1]][x]):
                x = pila.pop()
            accion += [x+" -> "+reglas[x]]
        else:
            print("ERROR")
            




# ==============================================================================

buildeado = False

while (exit):

    entrada = input("$> ")
    instruccion = entrada.split()

    # Instrucciones de tamaño 1
    if(len(instruccion) == 1):

        # Salida del simulador
        if (instruccion[0] == "EXIT"):
            exit = False

        # Accion: BUILD
        elif(instruccion[0] == "BUILD"):
            buildeado = build()
        else:
            print("ERROR")

    # Instrucciones de tamaño > 1      
    elif (len(instruccion) > 1):

        # Accion: Generar una regla
        if (instruccion[0] == "RULE"):

            ladoIzquierdo = instruccion[1]
            ladoDerecho = ''.join(instruccion[2:])

            if (isValidNonTerminal(ladoIzquierdo) and isValidRule(ladoDerecho) and ('$' not in ladoDerecho)):
                definirRegla(ladoIzquierdo, ladoDerecho)
            else: 
                print("Error: Los valores introducidos para la regla no son válidos. Por favor intente de nuevo")                
      
        # Opcion: Definir una precedencia en la gramática
        elif (instruccion[0] == "PREC"):

            if(len(instruccion[1:]) != 3):
                print("Formato inválido. Recuerde: PREC <terminal> <op> <terminal>")

            # El resto deben ser dos operandos y un operador. (tamaño 3)
            elif ((isValidTerminal(instruccion[1]) or instruccion[1] == '$') and (instruccion[2] in operadores) and (isValidTerminal(instruccion[3]) or instruccion[3] == '$')):
                setPrecedencia(instruccion[1], instruccion[2], instruccion[3])
            
            # El operador es inválido
            elif (not (instruccion[2] in operadores)):
                print("Operador inválido")

            # Los operandos no son válidos
            elif(not isValidTerminal(instruccion[1]) or not isValidTerminal(instruccion[3])):
                print("Uno o más de los símbolos no es/son terminal")
                
        # Opcion: Definir el símbolo inicial de la gramática
        elif(instruccion[0] == "INIT"):

            if(len(instruccion[1:]) != 1):
                print("Tamaño de símbolo inválido. Debe ser no-terminal un caracter")
            else:
                if(isValidNonTerminal(instruccion[1])):
                    setInitSymbol(instruccion[1])
                else:
                    print("El símbolo debe ser no-terminal")
        
        # Opcion: Ejecutar el parser para la gramática establecida 
        elif(instruccion[0] == "PARSER"):
            
            frase = ''.join(instruccion[1:])
            if(not isValidTerminal(frase)):
                print("La frase suministrada no está conformada por solo símbolos terminales")
            elif(not buildeado):
                print("Tiene que buildear primero")
            else: 
                parse(frase)
        else:
            print("ERROR: Opción inválida")
    

