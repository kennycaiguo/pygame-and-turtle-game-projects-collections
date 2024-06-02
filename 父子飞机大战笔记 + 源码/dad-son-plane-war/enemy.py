import random as rnd
import pygame as pg
from constants import *
from funcs import *
from enemybullet import *


enemies_images = [] #保存敌机图片对象的列表

enemies_list = [
    'dj1.png',
    'dj2.png',
    'dj3.png'
]

# 加载敌机
for img in enemies_list:
    enemies_img = pg.image.load(pic_path+img)
    enemies_img = pg.transform.scale(enemies_img,(80,60))
    enemies_images.append(enemies_img)

# 敌机类
class Enemy(pg.sprite.Sprite):
    def __init__(self) -> None:
        pg.sprite.Sprite.__init__(self) # 调用父类构造函数
        self.image_orig = rnd.choice(enemies_images) # 随机获取一张图片
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.90/2)
        self.rect.x = rnd.randrange(0,WIDTH-self.rect.width)
        self.rect.y = rnd.randrange(-150,-100)
        self.speedy = rnd.randrange(2,5)
        self.speedx = rnd.randrange(-3,3)
        self.shoot_delay = 1000
        self.last_shot = pg.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if rnd.randrange(10) >= 6:
            self.enemy_shoot()
        # 超出范围敌机重生
        if(self.rect.top > HEIGHT+10) or (self.rect.left < -25) or (self.rect.right > WIDTH+20):  
            self.rect.x = rnd.randrange(0,WIDTH-self.rect.width)
            self.rect.y = rnd.randrange(-100,-40)
            self.speedy = rnd.randrange(1,5)
        # 碰到两边会反弹    
        if self.rect.left < 0 :
            self.speedx = -self.speedx
        if self.rect.right > WIDTH:
            self.speedx = -self.speedx

    def enemy_shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # d敌机创建子弹
            enemy_bullet = EnemyBullet(self.rect.centerx,self.rect.bottom)   
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)
            ene_shoot_sound.play()




