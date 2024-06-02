import pygame as pg
from os import path

pg.init()       #初始化pygame模块
pg.mixer.init() #初始化pygame模块的音效模块
font_name = pg.font.match_font('arial') # 获取系统里面安装了的字体名称

# 实战图片和音效图片路径
pic_path = './res/images/'
sound_path = './res/sounds/'

WIDTH = 480      #窗口宽度
HEIGHT = 600     #窗口高度 
SIZE = (WIDTH,HEIGHT) #

FPS = 30   # 帧率

# 定义颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

bg = pg.image.load(pic_path+'startfield.jpg')
bg = pg.transform.scale(bg,(WIDTH,1536))
height = -936

POWERUP_TIME = 5000  #飞机的火力持续时间

# 所有精灵的精灵组
all_sprites = pg.sprite.Group()
# 我方子弹精灵组
bullets = pg.sprite.Group()
# 敌机精灵组
enemies = pg.sprite.Group()
# 敌人子弹精灵组
enemy_bullets = pg.sprite.Group()
# 补给精灵组
powers = pg.sprite.Group()
# 玩家精灵组
players = pg.sprite.Group()


# 分数
score = 0

BAR_LENGTH =100  #血条长度
BAR_HEIGHT = 10  #血条高度