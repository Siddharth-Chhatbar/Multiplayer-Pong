import pygame

WIDTH, HEIGHT = 1920, 1080
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 200


class Paddle:
    COLOUR = WHITE
    # TODO: Add a log curve to increase velocity over time
    VELOCITY = 10

    def __init__(self, x, y, width, height) -> None:
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOUR, (self.x, self.y, self.width, self.height))
        return

    def move(self, up=True):
        if up and self.y - self.VELOCITY >= 0:
            self.y -= self.VELOCITY
        elif not up and self.y + self.VELOCITY + self.height <= HEIGHT:
            self.y += self.VELOCITY
        return

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        return


class Ball:
    MAX_VELOCITY = 12
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1
