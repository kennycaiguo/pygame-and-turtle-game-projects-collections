import pygame as pg
import sys
from constants import *
from sprites import *
import os

class Game:
    def __init__(self) -> None:
        pg.init()       #初始化pygame模块
        pg.mixer.init() #初始化pygame模块的音效模块
        self.game_title = 'Kenny飞机大战游戏'
        self.font_name = pg.font.match_font('arial') # 获取系统里面安装了的字体名称
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption(self.game_title)
        self.clock = pg.time.Clock() 
        self.score = 0
        self.bg = pg.image.load(pic_path+'startfield.jpg')
        self.bg = pg.transform.scale(self.bg,(WIDTH,1536))
        self.running = True
        self.create_file()  # 如果没有highscore.txt就需要创建它
        self.load_datas()
       
    
    def create_file(self):
        file = './highscore.txt'
        if not os.path.exists(file):
            with open(file,'w') as f:
                f.write(str(0))

    def save_best_score(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open('./highscore.txt','w') as f:  
                f.write(str(self.score))          

    def load_datas(self):
        # 加载最好成绩
        file = open('./highscore.txt','r')
        self.highscore = int(file.read())
        file.close()
        # 加载玩家图片
        self.player_img1 = pg.image.load(pic_path+"my1.png")
        self.player_mini_img1 = pg.transform.scale(self.player_img1,(20,19))
        self.player_mini_img1.set_colorkey(BLACK)
        self.shooting_sound = pg.mixer.Sound(sound_path+'pew-gunshot-13.wav')
        self.enemies_images = [] #保存敌机图片对象的列表

        self.enemies_list = [
            'dj1.png',
            'dj2.png',
            'dj3.png'
        ]
        # 加载敌机
        for img in self.enemies_list:
            enemies_img = pg.image.load(pic_path+img)
            enemies_img = pg.transform.scale(enemies_img,(80,60))
            self.enemies_images.append(enemies_img)

        self.enemy_bullet_img = pg.transform.scale(pg.image.load(pic_path+'enemy_bullet.png'),(15,25))
        self.ene_shoot_sound = pg.mixer.Sound(sound_path+'enemy_bullet.wav')
        #加载爆炸图片
        self.explosion_anim = {}
        self.explosion_anim['sm'] = []
        self.explosion_anim['lg'] = []
        self.explosion_anim['player'] = []

        for i in range(8): #敌机，火山石爆炸
            filename = 'dd{}.png'.format(i+1)
            img = pg.image.load(pic_path + filename)
            img.set_colorkey(BLACK)
            #大爆炸
            img_lg = pg.transform.scale(img,(75,75))
            self.explosion_anim['lg'].append(img_lg)
            #小爆炸
            img_sm = pg.transform.scale(img,(32,32))
            self.explosion_anim['sm'].append(img_sm) 
            # 玩家爆炸
            filename = 'sonic{}.png'.format(i+1)
            img2 = pg.image.load(pic_path + filename)
            img2.set_colorkey(BLACK)
            self.explosion_anim['player'].append(img2)
        # 加载熔岩图片
        self.lava_list = []
        self.lava_pics = ['lava_med.png','lava_small1.png','lava_small2.png','lava_small3.png']
        for pic in self.lava_pics:
            lava = pg.image.load(pic_path+pic)
            self.lava_list.append(lava)  
        #导弹音效      
        self.missile_sound = pg.mixer.Sound(sound_path+'237071-Rocket_Launcher-02.wav')  
        # 加载盾牌和闪电
        self.powerup_images = {}
        self.powerup_images['shield'] = pg.image.load(pic_path+'shield.png')
        self.powerup_images['gun'] = pg.image.load(pic_path+'bolt2.png') 

    def new(self):
        #0.播放背景音乐
        pg.mixer.music.stop()
        pg.mixer.music.load(sound_path+'battle.ogg')
        pg.mixer.music.set_volume(0.8)
        pg.mixer.music.play(-1)
        self.score = 0
        # 1.创建精灵组
        # 所有精灵的精灵组
        self.all_sprites = pg.sprite.Group()
        # 我方子弹精灵组
        self.bullets = pg.sprite.Group()
        # 敌机精灵组
        self.enemies = pg.sprite.Group()
        # 敌人子弹精灵组
        self.enemy_bullets = pg.sprite.Group()
        # 补给精灵组
        self.powers = pg.sprite.Group()

        # 熔岩碎石精灵组
        self.lavas = pg.sprite.Group()

        #2.创建精灵
         # 3.创建玩家飞机
        self.player1 = Plane(self,self.player_img1,WIDTH/2,HEIGHT-30,pg.K_LEFT,pg.K_RIGHT,pg.K_UP,pg.K_DOWN)
        # 4.将他们添加到精灵组,这是必须的，因为只有精灵组才有绘制方法
        self.all_sprites.add(self.player1)
    
        # 创建敌机
        for i in range(4):
            self.new_enemy() # 这个方法可以创建敌机并且添加到all_sprites和enemies精灵组里面

        # 创建熔岩碎石
        for i in range(4):
            self.new_lava()   

        # 调用精灵组的更新方法
        self.all_sprites.update()
        # 3.调用run方法
        self.run()

    # run方法是游戏的主循环
    def run(self):
        global height
        self.playing = True 
        while self.playing:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                    self.save_best_score()
            # 背景图片向下滚动        
            self.screen.blit(self.bg,(0,height))
            height += 2
            if height > -168:
                height = -936        
            if self.player1.lives == 0: # 判断是否是游戏结束
                self.player1.shield = 0
                self.playing = False
            self.all_sprites.update()       # 调用精灵组的更新方法
            # 调用精灵组的更新方法
            self.all_sprites.draw(self.screen)  
            self.bullet_hit_enemy()              # 子弹打中敌人的碰撞检测
            self.plane_get_power(self.player1)        #我方飞机获取补给的碰撞检测
            self.enemy_hit_me(self.player1)           #敌机子弹打中我方飞机
            self.plane_crash(self.player1)            #我方飞机和敌机碰撞检测
            self.bullet_hit_lava()               #双方子弹打熔岩碎石的碰撞检测
            self.lava_hit_both_planes(self.player1)   #熔岩碎石碰撞双方飞机的碰撞检测
            self.bullet_vs_enemy_bullet()         # 双方子弹的碰撞检测
            self.draw_screen_text(self.player1) # 绘制血条和飞机架数
            pg.display.update()
                
    def exit_or_replay(self):
        pg.mixer.music.load(sound_path+'g-over.ogg')
        pg.mixer.music.play(-1)
        if not self.running:
            return   
        self.screen.blit(pg.image.load(pic_path+"menu.png"),(0,0))
        self.draw_text("Game Over",48,WIDTH/2,HEIGHT/2)
        self.draw_text("Press Any Key To Play Again",22,WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.save_best_score() # 保存好成绩
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if e.type == pg.KEYUP:
                    waiting = False    
        


    #绘制文本的函数
    def draw_text(self,text,size,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)  

    def draw_screen_text(self,player1):
        self.draw_text(str(self.score),18,WIDTH/2,10) #显示分数
        self.draw_shield_bar(5,5,player1.shield)
        self.draw_lives(10,20,player1.lives,self.player_mini_img1)
 

    # 绘制血条
    def draw_shield_bar(self,x,y,pct):
        pct = max(pct,0)
        fill = (pct/100) * BAR_LENGTH
        outline_rect = pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
        fill_rect = pg.Rect(x,y,fill,BAR_HEIGHT)
        pg.draw.rect(self.screen,GREEN,fill_rect)
        pg.draw.rect(self.screen,WHITE,outline_rect,2)

    def draw_lives(self,x,y,lives,img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30*i
            img_rect.y = y
            self.screen.blit(img,img_rect)

    # 创建敌机的函数   
    def new_enemy(self):
        enemy = Enemy(self)     
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def bullet_hit_enemy(self):
        """我方子弹打中敌人的函数"""    
        # 先进行我方子弹和敌机的碰撞检测
        hits = pg.sprite.groupcollide(self.enemies,self.bullets,True,True,pg.sprite.collide_mask)
        for hit in hits:
            self.score += 50-hit.radius
            pg.mixer.Sound(sound_path+"exp.wav").play()
            #创建一个爆炸对象需要调用Explosion类
            expl = Explosion(self,hit.rect.center,'lg')
            # 将爆炸对象添加到所有精灵组
            self.all_sprites.add(expl)
            if rnd.random()> 0.9:
                pow = Power(self,hit.rect.center)
                self.all_sprites.add(pow)
                self.powers.add(pow)
            # 每消灭一个敌机，又会创建一个敌机
            self.new_enemy()
    
    # 我方飞机获取补给的方法，元素碰撞检测
    def plane_get_power(self,player):
        sound = pg.mixer.Sound(sound_path+'FX054_cut.wav')
        hits = pg.sprite.spritecollide(player,self.powers,True)
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
    def enemy_hit_me(self,player):
        hits = pg.sprite.spritecollide(player,self.enemy_bullets,True,pg.sprite.collide_mask)  
        for h in hits:
            player.shield -= h.radius *2 # 被打中会掉血
            expl = Explosion(self,h.rect.center,'sm') # 创建爆炸对象，添加到小爆炸里集合面
            self.all_sprites.add(expl) # 将爆炸对象添加到所有精灵组
            if player.shield <=0: # 血量掉光了就死掉了
                pg.mixer.Sound(sound_path+'exp.wav').play() #播放爆炸音效
                dead_expl = Explosion(self,player.rect.center,'player')
                self.all_sprites.add(dead_expl)
                player.hide() # 调用这个方法后几秒钟就会显示player
                player.lives -= 1 # 死掉了，就要减少一条命
                player.shield = 100 # 把player的血量设置位100，那么他就相当于新创建的了

    # 我方飞机和敌机的碰撞检测
    def plane_crash(self,player):
        hits = pg.sprite.spritecollide(player,self.enemies,True,pg.sprite.collide_mask)
        for hit in hits:
            pg.mixer.Sound(sound_path+"exp.wav").play()
            #创建一个爆炸对象需要调用Explosion类
            expl = Explosion(self,hit.rect.center,'lg')
            # 将爆炸对象添加到所有精灵组
            self.all_sprites.add(expl)  
            if rnd.random()> 0.9:
                pow = Power(self,hit.rect.center)
                self.all_sprites.add(pow)
                self.powers.add(pow)
            # 每消灭一个敌机，又会创建一个敌机
            self.new_enemy()

    #创建熔岩碎石
    def new_lava(self):
        if rnd.random() >= 0.6:
            lava = Lava(self)
            self.all_sprites.add(lava)
            self.lavas.add(lava)

    # 子弹到熔岩碎石的碰撞检测，应该双方的子弹都功能打熔岩
    def bullet_hit_lava(self):
        hits = pg.sprite.groupcollide(self.bullets,self.lavas,True,True,pg.sprite.collide_mask) 
        for hit in hits:
            expl = Explosion(self,hit.rect.center,'lg')   
            self.all_sprites.add(expl)
            self.new_lava()
        hits = pg.sprite.groupcollide(self.enemy_bullets,self.lavas,True,True,pg.sprite.collide_mask) 
        for hit in hits:
            expl = Explosion(self,hit.rect.center,'lg')   
            self.all_sprites.add(expl)
            self.new_lava()

    # 熔岩碎石撞击双方飞机，我方是单人玩家，没有玩家精灵组
    def lava_hit_both_planes(self,player):
        hits = pg.sprite.spritecollide(player,self.lavas,True,pg.sprite.collide_mask) 
        for hit in hits:
            expl = Explosion(self,hit.rect.center,'sm')   
            self.all_sprites.add(expl)
            player.shield -= hit.radius
        for enemy in self.enemies:        
            hits = pg.sprite.spritecollide(enemy,self.lavas,True,pg.sprite.collide_mask) 
            for hit in hits:
                expl = Explosion(self,hit.rect.center,'lg')   
                self.all_sprites.add(expl)
                enemy.kill()
                self.new_enemy()    

    # 双方子弹的碰撞检测
    def bullet_vs_enemy_bullet(self):
        hits = pg.sprite.groupcollide(self.bullets,self.enemy_bullets,True,True,pg.sprite.collide_mask)  
        for hit in hits:
            expl = Explosion(self,hit.rect.center,'sm')   
            self.all_sprites.add(expl)     

    def main_menu(self):
        #加载菜单音乐
        pg.mixer.music.load(sound_path + 'tgfcoder-FrozenJam-SeamlessLoop.ogg')
        #循环播放菜单音乐
        pg.mixer.music.play(-1)

        # 加载开始图片
        start_img = pg.image.load(pic_path+'menu.png')
        start_img = pg.transform.scale(start_img,SIZE)
        self.screen.blit(start_img,(0,0))
        pg.display.update()

        while True:
            event = pg.event.poll() # 只获取一个事件
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN: # 回车键
                    break
            elif  event.type == pg.QUIT:
                pg.quit()
                quit() 
            else: 
                self.draw_text("Press [Enter] To Begin",30,WIDTH/2,HEIGHT/2)    
                self.draw_text("[↑]",30,WIDTH/2,2*HEIGHT/3-40)    
                self.draw_text("[←] [↓]  [→] ",30,WIDTH/2,2*HEIGHT/3)     
                pg.display.update()      
                
        pg.display.update()
    
    def menu_display(self):
        self.main_menu()
       

if __name__ == '__main__':
   g = Game()
   g.menu_display()
   while g.running:
       g.new()
       g.exit_or_replay()
   pg.quit()
   sys.exit()    

        