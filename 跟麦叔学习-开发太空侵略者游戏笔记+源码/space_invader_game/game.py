from func import *

# 创建游戏窗口
game_win = turtle.Screen()
# 设置窗口大小
game_win.setup(600,600)
#设置窗口标题
game_win.title("Space Invader Game")
# 设置背景图片
game_win.bgpic(pic_path+'bg1.png')

#给turtle图片库添加图片
turtle.addshape(pic_path+'player.gif')
# 创建玩家，它其实是一个Turtle类的对象
# player = turtle.Turtle()
player.ht() #先隐藏玩家
# 给玩家设置属性
player.speed(0)
player.up() # 把笔尖抬起来，避免绘制一条直线
# 给玩家设置图片
player.shape(pic_path+'player.gif')
player.setpos(0,-250)
# 把属性都设置好了就显示
player.st() #显示玩家
# 玩家移动
#1.开启turtle库的监听功能
turtle.listen()
# 按下←键的处理
turtle.onkey(goLeft,'Left') # goLeft是自定义函数，在func.py模块里面定义
# 按下→键的处理
turtle.onkey(goRight,'Right') # goRight是自定义函数，在func.py模块里面定义
# 创建子弹，这个版本的游戏只有一颗子弹
create_bomb()

# 添加游戏得分显示
show_score(pen,score)

# 当用户按下空格键时发发射子弹
turtle.onkey(fire,'space')

# 调用创建敌人的方法
create_enemies()
# 游戏主要业务逻辑：让敌人动起来，子弹打中敌人，加分等等功能
game_proc()
# 游戏主循环
game_win.mainloop() 

