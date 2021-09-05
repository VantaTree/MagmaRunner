import pygame
from sprite_sheet import get_frame, play_animation, load_sound_bool
from random import randint
from random import choice as rand_choice


class MrChomps(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.crawl_blink_png = pygame.image.load(
            'graphics/others/mr_chomps/Crawl_&_Blink.png').convert_alpha()
        self.crawl_chomp_png = pygame.image.load(
            'graphics/others/mr_chomps/Crawl_&_Chomp.png').convert_alpha()
        self.chomps_png = self.crawl_blink_png

        self.munch_sound = pygame.mixer.Sound('graphics/sound/croc_munch.wav')

        self.max_length = self.chomps_png.get_width()
        self.frame = 0
        self.attacking = False
        self.play_sound = load_sound_bool()

        x_pos = randint(830, 1050)

        self.image = get_frame(self.chomps_png, 0, 1, 96, 96)
        self.rect = self.image.get_rect(midbottom=(x_pos, 450))
        self.kill_rect = pygame.rect.Rect(0, 0, 40, 42)
        self.attack_rect = pygame.rect.Rect(0, 0, 50, 42)

    def play_animation(self):

        speed = .2 if self.attacking else .4

        self.image, self.frame = play_animation(
            self.chomps_png, self.frame, 1, 96, 96, speed)

        if self.attacking and self.frame == 0:
            self.attacking = False
            self.chomps_png = self.crawl_blink_png

    def move_chomps(self):

        if self.attacking:
            self.rect.x -= 3
        else:
            self.rect.x -= 4

        self.kill_rect.bottomleft = self.rect.bottomleft
        self.attack_rect.bottomleft = self.rect.left - 10, self.rect.bottom

    def kill_chomps(self):
        if self.rect.right < -30:
            self.kill()

    def attack_player(self):

        self.frame = 0
        self.attacking = True
        self.chomps_png = self.crawl_chomp_png
        if self.play_sound:
            self.munch_sound.play()

    def update(self):

        self.play_animation()
        self.move_chomps()
        self.kill_chomps()


class GizzlyBear(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.walk_png = pygame.image.load(
            'graphics/others/gizzly/Walking.png').convert_alpha()
        self.attack_png = pygame.image.load(
            'graphics/others/gizzly/Attack.png').convert_alpha()
        self.gizzly_png = self.walk_png

        self.attack_sound = pygame.mixer.Sound(
            'graphics/sound/bear_attack.wav')

        self.max_length = self.gizzly_png.get_width()
        self.frame = 0
        self.attacking = False
        self.play_sound = load_sound_bool()

        x_pos = randint(830, 1050)

        self.image = get_frame(self.gizzly_png, 0, 1, 144, 96)
        self.rect = self.image.get_rect(midbottom=(x_pos, 450))
        self.kill_rect = pygame.rect.Rect(0, 0, 68, 84)
        self.attack_rect = pygame.rect.Rect(0, 0, 78, 84)

    def play_animation(self):

        self.image, self.frame = play_animation(
            self.gizzly_png, self.frame, 1, 144, 96, .2)

        if self.attacking and self.frame == 0:
            self.attacking = False
            self.gizzly_png = self.walk_png
            self.rect.x -= 10

    def move_gizzly(self):

        if self.attacking:
            self.rect.x -= 2
        else:
            self.rect.x -= 3

        self.kill_rect.topleft = self.rect.topleft
        self.attack_rect.topleft = self.rect.left - 10, self.rect.top

    def kill_gizzly(self):
        if self.rect.right < -30:
            self.kill()

    def attack_player(self):

        self.frame = 0
        self.attacking = True
        self.gizzly_png = self.attack_png
        if self.play_sound:
            self.attack_sound.play()

    def update(self):

        self.play_animation()
        self.move_gizzly()
        self.kill_gizzly()


class Orc(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.walk_blink_png = pygame.image.load(
            'graphics/others/orc/Walking_&_Blink.png').convert_alpha()
        self.spear_png = pygame.image.load(
            'graphics/others/orc/Spear.png').convert_alpha()
        self.orc_png = self.walk_blink_png

        self.spear_attack = pygame.mixer.Sound(
            'graphics/sound/sword_attack.wav')

        self.max_length = self.orc_png.get_width()
        self.frame = 0
        self.attacking = False
        self.play_sound = load_sound_bool()

        x_pos = randint(830, 1050)

        self.image = get_frame(self.orc_png, 0, 1, 192, 96)
        self.rect = self.image.get_rect(midbottom=(x_pos, 450))
        self.kill_rect = pygame.rect.Rect(0, 0, 88, 32)
        self.attack_rect = pygame.rect.Rect(0, 0, 98, 96)

    def play_animation(self):

        self.image, self.frame = play_animation(
            self.orc_png, self.frame, 1, 192, 96, .2)

        if self.frame == 0 and self.attacking:
            self.attacking = False
            self.orc_png = self.walk_blink_png
            self.rect.x -= 10

    def move_orc(self):

        if self.attacking:
            self.rect.x -= 2
        else:
            self.rect.x -= 3

        self.kill_rect.bottomleft = self.rect.bottomleft
        self.attack_rect.topleft = self.rect.left - 10, self.rect.top

    def kill_orc(self):
        if self.rect.right < -30:
            self.kill()

    def attack_player(self):

        self.frame = 0
        self.attacking = True
        self.orc_png = self.spear_png
        if self.play_sound:
            self.spear_attack.play()

    def update(self):

        self.play_animation()
        self.move_orc()
        self.kill_orc()


class Mushroom(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.walk = pygame.image.load(
            'graphics/others/mushroom/Walk.png').convert_alpha()
        self.mushroom_png = self.walk

        self.max_length = self.mushroom_png.get_width()
        self.frame = 0

        x_pos = randint(830, 1050)

        self.image = get_frame(self.mushroom_png, 0, 1, 72, 72)
        self.rect = self.image.get_rect(midbottom=(x_pos, 450))

    def play_animation(self):

        self.image, self.frame = play_animation(
            self.mushroom_png, self.frame, 1, 72, 72, .2)

    def move_mushroom(self):

        self.rect.x -= 4

    def kill_mushroom(self):
        if self.rect.right < -30:
            self.kill()

    def update(self):

        self.play_animation()
        self.move_mushroom()
        self.kill_mushroom()


class BigRed(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.walk_png = pygame.image.load(
            'graphics/others/big_red/Running.png').convert_alpha()
        self.punch_png = pygame.image.load(
            'graphics/others/big_red/Punching.png').convert_alpha()
        self.big_red_png = self.walk_png

        self.punch_sound = pygame.mixer.Sound('graphics/sound/punch_sound.wav')

        self.max_length = self.big_red_png.get_width()
        self.frame = 0
        self.attacking = False
        self.play_sound = load_sound_bool()

        x_pos = randint(830, 1050)

        self.image = get_frame(self.big_red_png, 0, -1, 96, 96)
        self.rect = self.image.get_rect(midbottom=(x_pos, 450))
        self.kill_rect = pygame.rect.Rect(0, 0, 48, 54)
        self.attack_rect = pygame.rect.Rect(0, 0, 58, 54)

    def play_animation(self):

        width = 144 if self.attacking else 96

        self.image, self.frame = play_animation(
            self.big_red_png, self.frame, -1, width, 96, .2)

        if self.frame == 0 and self.attacking:
            self.attacking = False
            self.big_red_png = self.walk_png
            self.rect.x += 30
            self.rect.x -= 10

    def move_big_red(self):

        if self.attacking:
            self.rect.x -= 2
        else:
            self.rect.x -= 4

        self.kill_rect.bottomleft = self.rect.bottomleft
        self.attack_rect.bottomleft = self.rect.left - 10, self.rect.bottom

    def kill_big_red(self):
        if self.rect.right < -30:
            self.kill()

    def attack_player(self):

        self.attacking = True
        self.frame = 0
        self.big_red_png = self.punch_png
        self.rect.x -= 30
        if self.play_sound:
            self.punch_sound.play()

    def update(self):

        self.play_animation()
        self.move_big_red()
        self.kill_big_red()


class Snail(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.walk_png = pygame.image.load(
            'graphics/others/snail/Walk.png').convert_alpha()
        self.attack_png = pygame.image.load(
            'graphics/others/snail/Attack.png').convert_alpha()
        self.snail_png = self.walk_png

        self.gasp_sound = pygame.mixer.Sound('graphics/sound/snail_gasp.wav')
        self.suck_sound = pygame.mixer.Sound('graphics/sound/snail_suck.wav')

        self.max_length = self.snail_png.get_width()
        self.frame = 0
        self.attacking = False
        self.play_sound = load_sound_bool()

        x_pos = randint(830, 1050)

        self.image = get_frame(self.snail_png, 0, 1, 72, 72)
        self.rect = self.image.get_rect(midbottom=(x_pos, 450))
        self.kill_rect = pygame.rect.Rect(0, 0, 36, 36)
        self.attack_rect = pygame.rect.Rect(0, 0, 46, 36)

    def play_animation(self):

        speed = .15 if self.attacking else .08

        self.image, self.frame = play_animation(
            self.snail_png, self.frame, 1, 72, 72, speed)

        if self.frame == 0 and self.attacking:
            self.attacking = False
            self.snail_png = self.walk_png
            self.rect.x -= 10

    def move_snail(self):

        if self.attacking:
            self.rect.x -= 2
        else:
            self.rect.x -= 3

        self.kill_rect.bottomleft = self.rect.bottomleft
        self.attack_rect.bottomleft = self.rect.left - 10, self.rect.bottom

    def kill_snail(self):
        if self.rect.right < -30:
            self.kill()

    def attack_player(self):
        self.frame = 0
        self.attacking = True
        self.snail_png = self.attack_png
        if self.play_sound:
            if randint(0, 1):
                self.gasp_sound.play()
            else:
                self.suck_sound.play()

    def update(self):

        self.play_animation()
        self.move_snail()
        self.kill_snail()


class MutantPlant(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.idle_png = pygame.image.load(
            'graphics/others/mutant_plant/Idle.png').convert_alpha()
        self.attack_png = pygame.image.load(
            'graphics/others/mutant_plant/Attack.png').convert_alpha()
        self.plant_png = self.idle_png

        self.chomp_sound = pygame.mixer.Sound('graphics/sound/chomp_sound.wav')

        self.max_length = self.plant_png.get_width()
        self.frame = 0
        self.attacking = False
        self.play_sound = load_sound_bool()

        x_pos = randint(830, 1050)

        self.image = get_frame(self.plant_png, 0, 1, 138, 96)
        self.rect = self.image.get_rect(midbottom=(x_pos, 450))
        self.kill_rect = pygame.rect.Rect(0, 0, 45, 75)
        self.attack_rect = pygame.rect.Rect(0, 0, 55, 75)

    def play_animation(self):

        speed = .1 if self.attacking else .04

        self.image, self.frame = play_animation(
            self.plant_png, self.frame, 1, 138, 96, speed)

        if self.frame == 0 and self.attacking:
            self.attacking = False
            self.plant_png = self.idle_png

    def move_plant(self):

        self.rect.x -= 2

        self.kill_rect.bottomleft = self.rect.left + 36, self.rect.bottom
        self.attack_rect.bottomleft = self.rect.left + 26, self.rect.bottom

    def kill_plant(self):
        if self.rect.right < -30:
            self.kill()

    def attack_player(self):

        self.frame = 0
        self.attacking = True
        self.plant_png = self.attack_png
        if self.play_sound:
            self.chomp_sound.play()

    def update(self):

        self.play_animation()
        self.move_plant()
        self.kill_plant()


class MoeScotty(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.fly_png = pygame.image.load(
            'graphics/others/moe_scotty/Flying.png').convert_alpha()
        self.sting_png = pygame.image.load(
            'graphics/others/moe_scotty/Sting.png').convert_alpha()
        self.scotty_png = self.fly_png

        self.sting_sound = pygame.mixer.Sound(
            'graphics/sound/insect_sting.wav')

        self.max_length = self.scotty_png.get_width()
        self.frame = 0
        self.attacking = False
        self.play_sound = load_sound_bool()

        self.phase = 'entry'

        self.random_movt = pygame.math.Vector2(0, 0)
        self.entry_time = pygame.time.get_ticks()

        self.image = get_frame(self.scotty_png, 0, 1, 96, 96)
        self.rect = self.image.get_rect(midbottom=(400, -50))
        self.kill_rect = pygame.rect.Rect(0, 0, 96, 40)
        self.attack_rect = pygame.rect.Rect(0, 0, 106, 50)

    def play_animation(self):

        self.image, self.frame = play_animation(
            self.scotty_png, self.frame, 1, 96, 96, .3)

        if self.frame == 0 and self.attacking:
            self.attacking = False
            self.scotty_png = self.fly_png

    def move_scotty(self):

        if self.phase == 'entry':
            self.rect.y += 3
        elif self.phase == 'exit':
            self.rect.x -= 5
        elif self.phase == 'roaming':
            self.rect.x += self.random_movt.x
            self.rect.y += self.random_movt.y

            if self.rect.top < 0:
                self.rect.top = 0
                self.random_movt.y = 1
            if self.rect.bottom > 420:
                self.rect.bottom = 420
                self.random_movt.y = -1
            if self.rect.right > 800:
                self.rect.right = 800
                self.random_movt.x = -1
            if self.rect.left < 0:
                self.rect.left = 0
                self.random_movt.x = 1

        self.kill_rect.midbottom = self.rect.midbottom
        self.attack_rect.midbottom = self.rect.centerx, self.rect.bottom + 10

    def set_random_movt(self):

        random_bool_x = rand_choice([True, False])
        random_bool_y = rand_choice([True, False])

        if random_bool_x and self.random_movt.x < 6:
            self.random_movt.x += 2
        elif self.random_movt.x > -6:
            self.random_movt.x -= 2

        if random_bool_y and self.random_movt.y < 6:
            self.random_movt.y += 2
        elif self.random_movt.y > -6:
            self.random_movt.y -= 2

    def stop_movt(self):

        if rand_choice([True, False]):
            self.random_movt.x = 0

    def update_phase(self):

        if self.rect.y > 250:
            self.phase = 'roaming'

        if pygame.time.get_ticks() - self.entry_time > 30_000:
            self.phase = 'exit'

    def kill_scotty(self):
        if self.rect.right < -30:
            self.kill()

    def attack_player(self):

        self.frame = 0
        self.attacking = True
        self.scotty_png = self.sting_png
        if self.play_sound:
            self.sting_sound.play()

    def update(self):

        self.play_animation()
        self.move_scotty()
        self.kill_scotty()
        self.update_phase()


class BossGolem(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.idle = pygame.image.load(
            'graphics/others/golem/Enemy_Golem.png').convert_alpha()
        self.golem_png = self.idle

        self.max_length = self.golem_png.get_width()
        self.frame = 0

        x_pos = randint(830, 1050)

        self.image = get_frame(self.golem_png, 0, 1, 144, 144)
        self.rect = self.image.get_rect(midbottom=(x_pos, 450))

    def play_animation(self):

        self.image, self.frame = play_animation(
            self.golem_png, self.frame, 1, 144, 144, .1)

    def move_golem(self):

        self.rect.x -= 3

    def kill_golem(self):
        if self.rect.right < -30:
            self.kill()

    def update(self):

        self.play_animation()
        self.move_golem()
        self.kill_golem()
