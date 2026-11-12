import pygame as py
import sys
py.init()
width = 600
height = 500
screen = py.display.set_mode((width, height), py.DOUBLEBUF)
p1_surface = py.Surface((width, height/2)).convert()
p2_surface = py.Surface((width, height/2)).convert()

font = py.font.SysFont('dejavusansmono', 25)

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
orange = [255, 85, 0]
yellow = [255, 255, 0]
black = [0, 0, 0]
white = [255, 255, 255]
brown = [196, 164, 132]

gravity = 1

def draw_platform():
    global platform_surf
    platform_points = [(0, 0), (100, 0), (100, 10), (0, 10)]
    platform_surf = py.Surface((100, 10)).convert()
    py.draw.polygon(platform_surf, brown, platform_points)
draw_platform()

platforms = []

for i in range(9):
    platforms.append(platform_surf.get_rect(center = (300 + i * 150, 100)))
    platforms.append(platform_surf.get_rect(center = (225 + i * 150, 190 if (i + 1) % 2 == 1 else 195)))

def draw_gradient(w, h, c_top, c_bottom):
    bg_surf = py.Surface((1, 2))
    bg_surf.set_at((0, 0), c_top)
    bg_surf.set_at((0, 1), c_bottom)
    grad_surf = py.transform.smoothscale(bg_surf, (w, h))
    return grad_surf.convert()
class Player:
    def __init__(self, x, y, color, controls, health, speed, damage):
        self.rect = py.Rect(x, y, 18, 18)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = speed
        self.shoot_cooldown = 400
        self.last_shot = 0
        self.jump_power = -14
        self.facing = 1
        self.on_ground = False
        self.color = color
        self.controls = controls
        self.projectiles = []
        self.health = health
        self.damage = damage
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
        hit_indices = self.rect.collidelistall(platforms)
        for index in hit_indices:
            platform = platforms[index]
            if self.vel_y > 0:
                self.rect.bottom = platform.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:
                self.rect.top = platform.bottom
                self.vel_y = 0
    def draw(self, surface, scroll_x):
        py.draw.rect(surface, self.color, (round(self.rect.x - scroll_x), self.rect.y, self.rect.width, self.rect.height))

class Projectile:
    def __init__(self, x, y, direction, color):
        self.x = float(x)
        self.y = float(y)
        self.rect = py.Rect(int(self.x), int(self.y), 20, 2)
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
        py.draw.rect(surface, self.color, (round(self.x - scroll_x), self.rect.y, self.rect.width, self.rect.height))

def reset_game():
    p1 = Player(p1_startx, p1_starty, red, p1_controls, 10, 8, 1)
    p2 = Player(p2_startx, p2_starty, green, p2_controls, 10, 4, 2)
    return p1, p2, 0, 0, 'menu'
p1_controls = {'left': py.K_LEFT, 'right': py.K_RIGHT, 'jump': py.K_UP, 'shoot': py.K_p}
p2_controls = {'left': py.K_a, 'right': py.K_d, 'jump': py.K_w, 'shoot': py.K_2}
p1_startx, p1_starty, p2_startx, p2_starty = 230, 100, 1500, 100
level_width = 1200

player1, player2, scroll_x1, scroll_x2, gamestate = reset_game()

bg = draw_gradient(width, height/2, blue, black)
bg_2 = draw_gradient(width, height/2, blue, black)
projectiles = []

counter = 0

clock = py.time.Clock()
run = True
while run:
    current_time = py.time.get_ticks()
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        if event.type == py.KEYDOWN:
            if gamestate == 'playing':
                if event.key == player1.controls['shoot']:
                    if current_time - player1.last_shot >= player1.shoot_cooldown:
                        player1.projectiles.append(Projectile(int(player1.rect.right if player1.facing == 1 else player1.rect.left), player1.rect.centery, player1.facing, player1.color))
                        player1.last_shot = current_time
                if event.key == player2.controls['shoot']:
                    if current_time - player2.last_shot >= player2.shoot_cooldown:
                        player2.projectiles.append(Projectile(int(player2.rect.right if player2.facing == 1 else player2.rect.left), player2.rect.centery, player2.facing, player2.color))
                        player2.last_shot = current_time
        if event.type == py.MOUSEBUTTONDOWN:
            mouse_pos = py.mouse.get_pos()
            if button.collidepoint(mouse_pos):
                gamestate = 'playing'
    if gamestate == 'menu':
        button_text = font.render("Press Here to Start Game", True, black)
        button = button_text.get_rect(center = (width//2, height//2))
    if gamestate == 'playing':
        counter += 1
        if counter == 2:
            player1.update(platforms)
            player2.update(platforms)
            counter = 0
        player1.projectiles = [projectile for projectile in player1.projectiles if projectile.update(platforms)]
        player2.projectiles = [projectile for projectile in player2.projectiles if projectile.update(platforms)]

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
        
        if player1.health <= 0:
            gamestate = 'p2 win'
        if player2.health <= 0:
            gamestate = 'p1 win'
    if gamestate == 'p1 win':
        win_text = font.render("Player 1 Wins! Press 'r' to restart. Press 'm' to go to the menu.", True, white)
        win_rect = win_text.get_rect(center = (width // 2, height // 2))
        key = py.key.get_pressed()
        if key[py.K_r] or key[py.K_m]:
            player1, player2, scroll_x1, scroll_x2, gamestate = reset_game()
            if key[py.K_r]:
                gamestate = 'playing'
            projectiles = []
    elif gamestate == 'p2 win':
        win_text = font.render("Player 2 Wins! Press 'r' to restart. Press 'm' to go to the menu.", True, white)
        win_rect = win_text.get_rect(center = (width // 2, height // 2))
        key = py.key.get_pressed()
        if key[py.K_r] or key[py.K_m]:
            player1, player2, scroll_x1, scroll_x2, gamestate = reset_game()
            if key[py.K_r]:
                gamestate = 'playing'
            projectiles = []

    intscrollx1 = int(scroll_x1)
    intscrollx2 = int(scroll_x2)
    
    p1_surface.blit(bg, (0, 0))
    p2_surface.blit(bg_2, (0, 0))
    for platform in platforms:
        p1_surface.blit(platform_surf, (platform.x - intscrollx1, platform.y))
    for projectile in player2.projectiles[:]:
        projectile.draw(p2_surface, intscrollx2)
        projectile.draw(p1_surface, intscrollx1)
        if projectile.rect.colliderect(player1):
            player2.projectiles.remove(projectile)
            player1.health -= player2.damage
    if gamestate != 'menu':
        player1.draw(p1_surface, intscrollx1)
        player2.draw(p1_surface, intscrollx1)

    for platform in platforms:
        p2_surface.blit(platform_surf, (platform.x - intscrollx2, platform.y))
    for projectile in player1.projectiles[:]:
        projectile.draw(p1_surface, intscrollx1)
        projectile.draw(p2_surface, intscrollx2)
        if projectile.rect.colliderect(player2):
            player1.projectiles.remove(projectile)
            player2.health -= player1.damage
    if gamestate != 'menu':
        player1.draw(p2_surface, intscrollx2)
        player2.draw(p2_surface, intscrollx2)

    health_text = font.render(f"Player 1 Health: {player1.health} | Player 2 Health: {player2.health}", True, white)
    health_rect = health_text.get_rect(center = (width//2, height//2))

    screen.blit(p1_surface, (0, 0))
    screen.blit(p2_surface, (0, height/2))
    if gamestate == 'p1 win' or gamestate == 'p2 win':
        screen.blit(win_text, win_rect)
    elif gamestate == 'playing':
        screen.blit(health_text, health_rect)
    elif gamestate == 'menu':
        button_out = button.inflate(10, 10)
        py.draw.rect(screen, white, button_out, width=1)
        py.draw.rect(screen, yellow, button_out)
        screen.blit(button_text, button)
    py.display.flip()
    clock.tick(60)

py.quit()
sys.exit()
