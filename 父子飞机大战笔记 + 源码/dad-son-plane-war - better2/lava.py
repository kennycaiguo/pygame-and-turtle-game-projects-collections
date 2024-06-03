import pygame as pg
from constants import *
import random as rnd

# 加载熔岩图片
lava_list = []
lava_pics = ['lava_med.png','lava_small1.png','lava_small2.png','lava_small3.png']
for pic in lava_pics:
    lava = pg.image.load(pic_path+pic)
    lava_list.append(lava)

class Lava(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = rnd.choice(lava_list)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = rnd.randint(0,WIDTH)
        self.rect.y = rnd.randint(0,HEIGHT)
        self.radius = 10
        self.speedy = 8

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x =  rnd.randint(0,WIDTH)    
            self.rect.y = rnd.randint(0,HEIGHT)