import pygame
from sprite_sheet import get_frame, play_animation, load_sound_bool
from pickle import load as p_load
from random import randint


class WispyFire(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.idle_flicker_png = pygame.image.load(
            'graphics/others/wispy_fire/Idle_flicker.png').convert_alpha()
        self.death_png = pygame.image.load(
            'graphics/others/wispy_fire/Death.png').convert_alpha()
        self.wispy_png = self.idle_flicker_png

        self.flame_die = pygame.mixer.Sound('graphics/sound/flame_dying.wav')

        self.game_started = p_load(open('data/data/game_state.bat', 'rb'))
        self.max_length = self.wispy_png.get_width()
        self.frame = 0
        self.alive = True
        self.play_sound = load_sound_bool()

        self.speed = randint(2, 6)
        x_pos = randint(830, 1050)
        y_pos = randint(150, 400)

        self.image = get_frame(self.wispy_png, 0, 1, 32, 32)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def play_animation(self):

        self.image, self.frame = play_animation(
            self.wispy_png, self.frame, 1, 32, 32, .2)

    def move_wispy(self):

        if self.game_started:
            if self.alive:
                self.rect.x -= self.speed
            else:
                self.rect.x -= self.speed // 2

    def kill_wispy(self):

        if self.rect.right < -30:
            self.kill()
        if not self.alive and self.frame == 0:
            self.kill()

    def death_role(self):

        self.wispy_png = self.death_png
        self.alive = False
        self.frame = 0
        if self.play_sound:
            self.flame_die.play()

    def load_game_state(self):

        self.game_started = p_load(open('data/data/game_state.bat', 'rb'))

    def update(self):

        self.play_animation()
        self.move_wispy()
        self.kill_wispy()
        self.load_game_state()
