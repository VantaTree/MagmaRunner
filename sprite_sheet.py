import pygame
from pickle import load as p_load


def get_frame(sheet, x_frame, direction, width, height):

    frame = pygame.Surface((width, height)).convert_alpha()
    frame.blit(sheet, (0, 0), (x_frame, 0, width, height))
    if direction == -1:
        frame = pygame.transform.flip(frame, True, False)
    frame.set_colorkey((0, 0, 0))
    return frame


def play_animation(sheet, frame, direction, width, height, speed=.4):

    pic = get_frame(sheet, int(frame)*width, direction, width, height)
    max_length = sheet.get_width()

    frame += speed

    if frame*width > max_length-height:
        frame = 0

    return pic, frame


def load_sound_bool():

    sound_state = p_load(open('data/data/sound_state.bat', 'rb'))

    return sound_state
