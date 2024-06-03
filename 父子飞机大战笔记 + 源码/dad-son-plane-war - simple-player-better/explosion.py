import pygame as pg
import random as rnd
from constants import *
from funcs import *

#加载爆炸图片
explosion_anim = {}
explosion_anim['sm'] = []
explosion_anim['lg'] = []
explosion_anim['player'] = []

for i in range(8): #敌机，火山石爆炸
    filename = 'dd{}.png'.format(i+1)
    img = pg.image.load(pic_path + filename)
    img.set_colorkey(BLACK)
    #大爆炸
    img_lg = pg.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    #小爆炸
    img_sm = pg.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm) 
    # 玩家爆炸
    filename = 'sonic{}.png'.format(i+1)
    img2 = pg.image.load(pic_path + filename)
    img2.set_colorkey(BLACK)
    explosion_anim['player'].append(img2)

# 爆炸类
class Explosion(pg.sprite.Sprite):
    def __init__(self,center,size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frma_rate = 75

    def update(self) -> None:
        now = pg.time.get_ticks()
        if now - self.last_update > self.frma_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
               center = self.rect.center # 获取上一帧的中心点
               self.image = explosion_anim[self.size][self.frame]  
               self.rect = self.image.get_rect()
               self.rect.center = center   # 设置到当前帧的中心点
        



