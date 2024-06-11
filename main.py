import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("reality-experiment-dev")

COL_GRAY =  (25, 25, 25)
COL_WHITE = (220, 220, 220)
COL_RED =   (200, 0, 0)
COL_GREEN = (0, 200, 0)
COL_BLUE =  (0, 0, 200)
COL_YELLOW = (200, 200, 0)

class Particle:    
    TIMESTEP = 1 / 60
    RADIUS = 5

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

        self.path = []

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x + WIDTH / 2
        y = self.y + HEIGHT / 2

        if len(self.path) > 2:
            updated_points = []
            for point in self.path:
                x, y = point
                x = x + WIDTH / 2
                y = y + HEIGHT / 2
                updated_points.append((x, y))

            if len(self.path) > 10:
                self.path.pop(0)

            if show_trails:
                pygame.draw.lines(win, self.color, False, updated_points, 2)

        vector_scale = 0.05
        if show_vectors:
            pygame.draw.line(win, COL_RED, (x,y), (x, y+self.y_vel*vector_scale), 2)
            pygame.draw.line(win, COL_GREEN, (x,y), (x+self.x_vel*vector_scale, y), 2)
            pygame.draw.line(win, COL_YELLOW, (x,y), (x+self.x_vel*vector_scale, y+self.y_vel*vector_scale), 2)

        pygame.draw.circle(win, self.color, (x, y), self.RADIUS)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        force = distance
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_position(self, particles):
        total_fx = total_fy = 0
        for particle in particles:
            if self == particle:
                continue

            fx, fy = self.attraction(particle)
            total_fx = fx
            total_fy = fy

        self.x_vel += total_fx * self.TIMESTEP
        self.y_vel += total_fy * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # window border collision
        x = self.x + WIDTH / 2
        y = self.y + HEIGHT / 2

        if x <= 0 or x >= WIDTH:
            self.x_vel = -self.x_vel

        if y <= 0 or y >= HEIGHT:
            self.y_vel = -self.y_vel
        # window border collision

        self.path.append((self.x, self.y))


def main():
    global show_vectors
    global show_trails
    show_vectors = False
    show_trails = True

    run = True
    clock = pygame.time.Clock()

    particles = []

    for i in range(100):
        x = random.randrange(-WIDTH/2, WIDTH/2)
        y = random.randrange(-HEIGHT/2, HEIGHT/2)
        particle = Particle(x, y, COL_WHITE)
        particles.append(particle)

    while run:
        clock.tick(60)
        WIN.fill(COL_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    show_vectors = not show_vectors
                if event.key == pygame.K_t:
                    show_trails = not show_trails


        for particle in particles:
            particle.update_position(particles)
            particle.draw(WIN)
        
        pygame.display.update()

    pygame.quit()

main()