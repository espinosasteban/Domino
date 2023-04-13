class Jugador:
    def __init__(self, nombre, fichas): #Mirar si poner fichas en el constructor
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



