from random import randint
import numpy as np
import pygame
import sys


def compute_neighbours(Z):
    start_time = pygame.time.get_ticks()

    N = np.zeros_like(Z)
    N[1:-1,1:-1] = Z[:-2,:-2] + Z[1:-1,:-2] + Z[:-2,1:-1] \
                 + Z[2:,:-2]                + Z[2:,1:-1] \
                 + Z[:-2,2:]  + Z[1:-1,2:]  + Z[2:,2:]

    print("compute neighbours ", (pygame.time.get_ticks() - start_time)/1000)
    return N


def iterate(Z, N):
    start_time = pygame.time.get_ticks()

    Z[np.where(N > 3)] = 0
    Z[np.where(N < 2)] = 0
    Z[np.where(N == 3)] = 1
    
    print("iterate ", (pygame.time.get_ticks() - start_time)/1000)


def draw_blocks(screen, xlen, ylen, world, block_size, color):
    start_time = pygame.time.get_ticks()

    surf = pygame.surfarray.make_surface(world * color)
    
    screen.blit(surf, (-1, -1))
    
    print("draw ", (pygame.time.get_ticks() - start_time)/1000)


def make_random_grid(x, y):
    grid = np.random.randint(0, 2, size=(x, y))
    grid[:, 0] *= 0
    grid[:, -1] *= 0
    grid[0] *= 0
    grid[-1] *= 0
    
    return grid


def main():
    xmax = int(sys.argv[1])
    ymax = int(sys.argv[2])

    screen = pygame.display.set_mode((xmax, ymax), pygame.SCALED)
    clock = pygame.time.Clock()

    h = 0
    scale = 1
    xlen = xmax // scale + 2
    ylen = ymax // scale + 2
    world = make_random_grid(xlen, ylen)
    color = 1

    viterate = np.vectorize(iterate)
    
    while True:
        screen.fill("black")

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

        draw_blocks(screen, xlen, ylen, world, scale, color)

        N = compute_neighbours(world)

        iterate(world, N)

        pygame.display.set_caption("$~GoL ~fps: " + str(round(clock.get_fps(), 2)))

        color += 1

        pygame.display.flip()
        clock.tick()

if __name__ == '__main__':
    main()
