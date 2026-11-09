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
brown = [196, 164, 132]

gravity = 1

def draw_platform():
    global platform_surf
    platform_points = [(0, 0), (100, 0), (100, 10), (0, 10)]
    platform_surf = py.Surface((100, 10))
    py.draw.polygon(platform_surf, brown, platform_points)
draw_platform()

platforms = [
    platform_surf.get_rect(center = (250, 450))
]

for i in range(8):
    platforms.append(platform_surf.get_rect(center = (450 + i * 200, 450 if (i + 1) % 2 == 1 else 460)))

def draw_gradient(w, h, c_top, c_bottom):
    bg_surf = py.Surface((1, 2))
    bg_surf.set_at((0, 0), c_top)
    bg_surf.set_at((0, 1), c_bottom)
    grad_surf = py.transform.smoothscale(bg_surf, (w, h))
    return grad_surf
class Player:
    def __init__(self, x, y):
        self.rect = py.Rect(x, y, 20, 20)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 3
        self.jump_power = -15
        self.on_ground = False
    def key_input(self):
        keys = py.key.get_pressed()
        self.vel_x  = 0
        if keys[py.K_LEFT]:
            self.vel_x = -1 * self.speed
        if keys[py.K_RIGHT]:
            self.vel_x = self.speed
        if keys[py.K_UP] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
    def update(self, platforms):
        self.key_input()
        self.vel_y += gravity
        self.rect.x += self.vel_x
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_x > 0:
                    self.rect.right = platform.left
                elif self.vel_x < 0:
                    self.rect.left = platform.right
        self.rect.y += self.vel_y
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0
    def draw(self, surface, scroll_x):
        py.draw.rect(surface, red, (self.rect.x - scroll_x, self.rect.y, self.rect.width, self.rect.height))

player = Player(250, 400)
scroll_x = 0
level_width = 1200

bg = draw_gradient(width, height/2, blue, green)
bg_2 = draw_gradient(width, height/2, blue, green)
clock = py.time.Clock()
run = True
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    player.update(platforms)

    target_scroll_x = player.rect.x - (width // 2)
    scroll_x += (target_scroll_x - scroll_x) / 10

    if scroll_x < 0:
        scroll_x = 0
    if scroll_x > level_width:
        scroll_x = level_width

    screen.blit(bg, (0, 0))
    screen.blit(bg_2, (0, height/2))
    py.draw.rect(screen, black, (0, height/2 - 1, width, 2), width=0)
    for platform in platforms:
        screen.blit(platform_surf, (platform.x - scroll_x, platform.y))
    player.draw(screen, scroll_x)
    py.display.flip()
    clock.tick(60)

py.quit()
sys.exit()