import os
from collections import deque
from logica.tablero import Tablero
from random import randint
from logica.jugador import Jugador
from logica.rival import Rival
import pygame
from time import sleep


class GameDisplay:
    def dibujar(self, mi_ficha, tablero_logico, tablero_fisico, lado, v=[0, -1]):
        # Reutilizacion de codigo, el valor por defecto de "v" permite la logica para el lado derecho.
        # en caso de ser para el lado izquierdo, se pasa un array inverso
        if mi_ficha.getValores()[v[0]] != tablero_logico[v[1]].getValores()[v[1]]:
            mi_ficha.voltearFicha()
        self.ponerFicha(tablero_fisico, mi_ficha.getImagen(), lado, mi_ficha)

    def posicionarFicha(self, ficha_rotada, posicion_x, posicion_y, ficha_dibujar, tablero_logico):
        self.screen.blit(ficha_rotada, (posicion_x, posicion_y - 30))  # dibuja la ficha en una posicion determinada

        # condiciones de mostrar
        # utilzando el metodo determinarFichasValidas y mirando si el de la derecha, el de la izquierda o ambos son validos
        # se pintan los botones y se les pone para escoger donde poner la ficha

        # Crear boton y agregarlo a la lista
        boton_left = pygame.Rect(50, 50, 30, 30)
        boton_right = pygame.Rect(50, 50, 30, 30)

        # Flecha hacia la izquierda
        flecha_izquierda = [(0, 10), (10, 0), (10, 5), (20, 5), (20, 15), (10, 15), (10, 20)]

        # Flecha hacia la derecha
        flecha_derecha = [(20, 10), (10, 0), (10, 5), (0, 5), (0, 15), (10, 15), (10, 20)]

        print(ficha_dibujar.esValida(tablero_logico)[1])
        # izquierdo
        if (ficha_dibujar.esValida(tablero_logico)[1][0]):
            pygame.draw.polygon(self.screen, (0, 255, 0),
                                [(posicion_x + 10 + x, posicion_y - 70 + y) for x, y in flecha_izquierda])
            # pygame.draw.rect(self.screen, (0, 255, 0), flecha_izquierda, 3)
        else:
            pygame.draw.polygon(self.screen, (255, 0, 0),
                                [(posicion_x + 10 + x, posicion_y - 70 + y) for x, y in flecha_izquierda])
            # pygame.draw.rect(self.screen, (255, 0, 0), flecha_izquierda, 3)
        # izquierdo
        boton_left.center = (posicion_x + 20, posicion_y - 60)

        # pygame.draw.rect(self.screen, boton_color_izq, boton_left)

        if (ficha_dibujar.esValida(tablero_logico)[1][1]):
            pygame.draw.polygon(self.screen, (0, 255, 0),
                                [(posicion_x + 50 + x, posicion_y - 70 + y) for x, y in flecha_derecha])
            # pygame.draw.rect(self.screen, (0, 255, 0), flecha_derecha, 3)
        else:
            pygame.draw.polygon(self.screen, (255, 0, 0),
                                [(posicion_x + 50 + x, posicion_y - 70 + y) for x, y in flecha_derecha])
            # pygame.draw.rect(self.screen, (0, 255, 0), flecha_derecha, 3)
        # derecho
        boton_right.center = (posicion_x + 55, posicion_y - 60)
        self.lista_botones.append((boton_left, boton_right))
        # se agrega una tupla a lista botones para que corresponda con lista_validas

        # pygame.draw.rect(self.screen, boton_color_der, boton_right)

        # Dibuja el botón en la pantalla con el nuevo color
        # pygame.draw.rect(self.screen, boton_color_izq, boton_left)
        # pygame.draw.rect(self.screen, boton_color_der, boton_right)

    def ponerFicha(self, tablero_fisico: deque, imagen_ficha, lado, mi_ficha):

        # se transforma la imagen para que sea de menor tamaño
        ficha_transformada = pygame.transform.scale(imagen_ficha, (
            int(imagen_ficha.get_width() / 4), int(imagen_ficha.get_height() / 4)))

        if len(tablero_fisico) == 0:
            # si el tablero está vacío, se coloca en el centro
            ficha_transformada = pygame.transform.rotate(ficha_transformada, 90)

            # se muestra en el tablero en unas coordenadas que más o menos sea la mitad
            # (el centrado lo hice con prueba y error)
            self.screen.blit(ficha_transformada,
                             (int(self.ancho / 2) - ficha_transformada.get_width(), int(self.alto / 2) - 150))

            tablero_fisico.append((ficha_transformada,
                                   (int(self.ancho / 2) - ficha_transformada.get_width(), int(self.alto / 2) - 150),
                                   True))
            # y se agrega a tablero físico de la siguiente forma: (imagen de la ficha transformada, (posicion_x, posicion_y)
            # esto con el objetivo de que después sea fácil obtener las coordenadas de dónde está la ficha dibujada.
            pygame.display.update()

        else:
            # si ya hay una ficha en el tablero, entonces:
            # si la quiero poner a la derecha entonces mi ficha "anterior" es la ficha [-1] en el deque porque está
            # a la derecha del todo

            if lado == "derecho":
                print("derecho")

                ficha_derecha = tablero_fisico[-1]
                x_anterior, y_anterior = ficha_derecha[1]
                # se obtiene la tupla con las coordenadas
                print(x_anterior, y_anterior)

                if ficha_derecha[-1]:  # si la anterior es doble
                    self.screen.blit(ficha_transformada, (x_anterior + int((270 / 8)), y_anterior + 20))
                    tablero_fisico.append((ficha_transformada, (x_anterior + int((270 / 8)), y_anterior + 20), False))

                elif mi_ficha.esDoble():
                    ficha_transformada = pygame.transform.rotate(ficha_transformada, 90)
                    self.screen.blit(ficha_transformada,
                                     (x_anterior + int((270 / 4)), y_anterior - 20))  # se dibuja la nueva ficha
                    # para dibujar en x, tengo que correrla el ancho de la ficha anterior (256/4) y sumarle el x de la anterior.
                    # coloco + 270 para darle un poco de espacio y que no esté tan pegada.
                    tablero_fisico.append((ficha_transformada, (x_anterior + int((270 / 4)), y_anterior - 20), True))

                else:
                    self.screen.blit(ficha_transformada,
                                     (x_anterior + int((270 / 4)), y_anterior))  # se dibuja la nueva ficha
                    # para dibujar en x, tengo que correrla el ancho de la ficha anterior (256/4) y sumarle el x de la anterior.
                    # coloco + 270 para darle un poco de espacio y que no esté tan pegada.
                    tablero_fisico.append((ficha_transformada, (x_anterior + int((270 / 4)), y_anterior), False))

                # se agrega la ficha

                pygame.display.update()

            if lado == "izquierdo":
                # misma lógica que antes pero acá la ficha de la izquierda del deque es la [0]
                print("izquierdo")
                ficha_derecha = tablero_fisico[0]
                x_anterior, y_anterior = ficha_derecha[1]

                if ficha_derecha[-1]:
                    # si la ficha de la derecha (anterior) es doble
                    self.screen.blit(ficha_transformada, (x_anterior - int((270 / 4)), y_anterior + 20))
                    tablero_fisico.appendleft(
                        (ficha_transformada, (x_anterior - int((270 / 4)), y_anterior + 20), False))

                elif mi_ficha.esDoble():
                    ficha_transformada = pygame.transform.rotate(ficha_transformada, 90)

                    self.screen.blit(ficha_transformada, (x_anterior - int((270 / 8)), y_anterior - 20))
                    # acá en lugar de sumar hay que restar en x.

                    tablero_fisico.appendleft(
                        (ficha_transformada, (x_anterior - int((270 / 8)), y_anterior - 20), True))
                else:
                    self.screen.blit(ficha_transformada, (x_anterior - int((270 / 4)), y_anterior))
                    # acá en lugar de sumar hay que restar en x.

                    tablero_fisico.appendleft((ficha_transformada, (x_anterior - int((270 / 4)), y_anterior), False))
                # IMPORTANTE: se agrega la ficha al inicio
                pygame.display.update()

            tirar = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sonidos/tirar_ficha0.mp3"))
            tirar.play()


    def __init__(self):
        self.ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")
        self.lista_botones = []

        # Inicializar Pygame
        pygame.init()
        self.ancho = 1920
        self.alto = 1080
        self.screen = pygame.display.set_mode((self.ancho, self.alto), pygame.FULLSCREEN)

        # Establecer el título de la ventana
        pygame.display.set_caption("Mi Juego")

        # Establecer el color de fondo de la ventana
        self.background_color = (0, 128, 10)

        # Establecer el estado de la ventana a "abierto"
        self.is_running = True

    def run(self):
        tablero_fisico = deque()  # tablero que representa el juego (físicamente)
        tablero_logico = deque()  # tablero que representa el juego (logicamente)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "sonidos/background.mp3"))
        pygame.mixer_music.play(-1)

        # generación de fichas (PRUEBA)
        partida = Tablero()
        partida.generar_fichas()

        # primer turno
        proximo_jugador = partida.encontrarSaque()
        ficha_saque = proximo_jugador.buscarFicha(6, 6)
        print(f"El jugador que tenía la 6,6 era {proximo_jugador.getNombre()}")
        proximo_jugador.eliminarFicha(ficha_saque)

        jugador_principal = partida.getJugadores()[0]

        # siguiente turno
        proximo_jugador_indice = (partida.getJugadores().index(proximo_jugador) + 1) % 4
        proximo_jugador = partida.getJugadores()[proximo_jugador_indice]

        self.screen.fill(self.background_color)
        pygame.display.update()

        # generación de fichas POV jugador
        def generar_pov_jugador(fichas_jugador_principal):
            self.lista_botones.clear()
            ancho_total_fichas = (128 * 7)
            posicion_x = (self.ancho - ancho_total_fichas) / 2

            posicion_y = 700
            separacion = 10
            fondo = pygame.Surface((ancho_total_fichas + 128, 400))
            fondo.fill((0, 128, 0))
            self.screen.blit(fondo, (posicion_x, posicion_y - 100))

            for j in range(0, len(fichas_jugador_principal)):
                ficha_dibujar = fichas_jugador_principal[j]
                ficha_rotada = pygame.transform.rotate(ficha_dibujar.getImagen(), 90)
                if ficha_dibujar.esValida(tablero_logico)[0]:
                    # posiciona las fichas, realiza varias traslaciones en base a unas posiciones iniciales
                    self.posicionarFicha(ficha_rotada, posicion_x, posicion_y, ficha_dibujar, tablero_logico)
                else:
                    self.screen.blit(ficha_rotada, (posicion_x, posicion_y))

                posicion_x += 128 + separacion
            pygame.display.flip()

        self.ponerFicha(tablero_fisico, ficha_saque.getImagen(), "derecho", ficha_saque)
        tablero_logico.append(ficha_saque)
        generar_pov_jugador(jugador_principal.getFichas())

        def mostrarFichasRivales(jugador: Jugador, cord_x, cord_y):
            # Dibujar fondo
            fondo = pygame.Surface((200, 75))
            fondo.fill((0, 100, 10))
            self.screen.blit(fondo, (cord_x - 10, cord_y - 35))
            # Poner texto
            font = pygame.font.SysFont('Arial', 18)
            text = font.render(f'Fichas del {jugador.getNombre()}', True, (255, 255, 255))
            self.screen.blit(text, (cord_x, cord_y - 30))
            separa = 5
            for _ in jugador.getFichas():
                pygame.draw.rect(self.screen, (255, 255, 255), (cord_x, cord_y, 20, 30))
                cord_x += 20 + separa
            pygame.display.flip()
            return cord_x

        def ponerFichaDoble(listaFichasValidas):
            fichasDobles = [elemento[0] for elemento in listaFichasValidas if elemento[0].esDoble()] #poner que retorne esta lista

            #Si hay dos fichas dobles
            if len(fichasDobles) == 2:
                #Boton de pone ficha doble
                posBoton = (1120,500) #cambiar
                #boton tamaño
                tamBoton = (100,50)
                BotonDoble = pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(posBoton, tamBoton)) #ponerle un color como verde
                # Crear una fuente para el texto
                font = pygame.font.Font(None, 22)
                # Renderizar el texto en una superficie
                text_surface = font.render('Poner dobles', True, (0, 0, 0))
                # Obtener el rectángulo del texto
                text_rect = text_surface.get_rect()
                # Centrar el rectángulo del texto en el botón
                text_rect.center = BotonDoble.center
                # Dibujar el texto en la pantalla
                self.screen.blit(text_surface, text_rect)
                pygame.display.flip()
                return BotonDoble, fichasDobles
            
            else: #si no hay fichas dobles - esto se podria borrar y poner que se coloree del mismo color que el tablero ese espacio
                #Boton de pone ficha doble
                posBoton = (1120, 500) #cambiar
                #boton tamaño
                tamBoton = (100,50)
                BotonDoble = pygame.draw.rect(self.screen, (0,128,10), pygame.Rect(posBoton, tamBoton)) #ponerle un color como rojo
                # Crear una fuente para el texto
                font = pygame.font.Font(None, 22)
                # Renderizar el texto en una superficie
                text_surface = font.render('Poner dobles', True, (0, 128, 10))
                # Obtener el rectángulo del texto
                text_rect = text_surface.get_rect()
                # Centrar el rectángulo del texto en el botón
                text_rect.center = BotonDoble.center
                # Dibujar el texto en la pantalla
                self.screen.blit(text_surface, text_rect)
                pygame.display.flip()
                return BotonDoble, fichasDobles

        def mostrarFichasTurno(jugador, cord_x, cord_y):
            # Dibujar fondo
            fondo = pygame.Surface((700, 50))
            fondo.fill((0, 128, 10))
            self.screen.blit(fondo, (cord_x - 10, cord_y - 40))
            # Poner texto
            font = pygame.font.SysFont('Arial', 26)

            if partida.getJugadores()[0] == jugador:
                fichas_validas = jugador.determinarFichasValidas(tablero_logico)
                if len(fichas_validas) == 0:
                    text = font.render("No tienes fichas para jugar, oprime el boton de pasar", True, (255, 255, 255))
                    self.screen.blit(text, (cord_x, cord_y - 30))
                else:
                    text = font.render("Es tu turno!", True, (255, 255, 255))
                    self.screen.blit(text, (cord_x, cord_y - 30))
            else:
                fichas_validas = jugador.determinarFichasValidas(tablero_logico)
                if len(fichas_validas) == 0:
                    text = font.render(f"El {jugador.getNombre()} no tiene fichas para jugar. Saltando turno...", True,
                                       (255, 255, 255))
                    self.screen.blit(text, (cord_x, cord_y - 30))
                else:
                    text = font.render(f"Turno de {jugador.getNombre()}", True, (255, 255, 255))
                    self.screen.blit(text, (cord_x, cord_y - 30))

            pygame.display.flip()

        # Boton de pasar
        posBoton = (1000, 500)
        # botn tamañó
        tamBoton = (100, 50)
        BotonPass = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(posBoton, tamBoton))
        # Crear una fuente para el texto
        font = pygame.font.Font(None, 30)
        # Renderizar el texto en una superficie
        text_surface = font.render('Pasar', True, (0, 0, 0))
        # Obtener el rectángulo del texto
        text_rect = text_surface.get_rect()
        # Centrar el rectángulo del texto en el botón
        text_rect.center = BotonPass.center
        # Dibujar el texto en la pantalla
        self.screen.blit(text_surface, text_rect)
        """
        # no se si debo actualizar la pantalla
        pygame.display.flip()
        """

        # Boton de salir
        posSalir = (70, 50)
        # botn tamañó
        tamBotonSalir = (100, 50)
        BotonSalir = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(posSalir, tamBotonSalir))
        # Crear una fuente para el texto
        font = pygame.font.Font(None, 30)
        # Renderizar el texto en una superficie
        text_surface = font.render('Salir', True, (0, 0, 0))
        # Obtener el rectángulo del texto
        text_rect = text_surface.get_rect()
        # Centrar el rectángulo del texto en el botón
        text_rect.center = BotonSalir.center
        # Dibujar el texto en la pantalla
        self.screen.blit(text_surface, text_rect)

        contador = 0
        # partida.verEstado()
        Ganado = False
        while self.is_running:
            if not Ganado:


                # mostrar fichas si nadie ha ganado
                razon = (self.ancho - 380) / 4
                for i in range(3, 0, -1):
                    mostrarFichasRivales(partida.getJugadores()[i], razon, 50)
                    razon += self.ancho / 4

                for participante in partida.getJugadores():  # Mirar si alguien ganó
                    if len(participante.getFichas()) == 0:
                        pygame.mixer_music.stop()
                        Ganado = True
                        print(f"Ganó {participante.getNombre()}")
                        #sleep(1.5)
                        self.dibujarGanador(participante, partida)
                        break
                if contador == 4:
                    pygame.mixer_music.stop()
                    Ganado = True
                    ganador = partida.getGanadorPorPuntaje()
                    #suspenso
                    fondo_suspenso = pygame.Surface((self.ancho, self.alto))
                    fondo_suspenso.fill((38, 36, 36))

                    self.screen.blit(fondo_suspenso, (0, 0))
                    pygame.display.update()

                    suspenso = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__),
                                                               "sonidos/suspenso.mp3"))
                    suspenso.play()
                    fuente_suspenso = pygame.font.Font(None, 70)


                    text_suspenso = fuente_suspenso.render("El ganador se elegirá por puntos", True,
                                                           (255, 255, 255))


                    self.screen.blit(text_suspenso, (self.ancho // 2 - 350, self.alto // 2 - 80))
                    pygame.display.update()

                    sleep(3)
                    self.screen.blit(fondo_suspenso, (0, 0))
                    pygame.display.update()
                    sleep(2)

                    text_suspenso = fuente_suspenso.render("Y el ganador es...", True,
                                                           (255, 255, 255))

                    self.screen.blit(text_suspenso, (self.ancho // 2 - 200, self.alto // 2 - 80))
                    pygame.display.update()



                    sleep(4)


                    self.dibujarGanador(ganador, partida, True)

            # Procesar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Si el usuario cierra la ventana, establecer el estado a "cerrado"
                    self.is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # boton de salir
                    if BotonSalir.collidepoint(pos):
                        self.is_running = False

                """"
                elif event.type == pygame.VIDEORESIZE:
                    # Actualiza el tamaño de la ventana
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                pygame.display.update()"""

                # Turno de nosotros
                if not Ganado:

                    if partida.getJugadores()[0] == proximo_jugador:
                        mostrarFichasTurno(proximo_jugador, 200, 550)
                        fichas_validas = proximo_jugador.determinarFichasValidas(tablero_logico)
                        BotonDoble, fichasDobles = ponerFichaDoble(fichas_validas)

                        if len(fichas_validas) == 0:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                # boton de pasar
                                if BotonPass.collidepoint(pos):
                                    proximo_jugador_indice = (partida.getJugadores().index(proximo_jugador) + 1) % 4
                                    proximo_jugador = partida.getJugadores()[proximo_jugador_indice]
                                    # ver si hacer algo con el contador
                                    pasar = pygame.mixer.Sound(
                                        os.path.join(os.path.dirname(__file__), "sonidos/pasar.mp3"))
                                    pasar.play()
                                    print("boton pasar clickeado")
                                    contador += 1
                                    break

                        else:  # tiene fichas para jugar

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                # boton de pasar
                                if BotonPass.collidepoint(pos):
                                    proximo_jugador_indice = (partida.getJugadores().index(proximo_jugador) + 1) % 4
                                    proximo_jugador = partida.getJugadores()[proximo_jugador_indice]
                                    # ver si hacer algo con el contador
                                    pasar = pygame.mixer.Sound(
                                        os.path.join(os.path.dirname(__file__), "sonidos/pasar.mp3"))
                                    pasar.play()
                                    print("boton pasar clickeado")
                                    contador += 1
                                    break
                                if BotonDoble.collidepoint(pos): # que recorra la lista y las fichas las ponga con el metodo poner ficha, y que cambie de turno
                                    if len(fichasDobles)==2: #condicionales por si tiene mas de una ficha doble valida o no
                                        for mi_ficha in fichasDobles:
                                            if mi_ficha.esValida(tablero_logico)[1][0]: #es valida en la izquierda
                                                self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "izquierdo", v=[-1,0] )
                                                tablero_logico.appendleft(mi_ficha)
                                                jugador_principal.getFichas().remove(mi_ficha)
                                                generar_pov_jugador(jugador_principal.getFichas())

                                            elif mi_ficha.esValida(tablero_logico)[1][1]: #es valida en la derecha
                                                self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "derecho")
                                                tablero_logico.append(mi_ficha)
                                                jugador_principal.getFichas().remove(mi_ficha)
                                                generar_pov_jugador(jugador_principal.getFichas())
                                        
                                        proximo_jugador_indice = (partida.getJugadores().index(proximo_jugador) + 1) % 4
                                        proximo_jugador = partida.getJugadores()[proximo_jugador_indice]
                                        contador = 0
                                                                                       
                                        print("boton poner dobles clickeado") #aqui hacer que ponga las 2 fichas y rompa
                                        break
                                    elif len(fichasDobles)>0: #caso de prueba que funcione, se puede borrar
                                        for mi_ficha in fichasDobles:
                                            if mi_ficha.esValida(tablero_logico)[1][0]: #es valida en la izquierda
                                                self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "izquierdo", v=[-1,0] )
                                                tablero_logico.appendleft(mi_ficha)

                                                jugador_principal.getFichas().remove(mi_ficha)
                                                generar_pov_jugador(jugador_principal.getFichas())
                                                
                                            elif mi_ficha.esValida(tablero_logico)[1][1]: #es valida en la derecha
                                                self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "derecho")
                                                tablero_logico.append(mi_ficha)
                                                jugador_principal.getFichas().remove(mi_ficha)
                                        
                                        proximo_jugador_indice = (partida.getJugadores().index(
                                        proximo_jugador) + 1) % 4
                                        proximo_jugador = partida.getJugadores()[proximo_jugador_indice]
                                        contador = 0
                                        print("boton poner dobles clickeado") # aqui que no pase nada
                                        break
                                    else:
                                        print("No tienes fichas dobles validas")
                                        pass
                                for i, tupla_boton in enumerate(self.lista_botones):
                                    mi_ficha = fichas_validas[i][0]
                                    print(mi_ficha.getValores())
                                    if tupla_boton[0].collidepoint(pos):        
                                        coordenadas_boton = tupla_boton[0].center
                                        color = self.screen.get_at(coordenadas_boton)
                                        if color == (255, 0, 0, 255):
                                            print("jugada invalida")
                                            continue
                                        else:
                                            self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "izquierdo",
                                                         v=[-1, 0])
                                            seleccionar = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__),
                                                                                          "sonidos/seleccionar_lado_derecho.mp3"))
                                            seleccionar.play()
                                            tablero_logico.appendleft(mi_ficha)

                                            jugador_principal.getFichas().remove(mi_ficha)
                                            generar_pov_jugador(jugador_principal.getFichas())
                                            proximo_jugador_indice = (partida.getJugadores().index(
                                                proximo_jugador) + 1) % 4
                                            proximo_jugador = partida.getJugadores()[proximo_jugador_indice]
                                            contador = 0
                                            break

                                    elif tupla_boton[1].collidepoint(pos):
                                        coordenadas_boton = tupla_boton[1].center
                                        color = self.screen.get_at(coordenadas_boton)
                                        if color == (255, 0, 0, 255):
                                            print("jugada invalida")
                                            continue
                                        else:
                                            self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "derecho")
                                            seleccionar = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__),
                                                                                          "sonidos/seleccionar_lado_derecho.mp3"))
                                            seleccionar.play()
                                            tablero_logico.append(mi_ficha)
                                            jugador_principal.getFichas().remove(mi_ficha)
                                            generar_pov_jugador(jugador_principal.getFichas())
                                            proximo_jugador_indice = (partida.getJugadores().index(
                                                proximo_jugador) + 1) % 4
                                            proximo_jugador = partida.getJugadores()[proximo_jugador_indice]
                                            contador = 0
                                            break

                    # Ciclo principal del juego
                    if not (partida.getJugadores()[0] == proximo_jugador):
                        # Simular entrada del mouse
                        pygame.mouse.set_pos(pygame.mouse.get_pos())
                        mostrarFichasTurno(proximo_jugador, 200, 550)
                        ponerFichaDoble(partida.getJugadores()[0].determinarFichasValidas(tablero_logico))
                        partida.verEstado()
                        fichas_validas = proximo_jugador.determinarFichasValidas(tablero_logico)
                        if len(fichas_validas) == 0:
                            print(f"{proximo_jugador.getNombre()} no tiene fichas para jugar, se pasa al otro jugador")
                            sleep(2)
                            proximo_jugador_indice = (partida.getJugadores().index(proximo_jugador) + 1) % 4
                            proximo_jugador = partida.getJugadores()[proximo_jugador_indice]
                            contador += 1

                        else:
                            print(f"saca el {proximo_jugador.getNombre()}")
                            sleep(1)
                            print(f"{proximo_jugador.getNombre()} va a jugar...")
                            sleep(2)

                            lado = []

                            datos_ficha = fichas_validas[randint(0, len(fichas_validas) - 1)]
                            tupla_condicion = datos_ficha[1]
                            if tupla_condicion[0]:
                                lado.append("izquierdo")
                            if tupla_condicion[1]:
                                lado.append("derecho")

                            mi_ficha = datos_ficha[0]
                            print(f"Valores rival: {mi_ficha.getValores()}")
                            lado_str = lado[randint(0, len(lado) - 1)]
                            if lado_str == "derecho":
                                self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "derecho")
                                tablero_logico.append(mi_ficha)
                                proximo_jugador.getFichas().remove(mi_ficha)
                                generar_pov_jugador(jugador_principal.getFichas())


                            elif lado_str == "izquierdo":
                                self.dibujar(mi_ficha, tablero_logico, tablero_fisico, "izquierdo", v=[-1, 0])
                                tablero_logico.appendleft(mi_ficha)
                                proximo_jugador.getFichas().remove(mi_ficha)
                                generar_pov_jugador(jugador_principal.getFichas())

                            proximo_jugador_indice = (partida.getJugadores().index(proximo_jugador) + 1) % 4
                            proximo_jugador = partida.getJugadores()[proximo_jugador_indice]
                            break

                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.is_running = False

            # Dibujar el fondo

            # Actualizar la pantalla
            pygame.display.update()

        # Salir de Pygame
        pygame.mixer.music.stop()
        pygame.quit()

    def dibujarGanador(self, participante, partida, porPuntos=False):
        fondo_relleno = pygame.Surface((self.ancho, self.alto))

        fuente_ganar = pygame.font.Font(None, 70)
        if participante == partida.getJugadores()[0]:

            fondo_relleno.fill((0, 128, 10))
            self.screen.blit(fondo_relleno, (0, 0))
            sonido_ganar = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sonidos/ganar.mp3"))
            sonido_ganar.play()

            text = fuente_ganar.render("Ganaste!", True,
                                       (255, 255, 255))

            if porPuntos:
                text = fuente_ganar.render(f"Ganaste con {participante.calcularPuntos()} puntos", True,
                                           (255, 255, 255))

                self.screen.blit(text, (self.ancho // 2 - 250, self.alto // 2 - 80))
            else:
                self.screen.blit(text, (self.ancho // 2 - 100, self.alto // 2 - 80))

        else:
            fondo_relleno.fill((255, 0, 0))
            self.screen.blit(fondo_relleno, (0, 0))
            sonido_perder = pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), "sonidos/perder.mp3"))
            sonido_perder.play()

            text = fuente_ganar.render(f"Ganó {participante.getNombre()}", True,
                                       (255, 255, 255))

            if porPuntos:
                text = fuente_ganar.render(
                    f"Ganó {participante.getNombre()} con {participante.calcularPuntos()} puntos", True,
                    (255, 255, 255))

                self.screen.blit(text, (self.ancho // 2 - 300, self.alto // 2 - 80))
            else:
                self.screen.blit(text, (self.ancho // 2 - 100, self.alto // 2 - 80))
