import os
from collections import deque
from logica.tablero import Tablero
from random import randint
from logica.jugador import Jugador
from logica.rival import Rival
import pygame
 
class GameDisplay:
    def dibujar(self, mi_ficha, tablero_logico, tablero_fisico, lado, v=[0,-1]):
    #Reutilizacion de codigo, el valor por defecto de "v" permite la logica para el lado derecho.
    #en caso de ser para el lado izquierdo, se pasa un array inverso
        if mi_ficha.getValores()[v[0]] != tablero_logico[v[1]].getValores()[v[1]]:
            mi_ficha.voltearFicha()
        self.ponerFicha(tablero_fisico, mi_ficha.getImagen(), lado)
        tablero_logico.append(mi_ficha)
    

    def posicionarFicha(self, ficha_rotada, posicion_x, posicion_y, ficha_dibujar, tablero_logico):
        self.screen.blit(ficha_rotada, (posicion_x, posicion_y - 30))

        #condiciones de mostrar
        #utilzando el metodo determinarFichasValidas y mirando si el de la derecha, el de la izquierda o ambos son validos
        #se pintan los botones y se les pone para escoger donde poner la ficha

        # Crear boton y agregarlo a la lista
        boton_left = pygame.Rect(50, 50, 30, 30)
        boton_right = pygame.Rect(50, 50, 30, 30)

        # Flecha hacia la izquierda
        flecha_izquierda = [(0, 10), (10, 0), (10, 5), (20, 5), (20, 15), (10, 15), (10, 20)]

        # Flecha hacia la derecha
        flecha_derecha = [(20, 10), (10, 0), (10, 5), (0, 5), (0, 15), (10, 15), (10, 20)]


        print(ficha_dibujar.esValida(tablero_logico)[1])
        #izquierdo
        if (ficha_dibujar.esValida(tablero_logico)[1][0]):
            pygame.draw.polygon(self.screen, (0, 255, 0), [(posicion_x + 10 + x, posicion_y - 70 + y) for x, y in flecha_izquierda])
            #pygame.draw.rect(self.screen, (0, 255, 0), flecha_izquierda, 3)
        else:
            pygame.draw.polygon(self.screen, (255, 0, 0), [(posicion_x + 10 + x, posicion_y - 70 + y) for x, y in flecha_izquierda])
            #pygame.draw.rect(self.screen, (255, 0, 0), flecha_izquierda, 3)
        #izquierdo
        boton_left.center = (posicion_x + 20, posicion_y - 60)
        self.lista_botones.append(boton_left)
        #pygame.draw.rect(self.screen, boton_color_izq, boton_left)

        if (ficha_dibujar.esValida(tablero_logico)[1][1]):
            pygame.draw.polygon(self.screen, (0, 255, 0), [(posicion_x + 50 + x, posicion_y - 70 + y) for x, y in flecha_derecha])
            #pygame.draw.rect(self.screen, (0, 255, 0), flecha_derecha, 3)
        else:
            pygame.draw.polygon(self.screen, (255, 0, 0), [(posicion_x + 50 + x, posicion_y - 70 + y) for x, y in flecha_derecha])
            #pygame.draw.rect(self.screen, (0, 255, 0), flecha_derecha, 3)
        #derecho
        boton_right.center = (posicion_x + 55, posicion_y - 60)
        self.lista_botones.append(boton_right)

        #pygame.draw.rect(self.screen, boton_color_der, boton_right)

        #verificar click
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for boton in self.lista_botones:
                    if boton.collidepoint(pos):
                        boton_color = (0, 0, 0)
        # Dibuja el botón en la pantalla con el nuevo color
                    #pygame.draw.rect(self.screen, boton_color_izq, boton_left)
                    #pygame.draw.rect(self.screen, boton_color_der, boton_right)
    def ponerFicha(self, tablero_fisico: deque, imagen_ficha, lado):

        #se transforma la imagen para que sea de menor tamaño
        ficha_transformada = pygame.transform.scale(imagen_ficha, (int(imagen_ficha.get_width() / 4), int(imagen_ficha.get_height() / 4)))
        if len(tablero_fisico) == 0:
            #si el tablero está vacío, se coloca en el centro


            #se muestra en el tablero en unas coordenadas que más o menos sea la mitad
            #(el centrado lo hice con prueba y error)
            self.screen.blit(ficha_transformada, (int(self.ancho/2)-ficha_transformada.get_width(),int(self.alto/2)-150))

            tablero_fisico.append((ficha_transformada,(int(self.ancho/2)-ficha_transformada.get_width(),int(self.alto/2)-150)))
            #y se agrega a tablero físico de la siguiente forma: (imagen de la ficha transformada, (posicion_x, posicion_y)
            #esto con el objetivo de que después sea fácil obtener las coordenadas de dónde está la ficha dibujada.
            pygame.display.update()

        else:
            #si ya hay una ficha en el tablero, entonces:
            #si la quiero poner a la derecha entonces mi ficha "anterior" es la ficha [-1] en el deque porque está
            #a la derecha del todo
            if lado == "derecho":
                print("derecho")
                ficha_derecha = tablero_fisico[-1]
                x_anterior, y_anterior = ficha_derecha[1] # se obtiene la tupla con las coordenadas
                print(x_anterior, y_anterior)
                self.screen.blit(ficha_transformada, (x_anterior+int((270/4)),y_anterior)) # se dibuja la nueva ficha
                #para dibujar en x, tengo que correrla el ancho de la ficha anterior (256/4) y sumarle el x de la anterior.
                #coloco + 270 para darle un poco de espacio y que no esté tan pegada.
                tablero_fisico.append((ficha_transformada, (x_anterior+int((270/4)), y_anterior)))
                #se agrega la ficha

                pygame.display.update()

            if lado == "izquierdo":
                #misma lógica que antes pero acá la ficha de la izquierda del deque es la [0]
                print("izquierdo")
                ficha_derecha = tablero_fisico[0]
                x_anterior, y_anterior = ficha_derecha[1]


                self.screen.blit(ficha_transformada, (x_anterior - int((270 / 4)), y_anterior))
                #acá en lugar de sumar hay que restar en x.

                tablero_fisico.appendleft((ficha_transformada, (x_anterior - int((270 / 4)), y_anterior)))
                #IMPORTANTE: se agrega la ficha al inicio
                pygame.display.update()

    

    
    def ventana_emergente(self, mensaje):
        # Define el tamaño y posición de la ventana emergente
        mensaje_ancho = 400
        mensaje_alto = 200
        mensaje_x = (self.ancho - mensaje_ancho) // 2
        mensaje_y = (self.alto - mensaje_alto) // 2
    
        # Crea una capa separada para el mensaje emergente
        capa_mensaje = pygame.Surface((mensaje_ancho, mensaje_alto))
        capa_mensaje.fill((255, 255, 255))  # Rellena la capa con un color de fondo (en este caso blanco)
        fuente = pygame.font.Font(None, 36)  # Define una fuente para el mensaje
        texto = fuente.render(f"{mensaje}", True, (0, 0, 0))  # Crea un objeto de texto con el mensaje (usando "u" antes del mensaje para convertirlo en unicode)
        capa_mensaje.blit(texto, (0, 0))  # Dibuja el texto en la capa de mensaje en la posición correcta
    
        # Crea un botón de cerrar en la capa de mensaje
        boton_ancho = 80
        boton_alto = 40
        boton_x = mensaje_ancho - boton_ancho - 10
        boton_y = 10
        boton = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
        pygame.draw.rect(capa_mensaje, (255, 0, 0), boton)  # Dibuja un rectángulo rojo como el botón de cerrar en la capa de mensaje
        fuente_boton = pygame.font.Font(None, 24)
        texto_boton = fuente_boton.render("Cerrar", True, (255, 255, 255))
        capa_mensaje.blit(texto_boton, (boton_x + 10, boton_y + 10))  # Dibuja el texto del botón en la capa de mensaje en la posición correcta
    
        self.screen.blit(capa_mensaje, (mensaje_x, mensaje_y))
        return boton

    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")
        self.lista_botones = []

        # Inicializar Pygame
        pygame.init()

        # Crear la ventana del juego
        self.screen = pygame.display.set_mode((ancho, alto))

        # Establecer el título de la ventana
        pygame.display.set_caption("Mi Juego")

        # Establecer el color de fondo de la ventana
        self.background_color = (0, 128, 10)

        # Establecer el estado de la ventana a "abierto"
        self.is_running = True

    def run(self):
        tablero_fisico = deque()  # tablero que representa el juego (físicamente)
        tablero_logico = deque() #tablero que representa el juego (logicamente)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "sonidos/background.mp3"))
        pygame.mixer_music.play(-1)

        # generación de fichas (PRUEBA)
        partida = Tablero()
        partida.generar_fichas()
        jugador_saque = partida.encontrarSaque()

        ficha_saque = jugador_saque.buscarFicha(6,6)
        jugador_saque.eliminarFicha(ficha_saque)

        jugador_principal = partida.getJugadores()[0]


        # GENERACIÓN  DE BOTONES PARA PRUEBAS
        boton_superficie = pygame.Surface((100, 50))
        boton_superficie.fill((255, 255, 255))  # Establecer el color del botón

        # Crear el rectángulo del botón derecho
        boton_rect = boton_superficie.get_rect()
        boton_rect.x = 40  # Establecer la coordenada x del botón
        boton_rect.y = 40  # Establecer la coordenada y del botón
        self.screen.fill(self.background_color)
        self.screen.blit(boton_superficie, boton_rect)
        pygame.display.update()

        # crear el rectangulo del botón izquierdo

        # generación de fichas POV jugador
        def generar_pov_jugador(fichas_jugador_principal):
            self.lista_botones.clear()
            ancho_total_fichas = (128 * 7)
            posicion_x = (self.ancho - ancho_total_fichas) / 2

            posicion_y = 700
            separacion = 10
            fondo = pygame.Surface((ancho_total_fichas+128, 400))
            fondo.fill((0, 100, 10))
            self.screen.blit(fondo, (posicion_x, posicion_y - 100))

            #Botones
            #lista con los botones

            for j in range(0, len(fichas_jugador_principal)):
                ficha_dibujar = fichas_jugador_principal[j]
                ficha_rotada = pygame.transform.rotate(ficha_dibujar.getImagen(), 90)
                if ficha_dibujar.esValida(tablero_logico)[0]:
                    #posiciona las fichas, realiza varias traslaciones en base a unas posiciones iniciales
                    self.posicionarFicha(ficha_rotada, posicion_x, posicion_y, ficha_dibujar, tablero_logico)
                else:
                    self.screen.blit(ficha_rotada, (posicion_x, posicion_y))

                posicion_x += 128 + separacion

        self.ponerFicha(tablero_fisico, ficha_saque.getImagen(), "derecho")
        tablero_logico.append(ficha_saque)
        generar_pov_jugador(jugador_principal.getFichas())


        while self.is_running:
            fichas_validas = jugador_principal.determinarFichasValidas(tablero_logico)
            if len(fichas_validas) == 0:
                rival = partida.getJugadores()[randint(1,3)]

            elif len(fichas_validas) > 0:
                datos_ficha = fichas_validas[randint(0,len(fichas_validas)-1)]

            lado = []
            if len(fichas_validas) > 0:
                tupla_condicion = datos_ficha[1]
                if tupla_condicion[0]:
                    lado.append("izquierdo")
                if tupla_condicion[1]:
                    lado.append("derecho")


            # Procesar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Si el usuario cierra la ventana, establecer el estado a "cerrado"
                    self.is_running = False
                # si le doy click al boton de la izquierda, entonces ponerficha a la izquierda
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, boton in enumerate(self.lista_botones):
                        if boton.collidepoint(pos):
                            mi_ficha = datos_ficha[0]
                            coordenadas_boton = boton.center
                            color = self.screen.get_at(coordenadas_boton)
                            if color == (255, 0, 0, 255):
                                mensaje = self.ventana_emergente("Jugada invalida") 
                                break
                            elif i == 0: 
                                self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "izquierdo", v=[-1,0])
                                print("izquierdo")
                            elif i == 1:
                                self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "derecho")
                                print("derecho")
                            jugador_principal.getFichas().remove(mi_ficha)
                            generar_pov_jugador(jugador_principal.getFichas())
        # Ciclo principal del juego

                if event.type == pygame.MOUSEBUTTONDOWN and boton_rect.collidepoint(event.pos):
                    seleccionar = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sonidos/seleccionar_lado_derecho.mp3"))
                    seleccionar.play()
                    tirar = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sonidos/tirar_ficha0.mp3"))
                    tirar.play()                
                    if len(fichas_validas) > 0:
                        mi_ficha = datos_ficha[0]
                        lado_str = lado[randint(0,len(lado)-1)]
                        v_array = [0,-1]
                        if lado_str == "izquierdo":
                            v_array = [-1,0]
                        self.dibujar(mi_ficha, tablero_logico, tablero_fisico, lado_str, v_array)
                        
                        jugador_principal.getFichas().remove(mi_ficha)
                        generar_pov_jugador(jugador_principal.getFichas())

            # Dibujar el fondo

            # Actualizar la pantalla
            pygame.display.update()

        # Salir de Pygame
        pygame.mixer.music.stop()
        pygame.quit()
