class Nodo:

    def __init__(self, simbolo) -> None:

        self.simbolos = simbolo

        self.adyacentes = []

        self.caminoMasLargo = None

    def agregarAdy(self, adyacente):

        self.adyacentes.append(adyacente)

    def agregarSimbolo(self, simbolo):

        self.simbolos += "-" + simbolo

    def getAdys(self):

        return self.adyacentes

    def getSimbolos(self):

        return self.simbolos

    def getCaminoMasLargo(self):

        return self.caminoMasLargo

    def calcularCaminoMasLargo(self, camino):

        # Primero, verificar que no esté él mismo en el camino
        if self in camino:
            print("ERROR: Hay ciclo en el camino creado por el grafo de las funciones f y g") # Si está, hay un ciclo

            ciclo = ''
            for nodo in camino:
                ciclo += nodo.getSimbolos()
            
            print("El ciclo es: " + ciclo)

            return "ERROR"
        else:
            if self.adyacentes:
                self.caminoMasLargo = max(ady.calcularCaminoMasLargo(camino + [self]) for ady in self.adyacentes) + 1
            else: 
                self.caminoMasLargo = 0          

            return self.caminoMasLargo
