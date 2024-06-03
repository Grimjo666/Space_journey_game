import pygame


def get_text_surface(text, size=30):
    font = pygame.font.Font('fonts/Merriweather-Black.ttf', size)

    text_surface = font.render(text, False, 'White', 'Black')

    return text_surface
