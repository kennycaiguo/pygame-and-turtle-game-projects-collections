import pygame as pg
from constants import *
missile_sound = pg.mixer.Sound(sound_path+'237071-Rocket_Launcher-02.wav')
class Missile(pg.sprite.Sprite):
    def __init__(self, x,y) -> None:
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(pic_path+'missile3.png'),(20,55))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -10

    def update(self, ) -> None:
       self.rect.y += self.speed
       if self.rect.bottom < 0:
           self.kill() # 子弹出界了就销毁