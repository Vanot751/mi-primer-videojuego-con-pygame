import pygame
import sys
import math

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO, ALTO = 800, 600
FPS = 60
GRAVEDAD = 0.8
COLOR_FONDO = (20, 20, 20)
COLOR_JUGADOR = (0, 255, 0)
COLOR_PLATAFORMA = (139, 69, 19)
COLOR_ENEMIGO = (255, 0, 0)
COLOR_GANCHO = (0, 0, 255)

# Crear ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Microjuego de Plataformas 2D")

# Reloj
reloj = pygame.time.Clock()

# Clases
class Jugador(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60)
        self.vel_y = 0
        self.en_suelo = False
        self.ganchado = False
        self.gancho_pos = None

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.x -= 5
        if teclas[pygame.K_RIGHT]:
            self.x += 5
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = -15
            self.en_suelo = False

    def aplicar_gravedad(self):
        if not self.ganchado:
            self.vel_y += GRAVEDAD
            self.y += self.vel_y

    def colisiones(self, plataformas):
        self.en_suelo = False
        for plataforma in plataformas:
            if self.colliderect(plataforma):
                if self.vel_y > 0:
                    self.bottom = plataforma.top
                    self.vel_y = 0
                    self.en_suelo = True

    def usar_gancho(self, mouse_pos):
        dx = mouse_pos[0] - self.centerx
        dy = mouse_pos[1] - self.centery
        distancia = math.hypot(dx, dy)
        if distancia < 200:
            self.ganchado = True
            self.gancho_pos = mouse_pos

    def balancear(self):
        if self.ganchado and self.gancho_pos:
            dx = self.gancho_pos[0] - self.centerx
            dy = self.gancho_pos[1] - self.centery
            angulo = math.atan2(dy, dx)
            self.x += int(math.cos(angulo) * 5)
            self.y += int(math.sin(angulo) * 5)

    def soltar_gancho(self):
        self.ganchado = False
        self.gancho_pos = None

class Enemigo(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
        self.direccion = 1

    def mover(self):
        self.x += self.direccion * 2
        if self.x < 100 or self.x > 700:
            self.direccion *= -1

# Crear plataformas tipo cueva
plataformas = [
    pygame.Rect(0, ALTO - 40, ANCHO, 40),
    pygame.Rect(150, 450, 100, 20),
    pygame.Rect(300, 350, 100, 20),
    pygame.Rect(500, 250, 100, 20),
    pygame.Rect(650, 150, 100, 20)
]

# Crear jugador y enemigos
jugador = Jugador(100, ALTO - 100)
enemigos = [Enemigo(400, ALTO - 80)]

# Pantalla de inicio
def pantalla_inicio():
    fuente = pygame.font.SysFont(None, 48)
    texto = fuente.render("Presiona ENTER para comenzar", True, (255, 255, 255))
    while True:
        pantalla.fill(COLOR_FONDO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return

# Bucle principal
def juego():
    while True:
        reloj.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                jugador.usar_gancho(pygame.mouse.get_pos())
            if evento.type == pygame.MOUSEBUTTONUP:
                jugador.soltar_gancho()

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)
        jugador.aplicar_gravedad()
        jugador.colisiones(plataformas)
        if jugador.ganchado:
            jugador.balancear()

        for enemigo in enemigos:
            enemigo.mover()
            if jugador.colliderect(enemigo):
                pantalla_inicio()
                jugador.x, jugador.y = 100, ALTO - 100

        pantalla.fill(COLOR_FONDO)
        pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador)
        for plataforma in plataformas:
            pygame.draw.rect(pantalla, COLOR_PLATAFORMA, plataforma)
        for enemigo in enemigos:
            pygame.draw.rect(pantalla, COLOR_ENEMIGO, enemigo)
        if jugador.ganchado and jugador.gancho_pos:
            pygame.draw.line(pantalla, COLOR_GANCHO, jugador.center, jugador.gancho_pos, 2)

        pygame.display.flip()

# Ejecutar juego
pantalla_inicio()
juego()
