import pygame
import sprites.player_sprite as player_sprite
import sprites.wispy_sprite as wispy_sprite
from sprites.enemy_sprite import *
from sprites.fire_bar import FireBar
from pickle import dump as p_dump
from pickle import load as p_load
from random import choice as rand_choice


class Main:

    def __init__(self):

        self.quit_up = pygame.image.load(
            'graphics/buttons/Close_Unpressed.png').convert_alpha()
        self.quit_down = pygame.image.load(
            'graphics/buttons/Close_Pressed.png').convert_alpha()
        self.back_up = pygame.image.load(
            'graphics/buttons/Back_Unpressed.png').convert_alpha()
        self.back_down = pygame.image.load(
            'graphics/buttons/Back_Pressed.png').convert_alpha()
        self.restart_up = pygame.image.load(
            'graphics/buttons/Restart_Unpressed.png').convert_alpha()
        self.restart_down = pygame.image.load(
            'graphics/buttons/Restart_Pressed.png').convert_alpha()

        self.quit_rect = self.quit_up.get_rect(topright=(790, 10))
        self.restart_rect = self.quit_up.get_rect(midbottom=(400, -200))
        self.back_rect = self.quit_up.get_rect(topright=(740, 10))

        self.hover_quit_button = False
        self.hover_back_button = False
        self.hover_restart_button = False

        self.floor_pos = 0
        self.game_started = False
        p_dump(self.game_started, open('data/data/game_state.bat', 'wb'))
        self.high_score = p_load(open('data/data/high_score.bat', 'rb'))
        self.fire_bar = FireBar()
        self.score = 0
        self.lives = 5
        self.game_over = False

    def button_logic(self, mouse_pos, click=False):

        for index, button_rect in enumerate([self.quit_rect, self.restart_rect, self.back_rect]):
            if button_rect.collidepoint(mouse_pos):
                if click:
                    if index == 0:
                        pygame.quit()
                        raise SystemExit
                    elif index == 1 and self.game_over:
                        self.restart_game()
                        if play_sound:
                            click_sound.play()
                    elif index == 2:
                        self.restart_game()
                        main_menu.playing = False
                        if play_sound:
                            click_sound.play()
                        break
                else:
                    if index == 0:
                        self.hover_quit_button = True
                    elif index == 1:
                        self.hover_restart_button = True
                    elif index == 2:
                        self.hover_back_button = True

            else:
                if index == 0:
                    self.hover_quit_button = False
                elif index == 1:
                    self.hover_restart_button = False
                elif index == 2:
                    self.hover_back_button = False

    def animate_button(self):

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.button_logic(mouse_pos)
        else:
            self.hover_quit_button = False
            self.hover_back_button = False
            self.restart_back_button = False

    def restart_game(self):

        self.__init__()
        player.add(player_sprite.Player())
        fire_group.empty()
        fly_group.empty()
        enemy_group.empty()
        enemy_no_attack_group.empty()
        self.restart_rect.bottom = -200

    def update_high_score(self):

        if self.score > self.high_score:
            self.high_score = self.score
            p_dump(self.high_score, open('data/data/high_score.bat', 'wb'))

    def move_restart_button(self):

        if self.restart_rect.bottom >= 453:
            self.restart_rect.bottom = 453
        else:
            self.restart_rect.bottom += 8
        if self.restart_rect.bottom == 453 and self.restart_rect.left > -5:
            self.restart_rect.x -= 2
        if play_sound and self.restart_rect.bottom == 448:
            drop_sound.play()

    def move_floor(self):

        if self.game_started:
            self.floor_pos -= 2
            if self.floor_pos <= -800:
                self.floor_pos = 0

    def draw(self):

        screen.blit(background, (0, 0))
        screen.blit(floor, (self.floor_pos, 450))
        screen.blit(floor, (self.floor_pos+800, 450))

        lives = fire_font.render(f'X{self.lives}', False, (255, 90, 0))
        lives_rect = lives.get_rect(midleft=(255, 33))

        screen.blit(fire_heart_png, (210, 15))
        screen.blit(lives, lives_rect)

        score_text = score_font.render(
            f'Score: {self.score} HighScore: {self.high_score}', False, (200, 90, 0))
        score_rect = score_text.get_rect(topleft=(330, 20))
        screen.blit(score_text, score_rect)

        if self.hover_quit_button:
            screen.blit(self.quit_down, self.quit_rect)
        else:
            screen.blit(self.quit_up, self.quit_rect)

        if self.hover_back_button:
            screen.blit(self.back_down, self.back_rect)
        else:
            screen.blit(self.back_up, self.back_rect)

        if self.lives <= 1:
            screen.blit(fiery_heart_png, (204, -23))

        if self.game_over:

            score_text = fire_font.render(
                f'SCORE: {self.score}', False, (100, 90, 200))
            score_rect = score_text.get_rect(center=(400, 330))

            screen.blit(game_over_text, game_over_rect)
            screen.blit(score_text, score_rect)

            if self.hover_restart_button:
                screen.blit(self.restart_down, self.restart_rect)
            else:
                screen.blit(self.restart_up, self.restart_rect)

    def load_game_state(self):

        if not self.game_started:
            self.game_started = p_load(open('data/data/game_state.bat', 'rb'))

    def spawn_wispy(self):
        fire_group.add(wispy_sprite.WispyFire())

    def spawn_fly(self):

        fly_group.add(MoeScotty())

    def spawn_enemy(self):

        enemy = rand_choice(enemy_list)

        if enemy == 'Mr Chomps':
            enemy_group.add(MrChomps())
        elif enemy == 'Gizzly Bear':
            enemy_group.add(GizzlyBear())
        elif enemy == 'Orc':
            enemy_group.add(Orc())
        elif enemy == 'Mushroom':
            enemy_no_attack_group.add(Mushroom())
        elif enemy == 'Big Red':
            enemy_group.add(BigRed())
        elif enemy == 'Snail':
            enemy_group.add(Snail())
        elif enemy == 'Mutant Plant':
            enemy_group.add(MutantPlant())

    def change_scotty_movt(self):

        for fly in fly_group.sprites():
            fly.set_random_movt()

    def stop_scotty_movt(self):

        for fly in fly_group.sprites():
            fly.stop_movt()

    def collect_fire_check(self, player_object):

        wispy_sprite_list = fire_group.sprites()

        for wisp_fire in wispy_sprite_list:

            if wisp_fire and wisp_fire.alive and player_object.collide_rect.colliderect(wisp_fire.rect):
                self.fire_bar.collect_heat()
                wisp_fire.death_role()

    def enemy_attack_check(self, player_object):

        enemy_objects = enemy_group.sprites() + fly_group.sprites() + \
            enemy_no_attack_group.sprites()

        if enemy_objects and not player_object.hurt_cooldown:
            for enemy in enemy_objects:
                if 'Mushroom' in str(enemy):
                    if player_object.collide_rect.colliderect(enemy.rect):
                        self.player_hurt()
                        break
                else:
                    if player_object.collide_rect.colliderect(enemy.kill_rect):
                        self.player_hurt()
                    if not enemy.attacking and player_object.collide_rect.colliderect(enemy.attack_rect):
                        enemy.attack_player()
                        break

    def add_life(self):

        if self.fire_bar.add_a_life:
            self.lives += 1
            self.fire_bar.add_a_life = False
            if play_sound:
                life_sound.play()

    def player_hurt(self):

        self.lives -= 1
        player.sprite.get_hurt()

    def check_game_over(self):

        if self.lives == 0 and not self.game_over:
            self.game_over = True
            player.sprite.kill()

    def run(self):

        self.draw()
        self.fire_bar.run(screen)
        fire_group.draw(screen)
        enemy_no_attack_group.draw(screen)
        enemy_group.draw(screen)
        fly_group.draw(screen)
        player.draw(screen)

        self.move_floor()
        self.load_game_state()
        self.add_life()
        self.check_game_over()
        self.animate_button()

        player.update()
        fire_group.update()
        enemy_no_attack_group.update()
        fly_group.update()
        enemy_group.update()

        if self.game_over:
            self.move_restart_button()
            self.update_high_score()

        if not self.game_over and self.game_started:

            player_object = player.sprite

            self.collect_fire_check(player_object)
            self.enemy_attack_check(player_object)


class MainMenu:

    def __init__(self):

        # buttons
        self.play_up = pygame.image.load(
            'graphics/buttons/Play_Unpressed.png').convert_alpha()
        self.play_down = pygame.image.load(
            'graphics/buttons/Play_Pressed.png').convert_alpha()
        self.quit_up = pygame.image.load(
            'graphics/buttons/Cross_Unpressed.png').convert_alpha()
        self.quit_down = pygame.image.load(
            'graphics/buttons/Cross_Pressed.png').convert_alpha()
        self.back_up = pygame.image.load(
            'graphics/buttons/Back_Unpressed.png').convert_alpha()
        self.back_down = pygame.image.load(
            'graphics/buttons/Back_Pressed.png').convert_alpha()
        self.start_up = pygame.image.load(
            'graphics/buttons/Start_Unpressed.png').convert_alpha()
        self.start_down = pygame.image.load(
            'graphics/buttons/Start_Pressed.png').convert_alpha()
        self.sound_on_up = pygame.image.load(
            'graphics/buttons/Vol_on_Unpressed.png').convert_alpha()
        self.sound_on_down = pygame.image.load(
            'graphics/buttons/Vol_on_Pressed.png').convert_alpha()
        self.sound_off_up = pygame.image.load(
            'graphics/buttons/Vol_off_Unpressed.png').convert_alpha()
        self.sound_off_down = pygame.image.load(
            'graphics/buttons/Vol_off_Pressed.png').convert_alpha()
        self.scroll_text_png = pygame.image.load(
            'graphics/terrain/scroll_text.png').convert_alpha()
        self.scroll_top = pygame.image.load(
            'graphics/terrain/scroll_top.png').convert_alpha()
        self.scroll_middle = pygame.image.load(
            'graphics/terrain/scroll_middle.png').convert_alpha()
        self.scroll_bottom = pygame.image.load(
            'graphics/terrain/scroll_bottom.png').convert_alpha()
        self.scroll_top = pygame.transform.scale(
            self.scroll_top, (47*15, 26*15))
        self.scroll_middle = pygame.transform.scale(
            self.scroll_middle, (47*15, 13*15))
        self.scroll_bottom = pygame.transform.scale(
            self.scroll_bottom, (47*15, 19*15))

        # button rects
        self.play_rect = self.play_up.get_rect(center=(400, 300))
        self.quit_rect = self.quit_up.get_rect(center=(400, 450))
        self.back_rect = self.back_up.get_rect(topright=(800, 610))
        self.start_rect = self.start_up.get_rect(center=(400, 1940))
        self.sound_rect = self.sound_on_up.get_rect(center=(400, 550))

        # variables

        self.save_sound_bool()
        self.playing = False
        self.on_main_menu = True
        self.hover_play_button = False
        self.hover_quit_button = False
        self.hover_back_button = False
        self.hover_start_button = False
        self.hover_sound_button = False
        self.slide = 0

    def draw(self):

        screen.blit(main_background, (0, 0))
        if self.hover_play_button:
            screen.blit(
                self.play_down, (self.play_rect.left, self.play_rect.top+self.slide))
        else:
            screen.blit(
                self.play_up, (self.play_rect.left, self.play_rect.top+self.slide))
        if self.hover_quit_button:
            screen.blit(
                self.quit_down, (self.quit_rect.left, self.quit_rect.top+self.slide))
        else:
            screen.blit(
                self.quit_up, (self.quit_rect.left, self.quit_rect.top+self.slide))
        if self.hover_sound_button:
            screen.blit(
                self.sound_down, (self.sound_rect.left, self.sound_rect.top+self.slide))
        else:
            screen.blit(
                self.sound_up, (self.sound_rect.left, self.sound_rect.top+self.slide))

        if self.hover_back_button:
            screen.blit(self.back_down, self.back_rect)
        else:
            screen.blit(self.back_up, self.back_rect)
        if self.hover_start_button:
            screen.blit(self.start_down, self.start_rect)
        else:
            screen.blit(self.start_up, self.start_rect)

        screen.blit(self.scroll_top, (47, 650+self.slide))
        screen.blit(self.scroll_middle, (47, 1040+self.slide))
        screen.blit(self.scroll_middle, (47, 1235+self.slide))
        screen.blit(self.scroll_bottom, (47, 1325+self.slide))
        screen.blit(self.scroll_text_png, (0, 600+self.slide))

    def button_logic(self, mouse_pos, click=False):

        for index, button in enumerate([self.play_rect, self.quit_rect, self.sound_rect, self.back_rect, self.start_rect]):
            if button.collidepoint(mouse_pos):
                if self.on_main_menu and self.slide == 0:
                    if click:
                        if index == 0:
                            self.on_main_menu = False
                            if play_sound:
                                click_sound.play()
                        elif index == 1:
                            pygame.quit()
                            raise SystemExit
                        elif index == 2:
                            self.toggle_sound()
                            click_sound.play()
                    else:
                        if index == 0:
                            self.hover_play_button = True
                        elif index == 1:
                            self.hover_quit_button = True
                        elif index == 2:
                            self.hover_sound_button = True
                elif not self.on_main_menu and self.slide <= -600:
                    if click:
                        if index == 3:
                            self.on_main_menu = True
                            if play_sound:
                                click_sound.play()
                        elif index == 4:
                            self.on_main_menu = True
                            self.slide = 0
                            self.playing = True
                            if play_sound:
                                click_sound.play()
                            break
                    else:
                        if index == 3:
                            self.hover_back_button = True
                        if index == 4:
                            self.hover_start_button = True

            else:
                if index == 0:
                    self.hover_play_button = False
                elif index == 1:
                    self.hover_quit_button = False
                elif index == 2:
                    self.hover_sound_button = False
                elif index == 3:
                    self.hover_back_button = False
                elif index == 4:
                    self.hover_start_button = False

    def animate_button(self):

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.button_logic(mouse_pos)
        else:
            self.hover_play_button = False
            self.hover_play_button = False
            self.hover_back_button = False
            self.hover_start_button = False
            self.hover_sound_button = False

    def update_slide(self):

        if self.on_main_menu and self.slide < 0:
            self.slide += 8
        elif not self.on_main_menu and self.slide > -600:
            self.slide -= 8

        self.back_rect.top = 610+self.slide
        self.start_rect.centery = 1730+self.slide

    def scroll_page(self, button):

        if button == 4 and self.slide < -600:
            self.slide += 30
        elif button == 5 and self.slide > -1240:
            self.slide -= 30

    def save_sound_bool(self):

        p_dump(play_sound, open('data/data/sound_state.bat', 'wb'))

        if play_sound:
            self.sound_up = self.sound_on_up
            self.sound_down = self.sound_on_down
        else:
            self.sound_up = self.sound_off_up
            self.sound_down = self.sound_off_down

    def toggle_sound(self):

        global play_sound

        if play_sound:
            play_sound = False
        else:
            play_sound = True

        self.save_sound_bool()

    def run(self):

        self.draw()
        self.animate_button()
        self.update_slide()


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Magma Runner')
game_icon = pygame.image.load('graphics/others/magma.png').convert_alpha()
pygame.display.set_icon(game_icon)
fire_font = pygame.font.Font('data/font/Flame on!.ttf', 20)
game_over_font = pygame.font.Font('data/font/Flame on!.ttf', 45)
scroll_font = pygame.font.Font('data/font/Requiem.ttf', 38)
score_font = pygame.font.Font('data/font/Requiem.ttf', 25)
scroll_heading = pygame.font.Font('data/font/Requiem.ttf', 48)
play_sound = load_sound_bool()

background = pygame.image.load(
    'graphics/terrain/background.png').convert_alpha()
magma_tile = pygame.image.load(
    'graphics/terrain/magma_tile.png').convert_alpha()
floor = pygame.image.load('graphics/terrain/floor.png').convert_alpha()

fire_heart_png = pygame.image.load(
    'graphics/others/fire_heart.png').convert_alpha()
fiery_heart_png = pygame.image.load(
    'graphics/others/fiery_heart.png').convert_alpha()

main_background = pygame.image.load(
    'graphics/terrain/lava_under_world.png').convert_alpha()

click_sound = pygame.mixer.Sound('graphics/sound/click_sound.wav')
drop_sound = pygame.mixer.Sound('graphics/sound/falling_thud.wav')
life_sound = pygame.mixer.Sound('graphics/sound/life_sound.wav')

game_over_text = game_over_font.render('GAME OVER', False, (100, 90, 200))
game_over_rect = game_over_text.get_rect(center=(400, 270))


game = Main()
main_menu = MainMenu()
player = pygame.sprite.GroupSingle(player_sprite.Player())
fire_group = pygame.sprite.Group()
fly_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_no_attack_group = pygame.sprite.Group()
enemy_list = ['Mr Chomps', 'Gizzly Bear', 'Orc',
              'Mushroom', 'Big Red', 'Snail', 'Mutant Plant']

WISPY_SPAWNER = pygame.USEREVENT+1
ENEMY_SPAWNER = pygame.USEREVENT+2
FLY_SPAWNER = pygame.USEREVENT+3
CHANGE_SCOTTY_MOVT = pygame.USEREVENT+4
STOP_SCOTTY_MOVT = pygame.USEREVENT+5
SCORE = pygame.USEREVENT+6
pygame.time.set_timer(CHANGE_SCOTTY_MOVT, 1_000)
pygame.time.set_timer(WISPY_SPAWNER, 10_000)
pygame.time.set_timer(STOP_SCOTTY_MOVT, 4_000)
pygame.time.set_timer(FLY_SPAWNER, 60_000)
pygame.time.set_timer(ENEMY_SPAWNER, 2_200)
pygame.time.set_timer(SCORE, 800)

ok = False
while True:

    pygame.display.update()
    clock.tick(60)
    screen.fill('grey')

    if main_menu.playing:
        game.run()
    else:
        main_menu.run()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if main_menu.playing:
                    game.button_logic(event.pos, True)
                else:
                    main_menu.button_logic(event.pos, True)
            elif event.button >= 4 and not main_menu.playing and not main_menu.on_main_menu:
                main_menu.scroll_page(event.button)
        if main_menu.playing:
            if game.game_started:
                if event.type == CHANGE_SCOTTY_MOVT:
                    game.change_scotty_movt()
                if event.type == STOP_SCOTTY_MOVT:
                    game.stop_scotty_movt()
                if not game.game_over:
                    if event.type == WISPY_SPAWNER:
                        game.spawn_wispy()
                    if event.type == ENEMY_SPAWNER:
                        game.spawn_enemy()
                    if event.type == FLY_SPAWNER:
                        game.spawn_fly()
                    if event.type == SCORE:
                        game.score += 1
                        game.update_high_score()
