import random
import math
from pygame import Rect
from pgzero.builtins import Actor, keyboard, mouse
import pgzrun

WIDTH = 800
HEIGHT = 480

game_state = "menu"
music_on = True
sounds_on = True

start_button = Rect((WIDTH//2 - 100, 150), (200, 50))
sound_button = Rect((WIDTH//2 - 100, 220), (200, 50))
exit_button = Rect((WIDTH//2 - 100, 290), (200, 50))

player = None
enemies = []
platforms = []
coins = []
score = 0
max_score = 3

def play_sound(name):
    if sounds_on:
        sound = getattr(sounds, name, None)
        if sound:
            sound.play()

class Player:
    def __init__(self, x, y):
        self.actor = Actor("adventurer_hold1", (x, y))
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.gravity = 0.5
        self.anim_index = 0
        self.anim_timer = 0
        self.facing = "right"
        self.is_attacking = False
        self.attack_timer = 0

    def update(self):
        keys = keyboard
        self.vx = 0
        is_moving = False

        if keys.left:
            self.vx = -3
            is_moving = True
            self.facing = "left"
        elif keys.right:
            self.vx = 3
            is_moving = True
            self.facing = "right"

        if keys.space and self.on_ground:
            self.vy = -10
            play_sound("jump")

        if keys.x and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = 12
            play_sound("attack")

        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False

        self.vy += self.gravity
        self.actor.x += self.vx
        self.actor.y += self.vy

        if self.actor.left < 0:
            self.actor.left = 0
        if self.actor.right > WIDTH:
            self.actor.right = WIDTH
        if self.actor.top < 0:
            self.actor.top = 0
        if self.actor.bottom > HEIGHT:
            self.actor.bottom = HEIGHT
            self.vy = 0
            self.on_ground = True

        self.check_platforms()

        self.anim_timer += 1
        if self.anim_timer > 10:
            self.anim_index = (self.anim_index + 1) % 2
            self.anim_timer = 0

        if self.is_attacking:
            if self.facing == "left":
                self.actor.image = "adventurer_attack_left"
            else:
                self.actor.image = "adventurer_attack"
        elif not self.on_ground:
            if self.facing == "left":
                self.actor.image = "player_jump_left"
            else:
                self.actor.image = "player_jump"
        elif is_moving:
            if self.facing == "left":
                self.actor.image = f"adventurer_walk_left{self.anim_index + 1}"
            else:
                self.actor.image = f"adventurer_walk{self.anim_index + 1}"
        else:
            self.actor.image = f"adventurer_hold{self.anim_index + 1}"

        self.actor.flip_x = True if self.facing == "left" else False

    def draw(self):
        self.actor.draw()

    def check_platforms(self):
        self.on_ground = False
        for plat in platforms:
            if self.actor.colliderect(plat) and self.vy >= 0:
                self.actor.bottom = plat.top
                self.vy = 0
                self.on_ground = True

class Enemy:
    def __init__(self, x, y, left_limit, right_limit):
        self.actor = Actor("enemy_idle1", (x, y))
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.direction = 1
        self.speed = 2
        self.anim_index = 0
        self.anim_timer = 0

    def update(self):
        self.actor.x += self.speed * self.direction
        if self.actor.x < self.left_limit or self.actor.x > self.right_limit:
            self.direction *= -1

        self.anim_timer += 1
        if self.anim_timer > 12:
            self.anim_index = (self.anim_index + 1) % 4
            self.actor.image = f"enemy_idle{self.anim_index + 1}"
            self.anim_timer = 0

        enemy_box = Rect(
            self.actor.left + 5, 
            self.actor.top + 10, 
            self.actor.width - 10, 
            self.actor.height - 15
        )

        player_box = Rect(
            player.actor.left + 5, 
            player.actor.top + 10, 
            player.actor.width - 10, 
            player.actor.height - 15
        )

        if enemy_box.colliderect(player_box):
            if player.is_attacking:
                enemies.remove(self)
                play_sound("enemy_hit")
            else:
                game_over()

    def draw(self):
        self.actor.draw()

class Coin:
    def __init__(self, x, y):
        self.actor = Actor("coin", (x, y))
        self.collected = False
        self.anim_index = 0
        self.anim_timer = 0

    def update(self):
        if self.collected:
            return

        self.anim_timer += 1
        if self.anim_timer > 8:
            self.anim_index = (self.anim_index + 1) % 4
            self.actor.image = f"coin{self.anim_index + 1}"
            self.anim_timer = 0

        if self.actor.colliderect(player.actor):
            self.collected = True
            play_sound("coin")
            global score
            score += 1

    def draw(self):
        if not self.collected:
            self.actor.draw()

def game_over():
    global game_state
    game_state = "gameover"
    music.stop()

def draw_menu():
    screen.clear()
    screen.draw.text("Platformer", center=(WIDTH//2, 80), fontsize=60, color="white")
    screen.draw.filled_rect(start_button, "dodgerblue")
    screen.draw.text("Start Game", center=start_button.center, color="white")
    screen.draw.filled_rect(sound_button, "green")
    screen.draw.text("Toggle Sound", center=sound_button.center, color="white")
    screen.draw.filled_rect(exit_button, "red")
    screen.draw.text("Exit", center=exit_button.center, color="white")
    screen.draw.text("Press H for How to Play", center=(WIDTH//2, 360), fontsize=30, color="yellow")

def draw_how_to_play():
    screen.clear()
    screen.draw.text("How to Play", center=(WIDTH//2, 60), fontsize=60, color="white")
    lines = [
        "LEFT / RIGHT: Move",
        "SPACE: Jump",
        "X: Attack (when near an enemy)",
        "Collect 3 coins to win!",
        "Avoid touching enemies unless attacking.",
        "",
        "Click anywhere to return."
    ]
    for i, line in enumerate(lines):
        screen.draw.text(line, center=(WIDTH//2, 130 + i * 40), fontsize=30, color="yellow")

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "how_to_play":
        draw_how_to_play()
    elif game_state == "playing":
        screen.fill((30, 30, 30))
        player.draw()
        for plat in platforms:
            screen.draw.filled_rect(plat, "gray")
        for coin in coins:
            coin.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=30, color="white")
    elif game_state == "win":
        screen.fill("darkgreen")
        screen.draw.text("You Win!", center=(WIDTH//2, HEIGHT//2 - 40), fontsize=60, color="white")
        screen.draw.text("Click to return to menu", center=(WIDTH//2, HEIGHT//2 + 20), fontsize=30, color="white")
    elif game_state == "gameover":
        screen.fill("darkred")
        screen.draw.text("Game Over!", center=(WIDTH//2, HEIGHT//2 - 40), fontsize=60, color="white")
        screen.draw.text("Click to return to menu", center=(WIDTH//2, HEIGHT//2 + 20), fontsize=30, color="white")

def update():
    if game_state == "playing":
        player.update()
        for enemy in enemies:
            enemy.update()
        global score
        for coin in coins:
            coin.update()
        if all(coin.collected for coin in coins):
            game_win()

def on_mouse_down(pos):
    global game_state, music_on, sounds_on
    if game_state == "menu":
        if start_button.collidepoint(pos):
            start_game()
        elif sound_button.collidepoint(pos):
            sounds_on = not sounds_on
        elif exit_button.collidepoint(pos):
            exit()
    elif game_state == "how_to_play":
        game_state = "menu"
    elif game_state == "win":
        game_state = "menu"
    elif game_state == "gameover":
        game_state = "menu"

def on_key_down(key):
    global game_state
    if game_state == "menu" and key == keys.H:
        game_state = "how_to_play"

def game_win():
    global game_state
    game_state = "win"
    music.stop()
    play_sound("win")

def start_game():
    global player, enemies, platforms, coins, score, game_state
    game_state = "playing"
    player = Player(100, 300)
    score = 0
    platforms.clear()
    platforms.append(Rect((0, 440), (WIDTH, 40)))
    enemies.clear()
    coins.clear()
    y_levels = [350, 280, 210, 140, 70]
    zigzag_direction = 1
    for i, y in enumerate(y_levels):
        w = random.randint(100, 150)
        margin = 50
        max_x = WIDTH - w - margin
        if zigzag_direction == 1:
            x = random.randint(margin, int(max_x * 0.6))
        else:
            x = random.randint(int(max_x * 0.4), max_x)
        platform = Rect((x, y), (w, 20))
        platforms.append(platform)
        zigzag_direction *= -1
        if i != 0 and random.random() < 0.5:
            ex = random.randint(platform.left + 20, platform.right - 20)
            enemies.append(Enemy(ex, platform.top - 20, platform.left, platform.right))
        if random.random() < 0.7:
            cx = random.randint(platform.left + 10, platform.right - 10)
            coins.append(Coin(cx, platform.top - 20))
    if music_on:
        play_sound("bgm")

pgzrun.go()