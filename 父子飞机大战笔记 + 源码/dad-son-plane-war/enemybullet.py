import pygame as pg
from constants import *
from funcs import *

enemy_bullet_img = pg.transform.scale(pg.image.load(pic_path+'enemy_bullet.png'),(15,25))
ene_shoot_sound = pg.mixer.Sound(sound_path+'enemy_bullet.wav')

class EnemyBullet(pg.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pg.sprite.Sprite.__init__(self) # 这里不能用super(),必须用pg.sprite.Sprite.__init__(self)
        self.image = enemy_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.radius =5
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT: # 超出屏幕的子弹会非销毁
            self.kill()    

