import pygame
import os
import sys
import pygame_gui
from Game import *
from Game2 import *

pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
try:
    pygame.mixer.music.load('27.mp3')
    # dead = pygame.mixer.Sound('3')
except pygame.error:
    print('error')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(message)
        sys.exit()
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def game_over():
    pass


pygame.display.set_caption("Start")
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
fon = pygame.transform.scale(load_image('fon0.png'), (800, 600))
background.blit(fon, (0, 0))

# создаём менеджер GUI
manager = pygame_gui.UIManager((800, 600))
# создание элементов GUI
# кнопка для изменения цвета фона

# кнопки для смены цвета фона при наведении на них
level1_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((280, 435), (100, 50)),
    text='Level_1',
    manager=manager
)
level2_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((430, 435), (100, 50)),
    text='Level_2',
    manager=manager
)

# создание выпадающего списка для выбора уровня сложности игры
# элементами раскрывающегося списка могут быть только строки


# строка для ввода текста (например, имени игрока)
entry_name = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((350, 125), (100, 25)),
    manager=manager
)

start_screen()
P1 = Player()
P2 = Player2()
platforms = pygame.sprite.Group()
boofers = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

clock = pygame.time.Clock()

pygame.mixer.music.play(-1)
run = True
while run:

    # некоторые элементы GUI используют время,
    # поэтому необходима переменная для его хранения
    time_delta = clock.tick(60) / 1000

    for event in pygame.event.get():
        # fon = pygame.transform.scale(load_image('fon0.png'), (800, 600))
        # background.blit(fon, (0, 0))

        # вывод результата выбора раскрывающегося списка в консоль
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == level1_button:
                b = level_01()
                if b:
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((250, 200), (300, 200)),
                        manager=manager,
                        window_title="Победа!",
                        action_long_desc="Поздравляю, с победой!!!Выйти из игры?",
                        action_short_name='OK',
                        blocking=True
                    )
                else:
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((250, 200), (300, 200)),
                        manager=manager,
                        window_title="Поражение!",
                        action_short_name='OK',
                        blocking=True
                    )

                game_over()
            if event.ui_element == level2_button:
                b = level_02()

        # вывод текста из entry в консоль
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED \
                and event.ui_element == entry_name:
            print(event.text)

        # если пользователь хочет выйти, вызывается диалог подтверждения выхода
        if event.type == pygame.QUIT:
            confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((250, 200), (300, 200)),
                manager=manager,
                window_title="Подтверждение",
                action_long_desc="Вы уверены, что хотите выйти?",
                action_short_name='OK',
                blocking=True
            )

        # если в окне подтверждения выхода нажали OK
        if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            run = False

        # подключение менеджера GUI к обработке событий
        manager.process_events(event)

    window_surface.blit(background, (0, 0))
    # обновление менеджера GUI / отрисовка измененных элементов GUI
    manager.update(time_delta)
    manager.draw_ui(window_surface)
    pygame.display.update()
