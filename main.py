import pygame as py
import sys

py.init()
width = 600
height = 500
screen = py.display.set_mode((width, height), py.DOUBLEBUF)

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
black = [0, 0, 0]

def draw_gradient(w, h, c_top, c_bottom):
    bg_surf = py.Surface((1, 2))
    bg_surf.set_at((0, 0), c_top)
    bg_surf.set_at((0, 1), c_bottom)
    grad_surf = py.transform.smoothscale(bg_surf, (w, h))
    return grad_surf

bg = draw_gradient(width, height/2, blue, green)
bg_2 = draw_gradient(width, height/2, blue, green)
clock = py.time.Clock()
run = True
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    screen.blit(bg, (0, 0))
    screen.blit(bg_2, (0, height/2))
    py.draw.rect(screen, black, (0, height/2 - 1, width, 2), width=0)
    py.display.flip()
    clock.tick(60)

py.quit()
sys.exit()