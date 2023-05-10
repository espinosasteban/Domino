from logica.ficha import Ficha

class Jugador:
    def __init__(self, nombre, fichas): 
        self._nombre = nombre
        self._fichas = fichas

    def getFichas(self):
        return self._fichas

    def buscarFicha(self, valor_buscar1, valor_buscar2):
        for ficha in self.getFichas():
            valores = ficha.getValores()
            if valores == (valor_buscar1, valor_buscar2) or valores == (valor_buscar2, valor_buscar1):
                return ficha
        return None

    def eliminarFicha(self, ficha_eliminar):
        self.getFichas().remove(ficha_eliminar)

    def determinarFichasValidas(self, tablero_logico) -> list: #Funcion que regresa una lista de tuplas con las fichas que se pueden jugar y un bool que indica el lado en que se puede jugar
        listaValida = []
        for ficha in self.getFichas():
            if ficha.esValida(tablero_logico)[0]:
                listaValida.append((ficha, ficha.esValida(tablero_logico)[-1]))
        """
        valor_izq = tablero_logico[0].getValores()[0] #El valor izquierdo de la ficha mas a la izquierda
        valor_der = tablero_logico[-1].getValores()[-1] #El valor derecho de la ficha mas a la derecha 

        for ficha in self.getFichas(): #Para cada ficha en la mano de fichas del jugador 
            agregar = False
            izq = False
            der = False
            valores = ficha.getValores() #Obtener los 2 valores de la ficha
            
            # Comprobar si los valores de la ficha son iguales a los valores extremos del tablero 
            if valores[0] == valor_izq: 
                izq = True
                agregar = True
            if valores[0] == valor_der:
                der = True
                agregar = True
            if valores[-1] == valor_izq:
                izq = True
                agregar = True
            if valores[-1] == valor_der:
                der = True
                agregar = True
            if agregar: # Se agrega una tupla a la lista, con el valor de la ficha que se puede colocar y los lados en que se puede colocar 
                listaValida.append((ficha, (izq, der)))
            """
        return listaValida


    def getNombre(self):
        return self._nombre

    def calcularPuntos(self) -> int:
        puntaje = 0
        for ficha in self.getFichas():
            puntaje += sum(ficha.getValores())
        return puntaje

    #def seleccionarFicha(self.)
'''
##Caso de prueba

tablero_logico = deque()
ficha_tablero1 = Ficha(6,6)
ficha_tablero2 = Ficha(6,2)
tablero_logico.append(ficha_tablero1)
tablero_logico.append(ficha_tablero2)



ficha_jugador1 = Ficha(2,4)
ficha_jugador2 = Ficha(3,3)
ficha_jugador3 = Ficha(6,0)
ficha_jugador4 = Ficha(2,1)

fichas_jugador = deque([ficha_jugador1, ficha_jugador2, ficha_jugador3, ficha_jugador4])

JugadorPrincipal = Jugador("Principal", fichas_jugador)

print(JugadorPrincipal.determinarFichasValidas(tablero_logico))
'''

