from random import randint
import pygame
import sys


def compute_neighbours(Z):
    start_time = pygame.time.get_ticks()
    shape = len(Z), len(Z[0])
    N = [[0 for i in range(shape[1])] for i in range(shape[0])]
    
    for x in range(1, shape[0]-1):
        for y in range(1, shape[1]-1):
            N[x][y] = Z[x - 1][y - 1] + Z[x][y - 1] + Z[x + 1][y - 1] \
                    + Z[x - 1][y    ]               + Z[x + 1][y    ] \
                    + Z[x - 1][y + 1] + Z[x][y + 1] + Z[x + 1][y + 1]

    print("compute neighbours ", (pygame.time.get_ticks() - start_time)/1000)
    return N


def iterate(Z):
    start_time = pygame.time.get_ticks()
    shape = len(Z), len(Z[0])
    N = compute_neighbours(Z)
    
    for x in range(1, shape[0]-1):
        for y in range(1, shape[1]-1):
            if Z[x][y] and (N[x][y] < 2 or N[x][y] > 3):
                Z[x][y] = not Z[x][y]
            elif not Z[x][y] and N[x][y] == 3:
                Z[x][y] = not Z[x][y]
    
    print("iterate ", (pygame.time.get_ticks() - start_time)/1000)
    return Z


def draw_blocks(screen, xlen, ylen, world, alive_color, block_size):
    start_time = pygame.time.get_ticks()
    for xx in range(xlen):
            for yy in range(ylen):
                alive = world[xx][yy]
                if alive:
                    x = xx * block_size
                    y = yy * block_size
                    center_point = ((x + (block_size / 2)), (y + (block_size / 2)))
                    pygame.draw.rect(screen, alive_color, ((x, y), (block_size, block_size)))

    print("draw ", (pygame.time.get_ticks() - start_time)/1000)


def make_random_grid(x, y):
    grid = [[0 for i in range(y)]]

    for r in range(x-2):
        row = [0]
    
        for c in range(y-2):
            row.append(randint(0, 1))
    
        row.append(0)
        grid.append(row)
    
    grid.append([0 for i in range(y)])
    
    return grid


def main():
    xmax = int(sys.argv[1])
    ymax = int(sys.argv[2])

    fps = int(sys.argv[4])

    screen = pygame.display.set_mode((xmax, ymax))
    clock = pygame.time.Clock()

    h = 0
    alive_color = pygame.Color(0, 255, 0)
    scale = int(sys.argv[3])
    xlen = xmax // scale + 2
    ylen = ymax // scale + 2
    world = make_random_grid(xlen, ylen)
    
    while True:
        screen.fill("black")
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

        draw_blocks(screen, xlen, ylen, world, alive_color, scale)
        
        world = iterate(world)

        pygame.display.set_caption("$~GoL ~fps: " + str(round(clock.get_fps(), 2)))

        pygame.display.flip()
        if not fps:
            clock.tick(fps)

if __name__ == '__main__':
    main()
