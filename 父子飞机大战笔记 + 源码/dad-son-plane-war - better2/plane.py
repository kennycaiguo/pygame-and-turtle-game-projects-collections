from typing import Any
import pygame as pg
from constants import *
from bullet import *
from missile import *
import random as rnd

# 加载玩家飞机图片
player_img1 = pg.image.load(pic_path+"my1.png")
player_mini_img1 = pg.transform.scale(player_img1,(20,19))
player_mini_img1.set_colorkey(BLACK)
player_img2 = pg.image.load(pic_path+"my2.png")
player_mini_img2 = pg.transform.scale(player_img2,(30,19))
player_mini_img2.set_colorkey(BLACK)



class Plane(pg.sprite.Sprite):
    """"玩家飞机类"""
    def __init__(self, playerImg,center,bottom,K_LEFT,K_RIGHT,K_UP,K_DOWN) -> None:
        super().__init__()
        self.image = pg.transform.scale(playerImg,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = center
        self.rect.bottom = bottom
        self.speed = 5
        self.shield = 100 #血量
        self.redius = 20 #杀伤力
        self.shoot_delay = 250 #子弹延迟
        self.last_shot = pg.time.get_ticks() #最后一次射击时间
        self.lives = 3 # 飞机架数
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power = 3
        self.power_timer = pg.time.get_ticks() # 火力时间
        self.K_LEFT = K_LEFT
        self.K_RIGHT = K_RIGHT
        self.K_UP = K_UP
        self.K_DOWN = K_DOWN

    def update(self) -> None:
        # super().update()
        if self.power >=2 and pg.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pg.time.get_ticks() 
        if self.hidden and  pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 30  

        self.shoot()    # 是自动发射子弹的  
        self.move()     # 设置玩家移动边界
    

    def move(self):
        keys = pg.key.get_pressed() # 获取所有按下的键
        if keys[self.K_RIGHT]:
            if self.rect.right > WIDTH: # 右边越界
                self.rect.right = WIDTH
            else:
                self.rect.centerx += self.speed    
        if keys[self.K_LEFT]:
            if self.rect.left < 0 :# 左边越界
                self.rect.left = 0        
            else:
                self.rect.centerx -= self.speed
        if keys[self.K_UP]:
            if self.rect.y < 10:
                self.rect.top = 10
            else:
                self.rect.top -= self.speed

        if keys[self.K_DOWN]:
            if self.rect.bottom > HEIGHT-10:
                self.rect.bottom = HEIGHT-10     
            else:
                 self.rect.bottom += self.speed                

    def shoot(self):
        now = pg.time.get_ticks() # 获取现在的时间
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now # 保存最新的时间
            #单火力  
            if self.power ==1:
                bullet0 = Bullet(self.rect.centerx,self.rect.top)
                # bullet0 = Missile(self.rect.centerx,self.rect.top)
                
                # # 子弹需要添加到2个精灵组
                all_sprites.add(bullet0)
                bullets.add(bullet0)
                shooting_sound.set_volume(0.7)
                shooting_sound.play()
            #双火力  
            if self.power ==2:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                shooting_sound.set_volume(0.7)
                shooting_sound.play()
            #三火力  
            if self.power >=3:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                missile1 = Missile(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(missile1)
                shooting_sound.set_volume(0.7)
                shooting_sound.play()
                missile_sound.play()

    def powerup(self):
        self.power += 3
        self.power_timer = pg.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+200)




