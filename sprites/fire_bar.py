import pygame
from random import choice as rand_choice


class FireBar:

    def __init__(self):

        super().__init__()
        self.qyt = 0
        self.bar_1 = pygame.image.load(
            'graphics/others/fire_bar/fire_bar_1.png').convert_alpha()
        self.bar_2 = pygame.image.load(
            'graphics/others/fire_bar/2.png').convert_alpha()
        self.bar_3 = pygame.image.load(
            'graphics/others/fire_bar/3.png').convert_alpha()
        self.heat_rect = pygame.rect.Rect(42, 28, 4, 2)
        self.add_a_life = False

    def update_heat(self):

        if self.qyt:
            heat_qyt = self.qyt*13-2
        else:
            heat_qyt = 4

        if self.heat_rect.width < heat_qyt:
            self.heat_rect.width += 2
        elif self.heat_rect.width > heat_qyt:
            self.heat_rect.width -= 2

    def add_life(self):

        if self.qyt >= 12 and self.heat_rect.width == 154:
            self.add_a_life = True
            self.qyt = 0

    def display_bar(self, screen):

        screen.blit(self.bar_1, (10, 0))
        screen.blit(self.bar_2, (74, 0))
        screen.blit(self.bar_3, (138, 0))
        pygame.draw.rect(screen, (255, 90, 0), self.heat_rect)

    def collect_heat(self):

        increment_value = rand_choice([3, 5])
        self.qyt += increment_value

    def run(self, screen):

        self.display_bar(screen)
        self.update_heat()
        self.add_life()
