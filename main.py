

import pygame
import pygame.locals
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Manzana:
    def __init__(self, pantalla_padre):
        self.pantalla_padre = pantalla_padre
        self.image = pygame.image.load("Pygame/resources/apple.png").convert()
        self.x = 120
        self.y = 120
        
    def dibujar(self):
        self.pantalla_padre.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*40
        self.y = random.randint(1,19)*40

class Snake:
    def __init__(self, pantalla_padre):
        self.pantalla_padre = pantalla_padre
        self.image = pygame.image.load("Pygame/resources/02.png").convert()
        self.direccion = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direccion = 'left'

    def move_right(self):
        self.direccion = 'right'

    def move_up(self):
        self.direccion = 'up'

    def move_down(self):
        self.direccion = 'down'

    def caminar(self):
        #
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        #
        if self.direccion == 'up':
            self.y[0]-= SIZE
        if self.direccion == 'down':
            self.y[0] += SIZE
        if self.direccion == 'left':
            self.x[0] -= SIZE
        if self.direccion == 'right':
            self.x[0] += SIZE

        self.dibujar()

    def dibujar(self):
        for i in range(self.length):
            self.pantalla_padre.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def aumentar_tamaño(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
        
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Leonel Guerrero")

        pygame.mixer.init()
        self.musica_fondo()

        self.surface = pygame.display.set_mode((1280,720))
        self.snake = Snake(self.surface)
        self.snake.dibujar()
        self.manzana = Manzana(self.surface)
        self.manzana.dibujar()

    def musica_fondo(self):
        pygame.mixer.music.load("Pygame/resources/bg_music_1.ogg")
        pygame.mixer.music.play(-1, 0)
    
    def sonido(self,sound_name):
        if sound_name == "crash":
          sound = pygame.mixer.Sound("Pygame/resources/crash.ogg")
        elif sound_name == 'ding':
          sound = pygame.mixer.Sound("Pygame/resources/ding.ogg")

        pygame.mixer.Sound.play(sound)
        #


    def reset(self):
        self.snake = Snake(self.surface)
        self.manzana = Manzana(self.surface)


    def colision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def renderizado(self):
        bg = pygame.image.load("Pygame/resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.renderizado()
        self.snake.caminar()
        self.manzana.dibujar()
        self.puntaje()
        pygame.display.flip()
    
        # Serpiente colisiona con la manzana
        for i in range(self.snake.length):
            if self.colision(self.snake.x[i], self.snake.y[i], self.manzana.x, self.manzana.y):
                self.sonido("ding")
                self.snake.aumentar_tamaño()
                self.manzana.move()


        # Serpiente colisiona con ella misma
        for i in range(3, self.snake.length):
            if self.colision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.sonido("crash")
                raise "Troleaste XD"

        if not (0 <= self.snake.x[0] <= 1280 and 0 <= self.snake.y[0] <= 720):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def puntaje(self):
        font = pygame.font.SysFont('arial',20)
        puntos = font.render(f"Puntaje: {self.snake.length}", True, (255,255,255))
        self.surface.blit(puntos,(900,10))

    def show_game_over(self):
        self.renderizado()
        font = pygame.font.SysFont('arial',20)
        line1 = font.render(f"Troleaste XD: Tu puntaje fue: {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("Para jugar denuevo presiona ENTER, si no ESCAPE", True, (255,255,255))
        self.surface.blit(line2, (200,350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)    
    
if __name__ == "__main__":
    game = Game()
    game.run()