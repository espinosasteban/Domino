import os
import pygame


class Ficha:
    def __init__(self, valor1, valor2, imagen=""):
        self._valor1 = valor1  #Numero de la cara 1
        self._valor2  = valor2   #Numero de la cara 2
        self._imagen = imagen

    def getValores(self):
        return (self._valor1, self._valor2)

    def getImagen(self):
        return self._imagen

    def voltearFicha(self):
        self._valor1, self._valor2 = self._valor2, self._valor1

        ruta = os.path.join(os.getcwd(), 'parteGrafica', 'imagenes')
        self._imagen = pygame.image.load(os.path.join(ruta, f"ficha_{self._valor1}_{self._valor2}.png"))

    def esDoble(self):
        return self._valor1 == self._valor2

    def esValida(self, tablero_logico):
        valida = False
        valor_izq = tablero_logico[0].getValores()[0]  # El valor izquierdo de la ficha mas a la izquierda
        valor_der = tablero_logico[-1].getValores()[-1]

        valores = self.getValores()  # Obtener los 2 valores de la ficha

        # Comprobar si los valores de la ficha son iguales a los valores extremos del tablero
        if valores[0] == valor_izq:
            valida = True
        if valores[0] == valor_der:
            valida = True
        if valores[-1] == valor_izq:
            valida = True
        if valores[-1] == valor_der:
            valida = True

        return valida


    