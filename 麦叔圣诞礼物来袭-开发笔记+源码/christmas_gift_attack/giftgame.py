import turtle as t
import random as rnd
import simpleaudio as sa


pic_path = './res/images/'
sound_path = './res/sounds/'

# 注册图片到turtle库
t.register_shape(pic_path+'boy.gif')
t.register_shape(pic_path+'gift1.gif')
t.register_shape(pic_path+'gift2.gif')
t.register_shape(pic_path+'gift3.gif')
t.register_shape(pic_path+'zd.gif') # 炸弹

# 加载音效文件
dead = sa.WaveObject.from_wave_file(sound_path+'dead.wav')
yeah = sa.WaveObject.from_wave_file(sound_path+'yeah.wav')

game = t.Screen() #创建游戏窗口
game.bgpic(pic_path+'bg.gif') #设置背景图片
game.setup(900,650) #设置窗口大小
game.title('圣诞礼物来袭')
game.tracer(0) ##停止默认刷新

score = 0
lives = 3

def create_pen(x,y,color):
    pen = t.Turtle()
    pen.ht()
    pen.up()
    pen.speed(0)
    pen.goto(x,y)
    pen.color(color)
    return pen
#显示分数和命数
pen = create_pen(-400,265,'yellow')
pen.clear()
pen.write('score :{} lives:{}'.format(score,lives),font=('Arial',20,'bold'))

boy = t.Turtle() #创建小男孩
boy.shape(pic_path+'boy.gif')
boy.speed(0)
boy.ht() # 先隐藏
boy.up()
boy.goto(0,-250)
boy.st() # 移动号了再显示
fx = '||' # R 表示右边 L表示左边 ||b表示站立，此时boy不会动
boy_speed =3

def to_left():
    global fx
    global boy_speed 
    if fx == "L":
        boy_speed += 1 #boy_speed = boy_speed + 1
    else:
        fx = "L"
        boy_speed = 3

def to_right():
    global fx
    global boy_speed
    if fx == "R": #如果当前就是这个方向，就让他的速度慢慢加快
        boy_speed += 1 #boy_speed = boy_speed + 1
    else:
        fx = "R"
        boy_speed = 3 #如果当前不是这个方向，把他设置为这个方向并且把速度重置为3，要不然速度就会变得太快了

def stand():   # 停止运动的方法
    global boy_speed
    global fx
    boy_speed = 0
    fx = '||'
    


def make_gifts(shape,num): #创建多个礼物的方法
    gift_list = []
    for i in range(num):
        g = t.Turtle()
        g.ht()
        g.shape(shape)
        g.up()
        g.goto(rnd.randint(-410,410),rnd.randint(0,300))
        g.fall_speed = rnd.randint(1,3) # 添加下落速度属性
        g.st()
        gift_list.append(g)

    return gift_list    

gift1_list = make_gifts(pic_path+'gift1.gif',6)
gift2_list = make_gifts(pic_path+'gift2.gif',4)
gift3_list = make_gifts(pic_path+'gift3.gif',5)

# 创建炸弹
zd_list  = make_gifts(pic_path+'zd.gif',4)

# 礼物下落方法，捡到礼物会加分
def gifts_fall(gift_list,gscore):
    global score
    for g in gift_list:
        g.sety(g.ycor() - g.fall_speed)
        if g.ycor() < - 325:
           g.sety(300) 
        if g.distance(boy) < 40: #如果礼物和男孩的距离小于40，我们就认为男孩接到礼物了，需要加分
           score += gscore
           g.sety(300) #重置礼物的位置
           yeah.play() #播放接收成功音效
           #修改分数
           pen.clear()
           pen.write('score :{} lives:{}'.format(score,lives),font=('Arial',20,'bold')) 
               

# 炸弹下落方法，捡到炸弹要扣分扣命的
def zds_fall(zd_list):
    global lives,gameOver
    for d in zd_list:
        d.sety(d.ycor() - d.fall_speed) # 下落
        if d.ycor() < - 325: # 超出边界处理
           d.sety(300) 
        # 接到炸弹致命
        if d.distance(boy) < 40:   
            dead.play() #播放炸死音效
            lives -= 1 # 死掉一个生命值减去1
            d.sety(300) #重置炸弹位置
            if lives == 0: # 命数等于0，说明死光了，游戏需要结束
               pen.clear()
               pen.write('score :{} lives:{}'.format(score,0),font=('Arial',20,'bold'))
               pen2 = create_pen(-100,0,'red')
               pen2.write('Game Over',font=('Arial',30,'bold'))
               gameOver = True # 把游戏结束标记设置为True，游戏就退出
               

    
#事件监听
game.listen()
game.onkey(to_left,'Left')
game.onkey(to_right,'Right')
game.onkey(stand,'space')

gameOver = False
while True:
    if gameOver:
      break
    game.update() #自主刷新界面
    if fx == 'L':
       x = boy.xcor()
       x -= boy_speed
       if x < -420: # 越界处理
          x=-420
       boy.setx(x)
      
    elif fx == 'R':
         x = boy.xcor()
         x += boy_speed
         if x > 420: # 越界处理
            x= 420
         boy.setx(x)
    #礼物下落     
    gifts_fall(gift1_list,3)
    gifts_fall(gift2_list,5)
    gifts_fall(gift3_list,10)
    #炸弹下落
    zds_fall(zd_list)

game.mainloop()