import sys
import pygame as pg

img = pg.image.load('./sprite.png')
sub_img_list = []
xs = [0,391]
ys = [0,220,440,660]
region = (0,0,391,220)
# i = 1
for y in ys:
    for x in xs:
        sub_img = pg.Surface.subsurface(img,(x,y,391,220)) # pygame的切图方法
        # pg.image.save(sub_img,"./cutted/gocu%d.png" % i)
        # i += 1
        sub_img_list.append(sub_img)
sub_img = pg.Surface.subsurface(img,(0,880,391,220)) #保存最后一个小图
sub_img_list.append(sub_img)
# pg.image.save(sub_img,"./cutted/gocu9.png")        
win = pg.display.set_mode((800,600))
pg.display.set_caption("spritesheet test")
clock = pg.time.Clock()

running = True
index = 0
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    win.fill((255,255,255))
    # win.blit(img,(0,0))
    win.blit(sub_img_list[index],(100,100))
    if index < 8:
        index +=1
    else:
        index = 0    
    pg.display.update()
    clock.tick(10)

pg.quit()
sys.exit()
