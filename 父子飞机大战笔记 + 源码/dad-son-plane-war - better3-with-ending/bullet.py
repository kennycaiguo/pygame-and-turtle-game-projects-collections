import pygame as pg
from constants import *

shooting_sound = pg.mixer.Sound(sound_path+'pew-gunshot-13.wav')

class Bullet(pg.sprite.Sprite):
    def __init__(self, x,y) -> None:
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(pic_path+'pd333.png'),(15,40))
        # self.image = pg.transform.scale(pg.image.load(pic_path+'enemy_bullet2.png'),(15,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -10

    def update(self, ) -> None:
       self.rect.y += self.speed
       if self.rect.bottom < 0:
           self.kill() # 子弹出界了就销毁