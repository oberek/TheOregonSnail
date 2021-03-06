#! /usr/bin/python

import pygame
from pygame import *
from pygame_functions import *

WIN_WIDTH = 1000
WIN_HEIGHT = 750
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

background_x = 0
background_y = 0


def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    setBackgroundImage("kitchen_background.jpg")
    # background = pygame.Surface(screen.get_size())
    # background.fill((255, 0, 255))
    # screen.blit(background, (0, 0))

    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    up = down = left = right = running = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    player.animate(Surface((32,32)).blit("snail.gif"))
    platforms = []

    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                                                                                                                                                                                                                                                                                                                                                                                                                      P",
        "P                                                                                                                                                                                                                                                                                                                                                                                                                                                      P",
        "P                                                                                                                                                                                                                                                                                                                                                                                                                                                      P",
        "P                    WWWWWWWWWWW                                                                                                                                                                                                                                                                                                                                                                                                                       P",
        "P                                                                                                                                                                                                                                                                                                                                                                                                                                                      P",
        "P                                                                                                                                                                                                                                                                                                                                                                                                                                                      P",
        "P                                                                                                                                   WWWWWWW                                                                                                                                                                                                                                                                                                            P",
        "P    WWWWWWWW                                                                                                                                                                                                                                                                                                                                                                                                                                          P",
        "P                                                                                                                                                                                                                                                                                                                                                                                                                                                      P",
        "P                          WWWWWWWWW                                                                                                                                                                                                                                                                                                                                                                                                                   P",
        "P                                                 WWWWWWWWWW                                                                                                                                                                                                                                                                                                                                                                                           P",
        "P                                                                                                               WWWWWWWWWWW                                                                                                                                                                                                                                                                                                                            P",
        "P         WWWWWWW                                                                                                                                                                                                                                                                                                                                                                                                                                      P",
        "P                                                                                                                                                                                                                                                                                                                                                                                                                                                      P",
        "P                     WWWWWWWWW                                                                                                                            WWW                                                                                                                                                                                                                                                                                         P",
        "P                                                                                          WWWWWWWWWWWWWW                                                                                                                                                                                                                                                                                                                                              P",
        "P   WWWWWWWWWWW                                                                                                                                                                                                                                                                                                                                                                                                                                        P",
        "P                                                                               PPP                                                                                                                                                                                                                                                                                                                                                                    P",
        "P                 WWWWWWWWWWWWWW                                                 P                                                                                                                                                                                                                                                                                                                                                                     P",
        "P                                                                                P                                                                                                                                                                                                                                                                                                                                                                     P",
        "P                                                                                P                                                                                                                                                                                                                                                                                                                                                                     P",
        "P                                                                      P         P        P                                                                                                                                                                                                                                                                                                                                                            P",
        "P                                                                      P         P        P                                                                                                                                                                                                                                                                                                                                                            P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "W":
                w = Platform(x, y)
                platforms.append(w)
                entities.add(w)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)
    # global background_x, background_y
    # BackGround = Background('kitchen_background.jpg', [background_x, background_y])
    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit("ESCAPE")
            if e.type == KEYDOWN and (e.key == K_UP or e.key == K_w):
                up = True
            if e.type == KEYDOWN and (e.key == K_DOWN or e.key == K_s):
                down = True
            if e.type == KEYDOWN and (e.key == K_LEFT or e.key == K_a):
                left = True
            if (e.type == KEYDOWN) and (e.key == K_RIGHT or e.key == K_d):
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True

            if e.type == KEYUP and (e.key == K_UP or e.key == K_w):
                up = False
            if e.type == KEYUP and (e.key == K_DOWN or e.key == K_s):
                down = False
            if e.type == KEYUP and (e.key == K_RIGHT or e.key == K_d):
                right = False
            if e.type == KEYUP and (e.key == K_LEFT or e.key == K_a):
                left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        # screen.blit(BackGround.image, BackGround.rect)
        player.update(up, down, left, right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        # if right:
        #     background_x = background_x - 1
        # if left:
        #     background_x = background_x + 1

        # BackGround = Background('kitchen_background.jpg', [background_x, background_y])
        pygame.display.update()

# class Background(pygame.sprite.Sprite):
#     def __init__(self, image_file, location):
#         pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
#         self.image = pygame.image.load(image_file)
#         self.rect = self.image.get_rect()
#         self.rect.left, self.rect.top = location

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def animate(self, frame):
        self.image = Surface((300, 150), pygame.SRCALPHA)
        self.image.blit(frame, (0, 0))

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)


    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.rect.top -= self.yvel


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)
        # self.image.blit()

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))

if __name__ == "__main__":
    main()