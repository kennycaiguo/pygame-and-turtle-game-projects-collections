import pygame as pg
from constants import *
import random as rnd

# 加载盾牌和闪电
powerup_images = {}
powerup_images['shield'] = pg.image.load(pic_path+'shield.png')
powerup_images['gun'] = pg.image.load(pic_path+'bolt2.png')



class Power(pg.sprite.Sprite):
    def __init__(self, center) -> None:
        pg.sprite.Sprite.__init__(self)
        self.type = rnd.choice(['shield','gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


