import pygame
from pygame.locals import *
import sys
import os
import pygame_gui

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
manager = pygame_gui.UIManager((800, 600))
is_victory = False
try:
    pygame.mixer.music.load('27.mp3')
    jump = pygame.mixer.Sound('bib.ogg')
    tramplin = pygame.mixer.Sound('tranplin.ogg')
    dead = pygame.mixer.Sound('kcreek.ogg')
    victory = pygame.mixer.Sound('victory.ogg')
except pygame.error:
    print('error')

vec = pygame.math.Vector2
HEIGHT = 550
WIDTH = 800
ACC = 0.5
FRIC = -0.12
FPS = 60
FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


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


class Player(pygame.sprite.Sprite):
    # image = load_image("fire5.png")
    animation_frames_left = []
    animation_frames_right = []
    # создаем экран и загружаем изображение в переменную sprite, установив методом convert_alpha необходимую прозрачность
    image = load_image('3b2.png')
    image.set_colorkey(image.get_at((0, 0)))
    image = image.convert_alpha()

    # находим длину, ширину изображения и размеры каждого кадра
    width, height = image.get_size()
    w, h = width / 10, height
    for j in range(int(height / h)):
        # производим итерацию по элементам строки
        for i in range(int(width / w)):
            # добавляем  в список отдельные кадры
            img = image.subsurface(pygame.Rect(i * w, 0, w, h))
            colorkey = img.get_at((0, 0))
            img.set_colorkey(colorkey)
            img.convert_alpha()

            animation_frames_left.append(img)

    image = load_image('3b.png')
    image.set_colorkey(image.get_at((0, 0)))
    image = image.convert_alpha()

    # находим длину, ширину изображения и размеры каждого кадра
    width, height = image.get_size()
    w, h = width / 10, height
    for j in range(int(height / h)):
        # производим итерацию по элементам строки
        for i in range(int(width / w)):
            # добавляем  в список отдельные кадры
            animation_frames_right.append(image.subsurface(pygame.Rect(i * w, 0, w, h)))
    animation_frames_right.reverse()

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 128, 128))
        self.image = Player.animation_frames_right[0]
        self.counter2 = 0
        self.cur2 = 0
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask2 = pygame.mask.from_surface(self.image)
        self.surf = self.image
        self.is_jump = False
        self.is_victory = False
        self.pos = vec((20, 500))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.is_dead = False

    def move(self):
        self.acc = vec(0, 0.05)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.pos.x > 20:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT] and self.pos.x < 780:
            self.acc.x = ACC
        if (pressed_keys[K_SPACE] or pressed_keys[K_UP]) and not self.is_jump:
            self.vel += vec(0, -2.5)
            # self.pos.y -= 50
            self.is_jump = True
            jump.play()

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH - 20
            self.vel.x = 0
            # self.acc.x = 0
        if self.pos.x < 0:
            self.pos.x = 20
            self.vel.x = 0
            # self.acc.x = 0
        if self.pos.x < 100 and self.pos.y < 100:
            self.is_victory = True

        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits:
            if hits[0].type == 2:
                dead.play()
                self.is_dead = True
            # print(hits[0].line_width)
            if self.vel.y > 0:
                self.is_jump = False
                self.pos.y = hits[0].rect.top + 1
                # self.pos.y += 10
                self.vel.y = 0
            else:
                self.vel.y = - self.vel.y
        for obs in obstacles:
            hits2 = pygame.sprite.collide_mask(self, obs)
            if hits2:
                tramplin.play()
                self.pos.y -= 50
        if abs(self.vel.x) <= 0.5:
            self.counter2 = 0
        else:
            self.cur2 = (self.cur2 + abs(self.vel.x)) % 10000
            self.counter2 = int(self.cur2 / 10) % 10
        if self.vel.x >= 0:
            self.surf = Player.animation_frames_right[self.counter2]
        else:
            self.surf = Player.animation_frames_left[self.counter2]

    def update2(self):
        hits2 = pygame.sprite.spritecollide(P1, boofers, False)
        if hits2:
            print(hits2)
            if self.vel.x > 0:
                self.vel.x = - 5
            else:
                self.vel.x = + 5


class Player2(pygame.sprite.Sprite):
    # image = load_image("fire5.png")
    animation_frames_left = []
    animation_frames_right = []
    # создаем экран и загружаем изображение в переменную sprite, установив методом convert_alpha необходимую прозрачность
    image = load_image('3a.png')
    image.set_colorkey(image.get_at((0, 0)))
    image = image.convert_alpha()

    # находим длину, ширину изображения и размеры каждого кадра
    width, height = image.get_size()
    w, h = width / 10, height
    for j in range(int(height / h)):
        # производим итерацию по элементам строки
        for i in range(int(width / w)):
            # добавляем  в список отдельные кадры
            img = image.subsurface(pygame.Rect(i * w, 0, w, h))
            colorkey = img.get_at((0, 0))
            img.set_colorkey(colorkey)
            img.convert_alpha()

            animation_frames_left.append(img)

    image = load_image('3a2.png')
    image.set_colorkey(image.get_at((0, 0)))
    image = image.convert_alpha()

    # находим длину, ширину изображения и размеры каждого кадра
    width, height = image.get_size()
    w, h = width / 10, height
    for j in range(int(height / h)):
        # производим итерацию по элементам строки
        for i in range(int(width / w)):
            # добавляем  в список отдельные кадры
            animation_frames_right.append(image.subsurface(pygame.Rect(i * w, 0, w, h)))
    animation_frames_right.reverse()

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 128, 128))
        self.image = Player2.animation_frames_right[0]
        self.counter = 0
        self.cur = 0
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.surf = self.image
        self.is_jump = False
        self.is_dead = False
        self.is_victory = False

        self.pos2 = vec((40, 500))
        self.vel2 = vec(0, 0)
        self.acc2 = vec(0, 0)

    def move(self):
        self.acc2 = vec(0, 0.05)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a] and self.pos2.x > 20:
            self.acc2.x = -ACC
        if pressed_keys[K_d] and self.pos2.x < 780:
            self.acc2.x = ACC
        if (pressed_keys[K_SPACE] or pressed_keys[K_w]) and not self.is_jump:
            self.vel2 += vec(0, -2.5)
            # self.pos.y -= 50
            self.is_jump = True
            jump.play()

        self.acc2.x += self.vel2.x * FRIC
        self.vel2 += self.acc2
        self.pos2 += self.vel2 + 0.5 * self.acc2

        if self.pos2.x > WIDTH:
            self.pos2.x = WIDTH - 20
            self.vel2.x = 0
            # self.acc.x = 0
        if self.pos2.x < 0:
            self.pos2.x = 20
            self.vel2.x = 0
            # self.acc.x = 0
        if self.pos2.x < 100 and self.pos2.y < 100:
            self.is_victory = True

        self.rect.midbottom = self.pos2

    def update(self):
        hits = pygame.sprite.spritecollide(P2, platforms, False)
        if hits:
            if hits[0].type == 1:
                dead.play()
                self.is_dead = True
            if self.vel2.y > 0:
                self.is_jump = False
                self.pos2.y = hits[0].rect.top + 1
                # self.pos.y += 10
                self.vel2.y = 0
            else:
                self.vel2.y = - self.vel2.y
        for obs in obstacles:
            hits2 = pygame.sprite.collide_mask(self, obs)
            if hits2:
                tramplin.play()
                self.pos2.y -= 50
        if abs(self.vel2.x) <= 0.5:
            self.counter = 0
        else:
            self.cur = (self.cur + abs(self.vel2.x)) % 10000
            self.counter = int(self.cur / 10) % 10
        if self.vel2.x >= 0:
            self.surf = Player2.animation_frames_right[self.counter]
        else:
            self.surf = Player2.animation_frames_left[self.counter]

    def update2(self):
        hits2 = pygame.sprite.spritecollide(P2, boofers, False)
        if hits2:
            print(hits2)
            if self.vel2.x > 0:
                self.vel2.x = - 5
            else:
                print(1)
                self.vel2.x = + 5


class platform(pygame.sprite.Sprite):
    def __init__(self, height, width, shift=0, line_width=15, type=0):
        super().__init__()
        self.surf = pygame.Surface((width, line_width))
        self.surf.fill((128, 128, 128))
        self.rect = self.surf.get_rect(center=(width / 2 + shift, height - 10))
        self.line_width = line_width
        self.type = type


class boofer(pygame.sprite.Sprite):
    def __init__(self, height, shift=0, line_width=15):
        super().__init__()
        self.surf = pygame.Surface((2, line_width))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(center=(2 / 2 + shift, height - 10))


class obstacle(pygame.sprite.Sprite):
    def __init__(self, sp_coord, sp_center):
        super().__init__()
        self.surf = pygame.Surface((30, 30))

        # self.surf.fill((255, 255, 255))
        pygame.draw.polygon(self.surf, (128, 128, 128), sp_coord)
        self.rect = self.surf.get_rect(center=sp_center)
        self.mask = pygame.mask.from_surface(self.surf)
        self.pos3 = vec((200, 20))


def start_screen():
    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    displaysurface.blit(fon, (0, 0))


def level_02():
    global P1, P2, is_victory
    P1 = Player()
    P2 = Player2()
    platforms.empty()
    boofers.empty()
    obstacles.empty()
    PT1 = platform(HEIGHT - 10, 800)
    PT2 = platform(HEIGHT - 100, 350)
    PT5 = platform(HEIGHT - 100, 200, 500)
    PT3 = platform(HEIGHT - 188, 100, 100)
    PT4 = platform(HEIGHT - 185, 300, 200, 6, 1)
    PT6 = platform(HEIGHT - 95, 150, 350, 6, 2)
    PT7 = platform(HEIGHT - 188, 200, 400)
    PT8 = platform(HEIGHT - 185, 100, 600, 6, 2)
    PT9 = platform(HEIGHT - 188, 100, 700)
    PT10 = platform(HEIGHT - 280, 50)
    PT11 = platform(HEIGHT - 280, 200, 150)
    PT12 = platform(HEIGHT - 280, 50, 500)
    PT13 = platform(HEIGHT - 280, 50, 650)
    PT14 = platform(HEIGHT - 275, 650, 0, 6, 1)
    PT15 = platform(HEIGHT - 370, 50, 100)
    PT16 = platform(HEIGHT - 370, 250, 300)
    PT17 = platform(HEIGHT - 370, 100, 700)
    PT18 = platform(HEIGHT - 365, 550, 150, 6, 1)
    PT19 = platform(HEIGHT - 460, 700)
    # PT20 = platform(HEIGHT - 364, 300, 100, 8, 1)
    # PT21 = platform(HEIGHT - 274, 150, 350, 8, 1)
    PT22 = platform(HEIGHT - 272, 700, 0, 4)
    PT23 = platform(HEIGHT - 362, 700, 100, 4)
    PT24 = platform(HEIGHT - 182, 700, 100, 4)
    B1 = boofer(HEIGHT - 99, 350)
    B2 = boofer(HEIGHT - 99, 500)
    B3 = boofer(HEIGHT - 99, 700)
    B4 = boofer(HEIGHT - 187, 200)
    B5 = boofer(HEIGHT - 187, 100)
    B6 = boofer(HEIGHT - 187, 700)
    B7 = boofer(HEIGHT - 187, 600)
    B8 = boofer(HEIGHT - 187, 400)
    B9 = boofer(HEIGHT - 279, 50)
    B10 = boofer(HEIGHT - 279, 350)
    B11 = boofer(HEIGHT - 279, 150)
    B12 = boofer(HEIGHT - 279, 500)
    B13 = boofer(HEIGHT - 279, 550)
    B14 = boofer(HEIGHT - 279, 700)
    B15 = boofer(HEIGHT - 279, 650)
    B16 = boofer(HEIGHT - 369, 100)
    B17 = boofer(HEIGHT - 369, 150)
    B18 = boofer(HEIGHT - 369, 300)
    B19 = boofer(HEIGHT - 369, 550)
    B20 = boofer(HEIGHT - 369, 700)
    B21 = boofer(HEIGHT - 459, 700)
    O1 = obstacle([[29, 29], [0, 29], [0, 0]], (15, 240))
    O2 = obstacle([[29, 29], [0, 29], [0, 0]], (15, 420))
    O3 = obstacle([[29, 29], [0, 29], [29, 0]], (785, 330))
    O4 = obstacle([[29, 29], [0, 29], [29, 0]], (785, 510))
    O5 = obstacle([[29, 29], [0, 29], [29, 0]], (785, 150))

    platforms.add(PT1)
    platforms.add(PT2)
    platforms.add(PT3)
    platforms.add(PT4)
    platforms.add(PT5)
    platforms.add(PT6)
    platforms.add(PT7)
    platforms.add(PT8)
    platforms.add(PT9)
    platforms.add(PT10)
    platforms.add(PT11)
    platforms.add(PT12)
    platforms.add(PT13)
    platforms.add(PT14)
    platforms.add(PT15)
    platforms.add(PT16)
    platforms.add(PT17)
    platforms.add(PT18)
    platforms.add(PT19)
    # platforms.add(PT20)
    # platforms.add(PT21)
    platforms.add(PT22)
    platforms.add(PT23)
    platforms.add(PT24)
    boofers.add(B1)
    boofers.add(B2)
    boofers.add(B3)
    boofers.add(B4)
    boofers.add(B5)
    boofers.add(B6)
    boofers.add(B7)
    boofers.add(B8)
    boofers.add(B9)
    boofers.add(B10)
    boofers.add(B11)
    boofers.add(B12)
    boofers.add(B13)
    boofers.add(B14)
    boofers.add(B15)
    boofers.add(B16)
    boofers.add(B17)
    boofers.add(B18)
    boofers.add(B19)
    boofers.add(B20)
    boofers.add(B21)
    obstacles.add(O1)
    obstacles.add(O2)
    obstacles.add(O3)
    obstacles.add(O4)
    obstacles.add(O5)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(O1)
    all_sprites.add(O2)
    all_sprites.add(O3)
    all_sprites.add(O4)
    all_sprites.add(O5)
    all_sprites.add(PT1)
    all_sprites.add(PT2)
    all_sprites.add(PT3)
    all_sprites.add(PT4)
    all_sprites.add(PT5)
    all_sprites.add(PT6)
    all_sprites.add(PT7)
    all_sprites.add(PT8)
    all_sprites.add(PT9)
    all_sprites.add(PT10)
    all_sprites.add(PT11)
    all_sprites.add(PT12)
    all_sprites.add(PT13)
    all_sprites.add(PT14)
    all_sprites.add(PT15)
    all_sprites.add(PT16)
    all_sprites.add(PT17)
    all_sprites.add(PT18)
    all_sprites.add(PT19)
    # all_sprites.add(PT20)
    # all_sprites.add(PT21)
    all_sprites.add(PT22)
    all_sprites.add(PT23)
    all_sprites.add(PT24)
    all_sprites.add(P1)
    all_sprites.add(P2)
    all_sprites.add(B1)
    all_sprites.add(B2)
    all_sprites.add(B3)
    all_sprites.add(B4)
    all_sprites.add(B5)
    all_sprites.add(B6)
    all_sprites.add(B7)
    all_sprites.add(B8)
    all_sprites.add(B9)
    all_sprites.add(B10)
    all_sprites.add(B11)
    all_sprites.add(B12)
    all_sprites.add(B13)
    all_sprites.add(B14)
    all_sprites.add(B15)
    all_sprites.add(B16)
    all_sprites.add(B17)
    all_sprites.add(B18)
    all_sprites.add(B19)
    all_sprites.add(B20)
    all_sprites.add(B21)
    pygame.mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                print(pygame.time.get_ticks())
                running = False

                # pygame.quit()
                # sys.exit()

        displaysurface.fill((0, 0, 0))
        fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
        displaysurface.blit(fon, (0, 0))
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
        P1.move()
        P1.update()
        P1.update2()
        P2.move()
        P2.update()
        P2.update2()
        a = False
        if P2.is_dead or P1.is_dead:
            print(pygame.time.get_ticks())
            running = False
        if P2.is_victory and P1.is_victory:
            victory.play()
            is_victory = True
            running = False
            a = True
            return is_victory
        pygame.display.update()
        FramePerSec.tick(FPS)


P1 = Player()
P2 = Player2()
platforms = pygame.sprite.Group()
boofers = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
if __name__ == '__main__':
    start_screen()
    P1 = Player()
    P2 = Player2()
    platforms = pygame.sprite.Group()
    boofers = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    level_02()
