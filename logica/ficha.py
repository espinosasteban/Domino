class Ficha:
    def __init__(self, valor1, valor2, imagen=""):
        self.__valor1 = valor1  #Numero de la cara 1
        self.__valor2  = valor2   #Numero de la cara 2
        self.__imagen = imagen

    def getValores(self):
        vals = tuple(self.__valor1, self.__valor2)
        return vals
