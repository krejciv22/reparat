import pygame
import sys
import math
from pygame.locals import *
import random
import time 

pygame.init()
pygame.display.set_caption("Apocalyps")

# Hodnoty obrazovky
width = 1920
height = 1080

# Rychlost spawnování nepřátel 
enemy_spawn_timer = 0
enemy_spawn_speed = 250  # Každé 3 sekundy 

# Obrázky
window = pygame.display.set_mode((width, height))
background_img = pygame.image.load("images/background.jpg")
background_img = pygame.transform.scale(background_img, (width, height))

first_img = pygame.image.load("images/first.jpg")
first_img = pygame.transform.scale(first_img, (width, height))

# Hrdina
hero_img = pygame.image.load("images/hero.png")
hero_img = pygame.transform.scale(hero_img, (100, 100))
hero_x = width // 2 - 50
hero_y = height // 2 - 50
hero_speed = 5  # RYCHLOST PANACKA
hero_hp = 100
hero_xp = 0
hero_level = 1
hero_shoot_timer = 0

# Koule
bullet_img = pygame.image.load("images/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (30, 30))
bullets = []

# Nepřátelé (enemies)
enemy_img = pygame.image.load("images/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (100, 100))
enemies = []

enemy2_img = pygame.image.load("images/enemy2.png")
enemy2_img = pygame.transform.scale(enemy2_img, (100, 100))


# XP Bar
xp_bar_width = 300
xp_bar_height = 20
xp_bar_fill_color = (0, 128, 0)
xp_bar_background_color = (128, 128, 128)
xp_per_level = 500  # Počet XP potřebných k dosažení další úrovně

# HP Bar
hp_bar_width = 300
hp_bar_height = 20
hp_bar_fill_color = (255, 0, 0)
hp_bar_background_color = (128, 128, 128)

window.blit(first_img, (0, 0))
pygame.display.update()
time.sleep(5)  # Počkej 5 sekund


enemy2_img = pygame.image.load("images/enemy2.png")
enemy2_img = pygame.transform.scale(enemy2_img, (100, 100))
def spawn_enemy():
    side = random.randint(1, 4)
    if side == 1:
        x = 0
        y = random.randint(0, height - enemy_img.get_height())
    elif side == 2:
        x = width - enemy_img.get_width()
        y = random.randint(0, height - enemy_img.get_height())
    elif side == 3:
        x = random.randint(0, width - enemy_img.get_width())
        y = 0
    else:
        x = random.randint(0, width - enemy_img.get_width())
        y = height - enemy_img.get_height()
        
    enemy_type = random.choice([enemy_img, enemy2_img])  # Náhodně vyber jeden ze dvou druhů nepřátel
    return x, y, enemy_type


def check_bullet_enemy_collision(hero_hp):
    global bullets, enemies, hero_xp
    new_bullets = []
    new_enemies = []

    for bullet in bullets:
        bullet_x, bullet_y, bullet_dx, bullet_dy = bullet
        bullet_x += bullet_dx
        bullet_y += bullet_dy

        bullet_rect = bullet_img.get_rect(center=(bullet_x, bullet_y))
        hit_enemy = None

        for enemy in enemies:
            enemy_x, enemy_y, enemy_type = enemy  # Zde přidáme třetí hodnotu (typ nepřítele)
            enemy_rect = enemy_type.get_rect(topleft=(enemy_x, enemy_y))
            if enemy_rect.collidepoint(bullet_rect.center):
                hit_enemy = enemy
                break

        if hit_enemy is None and 0 <= bullet_x <= width and 0 <= bullet_y <= height:
            new_bullets.append((bullet_x, bullet_y, bullet_dx, bullet_dy))

        if hit_enemy is not None:
            enemies.remove(hit_enemy)
            hero_xp += 10

    for enemy in enemies:
        enemy_x, enemy_y, enemy_type = enemy
        dx = hero_x + hero_img.get_width() // 2 - enemy_x - enemy_type.get_width() // 2
        dy = hero_y + hero_img.get_height() // 2 - enemy_y - enemy_type.get_height() // 2
        dist = math.sqrt(dx**2 + dy**2)
        enemy_speed = 2
        enemy_dx = enemy_speed * dx / dist
        enemy_dy = enemy_speed * dy / dist
        enemy_x += enemy_dx
        enemy_y += enemy_dy

        hero_rect = hero_img.get_rect(topleft=(hero_x, hero_y))
        enemy_rect = enemy_type.get_rect(topleft=(enemy_x, enemy_y))
        if enemy_rect.colliderect(hero_rect):
            hero_hp -= 0.3
            if hero_hp <= 0:
                hero_hp = 0

        new_enemies.append((enemy_x, enemy_y, enemy_type))

    bullets = new_bullets
    enemies = new_enemies
    return hero_hp

enemy_spawn_timer = 0
enemy_spawn_speed = 250  # Každé 3 sekundy (60 snímků/s)
enemy_spawn_interval = 600  # Každých 10 sekund (60 snímků/s * 10)

# Hlavní smyčka hry
running = True
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # Při stisknutí tlačítka myši vytvoř novou kouli
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullet_x = hero_x + hero_img.get_width() // 2
            bullet_y = hero_y + hero_img.get_height() // 2
            angle = math.atan2(mouse_y - bullet_y, mouse_x - bullet_x)
            bullet_speed = 7
            bullet_dx = bullet_speed * math.cos(angle)
            bullet_dy = bullet_speed * math.sin(angle)
            bullets.append((bullet_x, bullet_y, bullet_dx, bullet_dy))
            
   
        
    # Generování nepřátel
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_speed:
        enemy_spawn_timer = 0
        for _ in range(5):
            enemy_x, enemy_y, enemy_type = spawn_enemy()
            enemies.append((enemy_x, enemy_y, enemy_type))
    # Navýšení rychlosti spawnování po každém intervalu
    if enemy_spawn_timer % enemy_spawn_interval == 0:
        enemy_spawn_speed -= 5  # Snížení intervalu o 10 snímků

    # Ovládání hrdiny pomocí kláves WASD
    keys = pygame.key.get_pressed()
    if keys[K_w] and hero_y > 0:
        hero_y -= hero_speed
    if keys[K_s] and hero_y < height - hero_img.get_height():
        hero_y += hero_speed
    if keys[K_a] and hero_x > 0:
        hero_x -= hero_speed
    if keys[K_d] and hero_x < width - hero_img.get_width():
        hero_x += hero_speed

    # Kontrola kolizí koule s nepřáteli a pohyb koulí a nepřátel
    hero_hp = check_bullet_enemy_collision(hero_hp)

    # Automatická střelba každých 10 sekund po dosažení 500 XP
    if hero_xp >= 500:
        hero_shoot_timer += 1
        if hero_shoot_timer >= 600:
            hero_shoot_timer = 0
            # Automatizovaná střelba
            for angle in range(0, 360, 45):
                bullet_x = hero_x + hero_img.get_width() // 2
                bullet_y = hero_y + hero_img.get_height() // 2
                angle_rad = math.radians(angle)
                bullet_speed = 10
                bullet_dx = bullet_speed * math.cos(angle_rad)
                bullet_dy = bullet_speed * math.sin(angle_rad)
                bullets.append((bullet_x, bullet_y, bullet_dx, bullet_dy))

    # Vykreslení
    window.blit(background_img, (0, 0))
    for bullet in bullets:
        window.blit(bullet_img, (bullet[0] - bullet_img.get_width() // 2, bullet[1] - bullet_img.get_height() // 2))
    
    for enemy in enemies:
        enemy_x, enemy_y, enemy_type = enemy
        window.blit(enemy_type, (enemy_x, enemy_y))
    window.blit(hero_img, (hero_x, hero_y))
    # Vykreslení XP Baru
    xp_percentage = min(1, hero_xp / 500)  # Omezíme na maximální šířku XP baru
    xp_bar_width_current = xp_bar_width * xp_percentage
    xp_bar_rect = pygame.Rect(20, 20, xp_bar_width, xp_bar_height)
    xp_bar_current_rect = pygame.Rect(20, 20, xp_bar_width_current, xp_bar_height)
    pygame.draw.rect(window, xp_bar_background_color, xp_bar_rect)
    pygame.draw.rect(window, xp_bar_fill_color, xp_bar_current_rect)

    if hero_xp >= xp_per_level * hero_level:
        hero_level += 1
        hero_xp = 0
    
    # Vykreslení textu XP Baru
    font = pygame.font.Font(None, 30)
    xp_text = font.render("XP Bar", True, (255, 255, 255))
    window.blit(xp_text, (20, 50))
    
    
    # Vykreslení úrovně postavy
    level_text = font.render(f"Level: {hero_level}", True, (255, 255, 255))
    window.blit(level_text, (20, 80))

    # Vykreslení HP Baru
    hp_percentage = max(0, hero_hp / 100)  # Omezíme na minimální šířku HP baru
    hp_bar_width_current = hp_bar_width * hp_percentage
    hp_bar_rect = pygame.Rect(width - 20 - hp_bar_width, 20, hp_bar_width, hp_bar_height)
    hp_bar_current_rect = pygame.Rect(width - 20 - hp_bar_width, 20, hp_bar_width_current, hp_bar_height)
    pygame.draw.rect(window, hp_bar_background_color, hp_bar_rect)
    pygame.draw.rect(window, hp_bar_fill_color, hp_bar_current_rect)

    # Vykreslení textu HP Baru
    hp_text = font.render("HP Bar", True, (255, 255, 255))
    window.blit(hp_text, (width - 20 - hp_bar_width, 50))
    if hero_hp <= 0:
        wasted_img = pygame.image.load("images\wasted.jpg")
        wasted_img = pygame.transform.scale(wasted_img, (width, height))
        window.blit(wasted_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)  # Počkej 3 sekundy
        pygame.quit()
        sys.exit()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()


    


