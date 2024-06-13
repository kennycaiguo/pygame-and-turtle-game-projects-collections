import pygame as pg
from constants import *
import random as rnd

# 加载玩家飞机图片

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
# 敌机类
class Enemy(pg.sprite.Sprite):
    def __init__(self,game) -> None:
        self.game = game
        pg.sprite.Sprite.__init__(self) # 调用父类构造函数
        self.image_orig = rnd.choice(self.game.enemies_images) # 随机获取一张图片
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
            enemy_bullet = EnemyBullet(self.game,self.rect.centerx,self.rect.bottom)   
            self.game.all_sprites.add(enemy_bullet)
            self.game.enemy_bullets.add(enemy_bullet)
            self.game.ene_shoot_sound.play()



class EnemyBullet(pg.sprite.Sprite):
    def __init__(self,game,x,y) -> None:
        self.game = game
        pg.sprite.Sprite.__init__(self) # 这里不能用super(),必须用pg.sprite.Sprite.__init__(self)
        self.image = self.game.enemy_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 5
        self.radius = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT: # 超出屏幕的子弹会非销毁
            self.kill()    




# 爆炸类
class Explosion(pg.sprite.Sprite):
    def __init__(self,game,center,size):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = self.game.explosion_anim[size][0]
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
            if self.frame == len(self.game.explosion_anim[self.size]):
                self.kill()
            else:
               center = self.rect.center # 获取上一帧的中心点
               self.image = self.game.explosion_anim[self.size][self.frame]  
               self.rect = self.image.get_rect()
               self.rect.center = center   # 设置到当前帧的中心点



class Lava(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.image = rnd.choice(game.lava_list)
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

class Plane(pg.sprite.Sprite):
    """"玩家飞机类"""
    def __init__(self,game, playerImg,center,bottom,K_LEFT,K_RIGHT,K_UP,K_DOWN) -> None:
        self.game = game
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
                self.game.all_sprites.add(bullet0)
                self.game.bullets.add(bullet0)
                self.game.shooting_sound.set_volume(0.7)
                self.game.shooting_sound.play()
            #双火力  
            if self.power ==2:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                self.game.all_sprites.add(bullet1)
                self.game.bullets.add(bullet1)
                self.game.all_sprites.add(bullet2)
                self.game.bullets.add(bullet2)
                self.game.shooting_sound.set_volume(0.7)
                self.game.shooting_sound.play()
            #三火力  
            if self.power >=3:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                missile1 = Missile(self.rect.centerx,self.rect.top)
                self.game.all_sprites.add(bullet1)
                self.game.bullets.add(bullet1)
                self.game.all_sprites.add(bullet2)
                self.game.bullets.add(bullet2)
                self.game.all_sprites.add(missile1)
                self.game.bullets.add(missile1)
                self.game.shooting_sound.set_volume(0.7)
                self.game.shooting_sound.play()
                self.game.missile_sound.play()

    def powerup(self):
        self.power += 3
        self.power_timer = pg.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+200)





class Power(pg.sprite.Sprite):
    def __init__(self, game,center) -> None:
        pg.sprite.Sprite.__init__(self)
        self.type = rnd.choice(['shield','gun'])
        self.image = game.powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
