import pygame
import config
from engine import events


class MarginMixin:
    def __init__(self):
        self.margin = [0, 0, 0, 0]

    def _set_margin(self, index, value):
        if isinstance(value, (int, float)):
            self.margin[index] = value
        elif isinstance(value, str) and value.isdigit():
            self.margin[index] = int(value)
        else:
            raise ValueError(f'Некорректное значение Margin: {value}, принимаемые типы int, float, str(digit)')

    @property
    def margin_left(self):
        return self.margin[0]

    @margin_left.setter
    def margin_left(self, value):
        self._set_margin(0, value)

    @property
    def margin_top(self):
        return self.margin[1]

    @margin_top.setter
    def margin_top(self, value):
        self._set_margin(1, value)

    @property
    def margin_right(self):
        return self.margin[2]

    @margin_right.setter
    def margin_right(self, value):
        self._set_margin(2, value)

    @property
    def margin_bottom(self):
        return self.margin[3]

    @margin_bottom.setter
    def margin_bottom(self, value):
        self._set_margin(3, value)


class Button(MarginMixin):
    def __init__(self, font_path, size, name, color, event):
        super().__init__()
        self.size = size
        self.name = name
        self.font_path = font_path

        self.font = pygame.font.Font(font_path, size)
        self.btn_surface = self.font.render(name, True, color)
        self.width = self.btn_surface.get_width()
        self.rect = None

        self.event = event

    def get_change_button(self, color, size=None):
        if not size:
            size = self.size

        return Button(self.font_path, size, self.name, color, self.event)


class BaseMenu(MarginMixin):
    FONT_PATH = '../fonts/Marske.ttf'
    BUTTON_NAMES = ()
    SIZE = 65

    BASE_COLOR = 'White'
    HOVER_COLOR = (121, 184, 233)

    def __init__(self):
        super().__init__()
        self.menu_buttons = []

        for name, event in self.BUTTON_NAMES:
            button = Button(self.FONT_PATH, self.SIZE, name, self.BASE_COLOR, event)
            self.menu_buttons.append(button)

        self.len_menu = len(self.menu_buttons)

    def draw(self, surface, surface_rect=None):
        if not surface_rect:
            surface_rect = surface.get_rect()

        mouse = pygame.mouse.get_pos()
        counter = 0
        for button in self.menu_buttons:

            if counter > self.len_menu:
                counter = 0

            x = button.margin_left + self.margin_left
            if counter > 0:
                y = (self.SIZE * counter) + button.margin_top + self.margin_top
            else:
                y = button.margin_top + self.margin_top

            if button.rect and self.check_hover(button, mouse):
                button = button.get_change_button(self.HOVER_COLOR)
                if pygame.mouse.get_pressed()[0]:
                    new_game_event = pygame.event.Event(button.event)
                    pygame.event.post(new_game_event)

            button.rect = button.btn_surface.get_rect(topleft=(surface_rect.left + x, surface_rect.top + y))

            counter += 1
            surface.blit(button.btn_surface, (x, y))

    @staticmethod
    def check_hover(button, mouse):
        return button.rect.collidepoint(mouse)


class MainMenu(BaseMenu):
    BUTTON_NAMES = (('Новая игра', events.NEW_GAME),
                    ('Продолжить', ''),
                    ('Загрузить', ''),
                    ('Настройки', ''),
                    ('Выйти', pygame.QUIT))


class PauseMenu(BaseMenu):
    BUTTON_NAMES = (('Продолжить', ''),
                    ('Загрузить', ''),
                    ('Настройки', ''),
                    ('В главное меню', events.TO_MAIN_MENU),
                    ('Выйти', pygame.QUIT))

