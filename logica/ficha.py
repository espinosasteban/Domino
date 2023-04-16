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



    