# 第10个版本，我方受伤
import sys
from constants import *
import menu
from plane import *
from funcs import *

screen = pg.display.set_mode(SIZE)
pg.display.set_caption("飞机大战")
clock = pg.time.Clock()

def main():
    # 1.显示启动画面
    menu.menu_display(screen) # 调用menu模块的显示菜单方法
    # 2.精灵组可以直接使用constants模块里面的all_sprites和bullets
    # 3.创建玩家飞机
    player1 = Plane(player_img1,WIDTH/2,HEIGHT-30,pg.K_LEFT,pg.K_RIGHT,pg.K_UP,pg.K_DOWN)
    # 4.将他们添加到精灵组,这是必须的，因为只有精灵组才有绘制方法
    all_sprites.add(player1)
   
    # 创建敌机
    for i in range(4):
        new_enemy() # 这个方法可以创建敌机并且添加到all_sprites和enemies精灵组里面
    # 调用精灵组的更新方法
    all_sprites.update()
    

    global height
    running = True
    while running: # 游戏主循环
    
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        # 背景图片向下滚动        
        screen.blit(bg,(0,height))
        height += 2
        if height > -168:
            height = -936
        all_sprites.update()       # 调用精灵组的更新方法
                 # 调用精灵组的更新方法
        all_sprites.draw(screen)   # 绘制精灵
        bullet_hit_enemy() # 子弹打中敌人的碰撞检测
        plane_get_power(player1) #我方飞机获取补给的碰撞检测
        enemy_hit_me(player1)    #敌机子弹打中我方飞机
        draw_screen_text(screen,player1) # 绘制血条和飞机架数
        
        pg.display.update()
        

    pg.quit()
    sys.exit()
if __name__ == '__main__':
    main()    


