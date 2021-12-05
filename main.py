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
    if (Z and (N < 2 or N > 3)) or (not Z and N == 3):
        Z = not Z

    return Z


def draw_blocks(screen, xlen, ylen, world, alive_color, block_size):
    start_time = pygame.time.get_ticks()
    for xx in range(xlen):
        for yy in range(ylen):
            alive = world[xx][yy]
            if alive:
                x = (xx - 1) * block_size
                y = (yy - 1) * block_size
                pygame.draw.rect(screen, alive_color, ((x, y), (block_size, block_size)))

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

    screen = pygame.display.set_mode((xmax, ymax))
    clock = pygame.time.Clock()

    h = 0
    alive_color = pygame.Color(0, 255, 0)
    scale = int(sys.argv[3])
    xlen = xmax // scale + 2
    ylen = ymax // scale + 2
    world = make_random_grid(xlen, ylen)

    viterate = np.vectorize(iterate)
    
    while True:
        screen.fill("black")

        # surf = pygame.surfarray.make_surface(world)
        # surf = pygame.transform.scale(surf, (xlen * scale, ylen * scale))
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

        draw_blocks(screen, xlen, ylen, world, alive_color, scale)
        
        # screen.blit(surf, (0, 0))

        N = compute_neighbours(world)

        start_time = pygame.time.get_ticks()
        world = viterate(world, N)
        print("iterate ", (pygame.time.get_ticks() - start_time)/1000)

        pygame.display.set_caption("$~GoL ~fps: " + str(round(clock.get_fps(), 2)))

        pygame.display.flip()
        clock.tick()

if __name__ == '__main__':
    main()
