background_image_filename = 'img/background.jpg'
mouse_image_filename = 'img/ball.png'
bullet_image_filename = 'img/ball.png'
#指定图像文件名称
 
import pygame #导入pygame库
import random
from sys import exit #向sys模块借一个exit函数用来退出程序
 
pygame.init() #初始化pygame,为使用硬件做准备
screen = pygame.display.set_mode((480, 650), 0, 32)
#创建了一个窗口
pygame.display.set_caption("Tset!")
#设置窗口标题
pygame.mouse.set_visible(False)
 
background = pygame.image.load(background_image_filename).convert()
mouse_curso = pygame.image.load(mouse_image_filename).convert_alpha()
mouse_cursor = pygame.transform.scale(mouse_curso, (60, 80))
bullet = pygame.image.load(bullet_image_filename).convert_alpha()
#加载并转换图像

bullet_x, bullet_y = 10, 100 #初始化子弹坐标

g=0.003
vx=0#random.randint(-2,2)
vy=0#random.randint(-2,2)
while True:
#游戏主循环
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #接收到退出事件后退出程序
            pygame.quit()
            exit()
 
    screen.blit(background, (0,0))
    screen.blit(bullet, (bullet_x,bullet_y))
    #将背景图画上去
    keys_pressed = pygame.key.get_pressed()
    #获得鼠标位置
    if bullet_y>650 : #移动子弹
        #bullet_x, bullet_y = x, -y
        vy=0-vy
        bullet_y +=vy
    if   bullet_y<2: #移动子弹
        #bullet_x, bullet_y = x, -y
        vy=0
        bullet_y -=2
    if bullet_x>480 or  bullet_x<0: #移动子弹
        #bullet_x, bullet_y = x, -y
        vx=0-vx
        bullet_x +=vx
    else:
        bullet_y +=vy
        bullet_x +=vx
        vy+=g
    if vy>0:
        vy-=0.001
    elif vy<0:
        vy+=0.001
    if vx>0:
        vx-=0.001
    elif vx<0:
        vx+=0.001
    if keys_pressed[pygame.K_UP] and bullet_y>=640 :
            vy+=0.3
    if keys_pressed[pygame.K_LEFT] and bullet_x>0:
            vx-=0.004
    if keys_pressed[pygame.K_RIGHT] and bullet_x<860:
       vx+=0.004
    #把光标画上去
 
    pygame.display.update()
    #刷新一下画面

