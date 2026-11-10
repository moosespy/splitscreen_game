import pygame as py
import sys

py.init()
width = 600
height = 500
screen = py.display.set_mode((width, height), py.DOUBLEBUF)
p1_surface = py.Surface((width, height/2))
p2_surface = py.Surface((width, height/2))

font = py.font.SysFont('dejavusansmono', 16)

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
orange = [255, 165, 0]
black = [0, 0, 0]
white = [255, 255, 255]
brown = [196, 164, 132]

gravity = 1

def draw_platform():
    global platform_surf
    platform_points = [(0, 0), (100, 0), (100, 10), (0, 10)]
    platform_surf = py.Surface((100, 10))
    py.draw.polygon(platform_surf, brown, platform_points)
draw_platform()

platforms = []

for i in range(9):
    platforms.append(platform_surf.get_rect(center = (300 + i * 150, 120 if (i + 1) % 2 == 1 else 110)))
    platforms.append(platform_surf.get_rect(center = (275 + i * 150, 200 if (i + 1) % 2 == 1 else 190)))

def draw_gradient(w, h, c_top, c_bottom):
    bg_surf = py.Surface((1, 2))
    bg_surf.set_at((0, 0), c_top)
    bg_surf.set_at((0, 1), c_bottom)
    grad_surf = py.transform.smoothscale(bg_surf, (w, h))
    return grad_surf
class Player:
    def __init__(self, x, y, color, controls):
        self.rect = py.Rect(x, y, 18, 18)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 3
        self.shoot_cooldown = 400
        self.last_shot = 0
        self.jump_power = -14
        self.facing = 1
        self.on_ground = False
        self.color = color
        self.controls = controls
    def key_input(self):
        keys = py.key.get_pressed()
        self.vel_x  = 0
        if keys[self.controls['left']]:
            self.vel_x = -1 * self.speed
            self.facing = -1
        if keys[self.controls['right']]:
            self.vel_x = self.speed
            self.facing = 1
        if keys[self.controls['jump']] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
        if keys[self.controls['shoot']]:
            current_time = py.time.get_ticks()
            if current_time - self.last_shot >= self.shoot_cooldown:
                projectiles.append(Projectile(self.rect.centerx, self.rect.centery, self.facing, self.color))
                self.last_shot = current_time
    def update(self, platforms):
        self.key_input()
        if self.vel_y > 15:
            self.vel_y = 15
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10
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
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0
    def draw(self, surface, scroll_x):
        py.draw.rect(surface, self.color, (self.rect.x - scroll_x, self.rect.y, self.rect.width, self.rect.height))

class Projectile:
    def __init__(self, x, y, direction, color):
        self.x = float(x)
        self.y = float(y)
        self.rect = py.Rect(int(self.x), int(self.y), 10, 1)
        self.direction = direction
        self.speed = 5
        self.color = color
        self.distance = 0
    def update(self, platforms):
        max_distance = 400
        move = self.speed * self.direction
        self.x += move
        self.distance += abs(move)
        self.rect.x = int(self.x)
        if self.distance > max_distance:
            return False
        for platform in platforms:
            if self.rect.colliderect(platform):
                return False
        return True
    def draw(self, surface, scroll_x):
        py.draw.rect(surface, self.color, (self.rect.x - scroll_x, self.rect.y, self.rect.width, self.rect.height))
p1_controls = {'left': py.K_LEFT, 'right': py.K_RIGHT, 'jump': py.K_UP, 'shoot': py.K_p}
p2_controls = {'left': py.K_a, 'right': py.K_d, 'jump': py.K_w, 'shoot': py.K_2}
p1_startx, p1_starty, p2_startx, p2_starty = 230, 100, 1500, 100
player1 = Player(p1_startx, p1_starty, red, p1_controls)
player2 = Player(p2_startx, p2_starty, orange, p2_controls)
scroll_x1 = 0
scroll_x2 = 0
level_width = 1200

bg = draw_gradient(width, height/2, blue, green)
bg_2 = draw_gradient(width, height/2, blue, green)
projectiles = []

gamestate = 'playing'

clock = py.time.Clock()
run = True
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    if gamestate == 'playing':
        player1.update(platforms)
        player2.update(platforms)

        target_scroll_x1 = player1.rect.x - (width // 2)
        scroll_x1 += (target_scroll_x1 - scroll_x1) / 10

        if scroll_x1 < 0:
            scroll_x1 = 0
        if scroll_x1 > level_width:
            scroll_x1 = level_width
        if player1.rect.y >= height/2:
            gamestate = 'p2 win'

        target_scroll_x2 = player2.rect.x - (width // 2)
        scroll_x2 += (target_scroll_x2 - scroll_x2) / 10

        if scroll_x2 < 0:
            scroll_x2 = 0
        if scroll_x2 > level_width:
            scroll_x2 = level_width
        if player2.rect.y >= height/2:
            gamestate = 'p1 win'
        for projectile in projectiles[:]:
            alive = projectile.update(platforms)
            if not alive:
                projectiles.remove(projectile)
    if gamestate == 'p1 win':
        win_text = font.render("Player 1 Wins! Press 'r' to restart.", True, white)
        key = py.key.get_pressed()
        if key[py.K_r] == True:
            gamestate = 'playing'
            player1 = Player(p1_startx, p1_starty, red, p1_controls)
            player2 = Player(p2_startx, p2_starty, orange, p2_controls)
            scroll_x1 = 0
            scroll_x2 = 0
    elif gamestate == 'p2 win':
        win_text = font.render("Player 2 Wins! Press 'r' to restart.", True, white)
        key = py.key.get_pressed()
        if key[py.K_r] == True:
            gamestate = 'playing'
            projectiles = []
            player1 = Player(p1_startx, p1_starty, red, p1_controls)
            player2 = Player(p2_startx, p2_starty, orange, p2_controls)
            scroll_x1 = 0
            scroll_x2 = 0


    p1_surface.blit(bg, (0, 0))
    for platform in platforms:
        p1_surface.blit(platform_surf, (platform.x - scroll_x1, platform.y))
    for projectile in projectiles:
        projectile.draw(p1_surface, scroll_x1)
    player1.draw(p1_surface, scroll_x1)
    player2.draw(p1_surface, scroll_x1)

    p2_surface.blit(bg_2, (0, 0))
    for platform in platforms:
        p2_surface.blit(platform_surf, (platform.x - scroll_x2, platform.y))
    for projectile in projectiles:
        projectile.draw(p2_surface, scroll_x2)
    player1.draw(p2_surface, scroll_x2)
    player2.draw(p2_surface, scroll_x2)
    screen.blit(p1_surface, (0, 0))
    screen.blit(p2_surface, (0, height/2))
    if gamestate == 'p1 win' or gamestate == 'p2 win':
        screen.blit(win_text, (width/2 - 200, height/2))
    py.draw.rect(screen, black, (0, height/2 - 1, width, 2), width=0)

    py.display.flip()
    clock.tick(60)

py.quit()
sys.exit()
