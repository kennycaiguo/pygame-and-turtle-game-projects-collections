import sys
import pygame as pg

img = pg.image.load('./sprite.png')
sub_img = pg.Surface.subsurface(img,(0,220,391,220)) # pygame的切图方法
win = pg.display.set_mode((800,600))
pg.display.set_caption("spritesheet test")
clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    win.fill((255,255,255))
    # win.blit(img,(0,0))
    win.blit(sub_img,(100,100))
    pg.display.update()
    clock.tick(30)

pg.quit()
sys.exit()
