from os import path
import pygame as pg
from constants import *
import funcs

def main_menu(screen):
    #加载菜单音乐
    pg.mixer.music.load(sound_path + 'tgfcoder-FrozenJam-SeamlessLoop.ogg')
    #循环播放菜单音乐
    pg.mixer.music.play(-1)

    # 加载开始图片
    start_img = pg.image.load(pic_path+'menu.png')
    start_img = pg.transform.scale(start_img,SIZE)
    screen.blit(start_img,(0,0))
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
            funcs.draw_text(screen,"Press [Enter] To Begin",30,WIDTH/2,HEIGHT/2)    
            funcs.draw_text(screen,"[W] ↑",30,WIDTH/2,2*HEIGHT/3-40)    
            funcs.draw_text(screen,"[A]← [S] ↓ [D]→ ",30,WIDTH/2,2*HEIGHT/3)     
            pg.display.update()      
                
    pg.display.update()

def menu_display(screen):
    main_menu(screen)
    pg.mixer.music.stop()
    pg.mixer.music.load(sound_path+'battle.ogg')
    pg.mixer.music.set_volume(0.6)
    pg.mixer.music.play(-1)