import pygame
import numpy as np
import sys
import random

WIDTH, HEIGHT = 576, 1024
GRAVITY = 0.25
BIRD_JUMP = 10
PIPE_GAP = 200
PIPE_VELOCITY = 5
BIRD_WIDTH, BIRD_HEIGHT = 64, 48
PIPE_WIDTH, PIPE_HEIGHT = 100, 800
BACKGROUND_COLOR = (0, 102, 204)

# Initialize Pygame
pygame.init()
pygame.font.init()

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# Set images for bird and pipe
bird_img = pygame.image.load('bird.png').convert_alpha()
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_img = pygame.image.load('pipe.png').convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))


# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.image = bird_img
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def jump(self):
        self.velocity = -BIRD_JUMP

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(200, HEIGHT - PIPE_GAP - 200)
        self.top_rect = pipe_img.get_rect(midbottom=(self.x, self.height))
        self.bottom_rect = pipe_img.get_rect(midtop=(self.x, self.height + PIPE_GAP))

    def move(self):
        self.x -= PIPE_VELOCITY
        self.top_rect = pipe_img.get_rect(midbottom=(self.x, self.height))
        self.bottom_rect = pipe_img.get_rect(midtop=(self.x, self.height + PIPE_GAP))

    def draw(self):
        screen.blit(pipe_img, self.top_rect)
        screen.blit(pipe_img, self.bottom_rect)

def check_collision(bird, pipes):
    if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
        return True
    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
            return True
    return False

def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    font = pygame.font.Font(None, 74)
    score_bg_color = (0, 0, 0)
    score_text_color = (255, 255, 255)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                bird.jump()

        screen.fill(BACKGROUND_COLOR)

        bird.update()
        for pipe in pipes:
            pipe.move()
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe())
                score += 1

        if check_collision(bird, pipes):
            pygame.quit()
            sys.exit()

        bird.draw()
        for pipe in pipes:
            pipe.draw()

        score_text = font.render(str(score), True, score_text_color)
        Flappy_bird = font.render(str('FLAPPY BIRD'), True, (255,255,255))
        score_bg_rect = score_text.get_rect(center=(WIDTH // 2, 200))
        Flappy_rect = Flappy_bird.get_rect(center=(WIDTH // 2, 120))
        pygame.draw.rect(screen, score_bg_color, score_bg_rect.inflate(20, 20))
        screen.blit(score_text, score_bg_rect)
        screen.blit(Flappy_bird, Flappy_rect)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except pygame.error as e:
        print(f"Pygame error: {e}")
