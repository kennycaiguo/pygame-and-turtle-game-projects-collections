import pygame as pg
from constants import *
from plane import *
from enemy import *
from explosion import *
import random as rnd
from power import *

#绘制文本的函数
def draw_text(surf,text,size,x,y):
    font = pg.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

def draw_screen_text(screen,player1,player2):
    draw_text(screen,str(score),18,WIDTH/2,10) #显示分数
    draw_shield_bar(screen,5,5,player1.shield)
    draw_shield_bar(screen,WIDTH-105,5,player2.shield)
    draw_lives(screen,10,20,player1.lives,player_mini_img1)
    draw_lives(screen,WIDTH-100,20,player2.lives,player_mini_img2)

# 绘制血条
def draw_shield_bar(screen,x,y,pct):
    pct = max(pct,0)
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill,BAR_HEIGHT)
    pg.draw.rect(screen,GREEN,fill_rect)
    pg.draw.rect(screen,WHITE,outline_rect,2)


def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img,img_rect)

# 创建敌机的函数   
def new_enemy():
    enemy = Enemy()     
    all_sprites.add(enemy)
    enemies.add(enemy)

def bullet_hit_enemy():
    """我方子弹打中敌人的函数"""    
    # 先进行我方子弹和敌机的碰撞检测
    global score
    hits = pg.sprite.groupcollide(enemies,bullets,True,True)
    for hit in hits:
        score += 50-hit.radius
        pg.mixer.Sound(sound_path+"exp.wav").play()
        #创建一个爆炸对象需要调用Explosion类
        expl = Explosion(hit.rect.center,'lg')
        # 将爆炸对象添加到所有精灵组
        all_sprites.add(expl)
        if rnd.random()> 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        # 每消灭一个敌机，又会创建一个敌机
        new_enemy()

# 我方飞机获取补给的方法，元素碰撞检测
def plane_get_power():
    sound = pg.mixer.Sound(sound_path+'FX054_cut.wav')
    for player in players:
        hits = pg.sprite.spritecollide(player,powers,True)
        for hit in hits:
            if hit.type == 'shield': 
                sound.play() 
                player.shield += rnd.randrange(20,40)
                if player.shield >=100:
                    player.shield = 100 # 血量不能超过100
            elif hit.type == 'gun': 
                sound.play()  
                player.powerup()
                 
#敌机子弹打中我方飞机
def enemy_hit_me():
    for player in players:
        hits = pg.sprite.spritecollide(player,enemy_bullets,True,pg.sprite.collide_circle)  
        for h in hits:
            player.shield -= h.radius *2 # 被打中会掉血
            expl = Explosion(h.rect.center,'sm') # 创建爆炸对象，添加到小爆炸里集合面
            all_sprites.add(expl) # 将爆炸对象添加到所有精灵组
            if player.shield <=0: # 血量掉光了就死掉了
                pg.mixer.Sound(sound_path+'exp.wav').play() #播放爆炸音效
                dead_expl = Explosion(player.rect.center,'player')
                all_sprites.add(dead_expl)
                player.hide() # 调用这个方法后几秒钟就会显示player
                player.lives -= 1 # 死掉了，就要减少一条命
                player.shield = 100 # 把player的血量设置位100，那么他就相当于新创建的了




