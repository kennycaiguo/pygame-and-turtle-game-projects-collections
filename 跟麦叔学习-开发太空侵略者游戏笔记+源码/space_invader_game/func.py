# 定义一些函数
import turtle
import random
import simpleaudio as sa

pic_path = './resource/images/'     #图片文件夹路径
sound_path = './resource/sounds/'   #音效文件路径
player = turtle.Turtle()
player_step = 15

num = 6 #敌人数量
inv_list = [] # 敌人列表
bomb = None
is_fired = False
score = 0 #游戏得分
pen = turtle.Turtle() # 用来写分数的笔对象
game_over = False

#创建发射子弹和爆炸的音效
laser = sa.WaveObject.from_wave_file(sound_path+'laser.wav')         # 发射子弹
explosion = sa.WaveObject.from_wave_file(sound_path+'explosion.wav') # 爆炸的音效

#创建敌人的方法
def create_enemies():
    turtle.addshape(pic_path+'inv.gif') # 添加敌人图片到turtle库
    for i in range(num):
        inv = turtle.Turtle()
        # 隐藏敌人
        inv.ht() 
        # 设置敌人属性
        inv.speed(0)
        inv.up() # 使他移动时不会绘制直线
        inv.shape(pic_path+'inv.gif')
        # 利用随机数计算敌人出现的位置
        x = random.randint(-200,200)
        y = random.randint(100,200)
        inv.setpos(x,y)
        inv.st() # 显示敌人
        inv_list.append(inv) # 把敌人添加到敌人列表

# 玩家往左移动
def goLeft():
    # print("moving left...")
    x = player.xcor() #获取玩家当前的坐标
    x -= player_step # 把它的坐标减去移动步长，因为往左边所有是减
    # 越界处理
    if x < -250:
        x= -250
    player.setx(x) # 重新设置玩家的x坐标，就实现了水平运动

# 玩家往右移动
def goRight():
    # print("moving left...")
    x = player.xcor() #获取玩家当前的坐标
    x += player_step # 把它的坐标减去移动步长，因为往左边所有是减
    # 越界处理
    if x > 250:
        x= 250
    player.setx(x) # 重新设置玩家的x坐标，就实现了水平运动


# def enemy_move():
#游戏主逻辑函数，实现敌人和子弹移动，子弹打中敌人，和加分功能
def game_proc(): 
    global bomb,is_fired,score,pen,game_over
    inv_step = 2 # 左右移动步长
    sink_step = 40 # y轴下沉步长，注意turtle是使用数学坐标系而不是屏幕坐标系
    go_back = False
    # 敌人是组件运动的需要一个循环来实现
    while True:
        if game_over: #如果这个标志位True，就需要终止循环
            # 在屏幕中间显示：Game Over
            over_pen = turtle.Turtle()
            over_pen.color('red')
            over_pen.up()
            over_pen.ht()
            over_pen.write('Game Over',align='center',font=('Arial',18,'bold'))
            explosion.play() # 游戏结束相当于大本营给炸了，有需要播放爆炸音效
            break

        bomb_step = 20 # 子弹位移
        for inv in inv_list:
            x = inv.xcor()
            x += inv_step
            inv.setx(x)
            # 越界处理
            if x > 250 or x < -250:
                # 往反方向动
                go_back = True
            # 用距离来判断敌人是否中弹
            if inv.distance(bomb) < 15: # 如果距离小于15，我们就认为子弹打中敌人
                # 打中后处理
                #1.把敌人复位到尽量靠上面
                inv.setpos(0,285)
                # 播放爆炸音效
                explosion.play()
                # 2.把is_fired设置为False这样子才能继续发射子弹
                is_fired = False
                # 3.重置子弹的位置并且隐藏子弹
                bomb.setpos(-300,-300)
                bomb.ht()
                # 更新分数并且显示
                score += 10
                show_score(pen,score)
            # 判断游戏是否结束
            if inv.ycor() < -280:
               game_over = True 

        if go_back:
            inv_step = inv_step * -1  
            go_back = False      
            # 碰到我们设置的限定边界需要往下沉
            for inv in inv_list:
                y = inv.ycor()
                y -= sink_step
                inv.sety(y)  

        if is_fired: #如果is_fired为True，子弹需要动
           y = bomb.ycor() 
           y += bomb_step
           bomb.sety(y)
           # 子弹飞出边界，需要把is_fired设置为False
           if y > 250:
               is_fired = False
               # 重新设置子弹位置
               bomb.setpos(-300,-300)
               bomb.ht() # 把子弹隐藏


def create_bomb():
    global bomb
    bomb = turtle.Turtle()
    bomb.ht()
    bomb.up()
    bomb.speed(0)
    bomb.shape('triangle') # 使用turtle库自带的图片
    bomb.color('yellow') # 设置颜色
    bomb.shapesize(0.5,0.5) # 设置子弹尺寸
    bomb.seth(90)
    


def fire(): # 发射子弹功能
    global bomb,is_fired,laser
    if not is_fired: # 设置不能连续发射，因为这样子视觉效果不好，子弹发射出去又被拉回来。
        bomb.setpos(player.xcor(),player.ycor()+20) # 把子弹移动到玩家飞机的上方
        bomb.st()
        is_fired = True
        # 播放音效
        laser.play()

# 显示游戏得分的函数
def show_score(pen,score):
    pen.color('white')
    pen.speed(0)
    pen.up()
    pen.ht() #笔不需要显示
    pen.setpos(-270,255)
    pen.clear() # 在写新分数之前，需要去除旧分数，否则两个分数重叠在一起
    pen.write(f"得分：{score}",align='left',font=("Arial",14,'normal'))