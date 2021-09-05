import pygame
from sprite_sheet import get_frame, play_animation, load_sound_bool
from pickle import dump as p_dump
from pickle import load as p_load


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # assets
        self.player_run_png = pygame.image.load(
            'graphics/player/Run.png').convert_alpha()
        self.player_idle_png = pygame.image.load(
            'graphics/player/Idle.png').convert_alpha()
        self.player_jump_png = pygame.image.load(
            'graphics/player/Jump.png').convert_alpha()
        self.player_fall_png = pygame.image.load(
            'graphics/player/Fall.png').convert_alpha()
        self.player_hit_png = pygame.image.load(
            'graphics/player/Hit.png').convert_alpha()

        self.jump_sound = pygame.mixer.Sound('graphics/sound/jump_sound.wav')
        self.hit_sound = pygame.mixer.Sound('graphics/sound/hit_sound.wav')

        self.player_png = self.player_idle_png
        self.max_length = self.player_png.get_width()
        self.frame = 0
        self.direction = 1
        self.jump_speed = 0
        self.moving = False
        self.getting_hurt = False
        self.hurt_cooldown = False
        self.hurt_cooldown_timer = 0
        self.play_sound = load_sound_bool()
        self.game_started = p_load(open('data/data/game_state.bat', 'rb'))

        self.image = get_frame(self.player_run_png, int(
            self.frame), self.direction, 96, 96)
        self.rect = self.image.get_rect(bottomleft=(50, 450))
        self.collide_rect = pygame.rect.Rect(
            0, 0, 68, 80)

    def play_animation(self):

        speed = .2 if self.getting_hurt else .4

        self.image, self.frame = play_animation(
            self.player_png, self.frame, self.direction, 96, 96, speed)

        if self.frame == 0 and self.getting_hurt:
            self.getting_hurt = False

    def player_input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction = 1
            self.moving = True
            self.game_started = True
            self.player_png = self.player_run_png
        elif keys[pygame.K_a]:
            self.direction = -1
            self.moving = True
            self.game_started = True
            self.player_png = self.player_run_png
        else:
            self.moving = False
            self.player_png = self.player_idle_png

        # checks if player is on ground to jump
        if keys[pygame.K_SPACE] and self.rect.bottom == 450:
            self.jump_speed = 16
            if self.play_sound:
                self.jump_sound.play()

        if self.jump_speed > 0:  # if acceleration/ jumpspeed is + then we are going up else down
            self.player_png = self.player_jump_png
        elif self.jump_speed <= 0 and self.rect.bottom != 450:
            self.player_png = self.player_fall_png

        if self.getting_hurt:
            self.player_png = self.player_hit_png

        if pygame.time.get_ticks() - self.hurt_cooldown_timer >= 1000:
            self.hurt_cooldown = False

    def move_player(self):

        if self.moving:
            self.rect.x += 5 * self.direction
        elif self.rect.bottom == 450 and self.game_started:
            self.rect.x -= 2

        if self.rect.left < -30:
            self.rect.left = -30
        elif self.rect.right > 830:
            self.rect.right = 830

        self.jump_speed -= .6  # .6 is gravity
        self.rect.bottom -= self.jump_speed

        if self.rect.bottom > 450:  # if player is below the ground it moves it above.
            self.rect.bottom = 450

        self.collide_rect.center = self.rect.centerx, self.rect.centery + 8

    def get_hurt(self):

        self.getting_hurt = True
        self.frame = 0
        self.hurt_cooldown = True
        self.hurt_cooldown_timer = pygame.time.get_ticks()
        if self.play_sound:
            self.hit_sound.play()

    def save_game_state(self):

        p_dump(self.game_started, open('data/data/game_state.bat', 'wb'))

    def update(self):

        self.player_input()
        self.move_player()
        self.play_animation()
        self.save_game_state()
