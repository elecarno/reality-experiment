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

FONT = pygame.font.SysFont("couriernew", 16)

class Particle:    
    SCALE = 2
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
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.color, (x, y), self.RADIUS)

        if len(self.path) > 2:
            updated_points = []
            for point in self.path:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            if len(self.path) > 100:
                self.path.pop(0)

            if show_trails:
                pygame.draw.lines(win, self.color, False, updated_points, 2)

        vector_scale = 1
        if show_vectors:
            #pygame.draw.line(win, COL_RED, (x,y), (x, y+self.y_vel*vector_scale), 2)
            #pygame.draw.line(win, COL_GREEN, (x,y), (x+self.x_vel*vector_scale, y), 2)
            pygame.draw.line(win, COL_YELLOW, (x,y), (x+self.x_vel*vector_scale, y+self.y_vel*vector_scale), 2)

    def update_position(self):
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # window border collision
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if x <= 0 or x >= WIDTH:
            self.x_vel = -self.x_vel

        if y <= 0 or y >= HEIGHT:
            self.y_vel = -self.y_vel
        # window border collision

        self.path.append((self.x, self.y))


class Aether(Particle):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color)
        self.size = size
        self.links = []

    def draw_size(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        size_text = FONT.render(f"{round(self.size, 1)}", 1, COL_WHITE)
        win.blit(size_text, (x - size_text.get_width()/2, y+10))

    def avoidance(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        # avoidance force
        force = -(1 / (self.size * math.sqrt(distance)))

        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def check_for_chaining(self, win, particles):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        for particle in particles:
            if self == particle:
                continue

            other_x, other_y = particle.x, particle.y
            distance_x = other_x - self.x
            distance_y = other_y - self.y
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
            
            idx = particles.index(particle)

            if distance < 10 * self.SCALE:
                #print(f"dist {particles.index(self)} {particles.index(particle)}")
                if len(self.links) < 1:
                    self.links.append(idx)
            # else:
            #     if idx in self.links:
            #         self.links.remove(idx)

        for linked_p in self.links:
            px = particles[linked_p].x * self.SCALE + WIDTH / 2
            py = particles[linked_p].y * self.SCALE + HEIGHT / 2

            pygame.draw.line(win, COL_GREEN, (x,y), (px, py), 4)

    def calculate_velocities(self, win, particles):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        total_fx = total_fy = 0
        for particle in particles:
            if self == particle:
                continue

            fx, fy = self.avoidance(particle)
            total_fx += fx
            total_fy += fy

        # a = F^2 * s
        self.x_vel += math.pow(total_fx, 2) * self.size * self.TIMESTEP
        self.y_vel += math.pow(total_fy, 2) * self.size * self.TIMESTEP

        vector_scale = 10
        pygame.draw.line(win, COL_RED, (x,y), (x+total_fx*vector_scale, y+total_fy*vector_scale), 2)


def main():
    global show_vectors
    global show_trails
    show_vectors = False
    show_trails = True

    run = True
    clock = pygame.time.Clock()

    aether_particles = []

    for i in range(20):
        x = random.randrange(-60, 60)
        y = random.randrange(-60, 60)
        size = random.uniform(0.1, 1)
        aether = Aether(x, y, COL_WHITE, size)
        aether_particles.append(aether)

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


        for aether in aether_particles:
            aether.check_for_chaining(WIN, aether_particles)
            aether.calculate_velocities(WIN, aether_particles)
            aether.update_position()
            aether.draw(WIN)
            aether.draw_size(WIN)
        
        pygame.display.update()

    pygame.quit()

main()