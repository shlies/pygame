# -*- coding: utf8 -*-

background_image_filename = 'background.jpg'
mouse_image_filename = 'img.png'
#指定图像文件名称
 
import pygame #导入pygame库
from sys import exit #向sys模块借一个exit函数用来退出程序
 
pygame.init() #初始化pygame,为使用硬件做准备
screen = pygame.display.set_mode((480, 650), 0, 32)
#创建了一个窗口
pygame.display.set_caption("Test!")
#设置窗口标题
 
background = pygame.image.load(background_image_filename).convert()
mouse_curso = pygame.image.load(mouse_image_filename).convert_alpha()
mouse_cursor = pygame.transform.scale(mouse_curso, (60, 80))
pygame.mouse.set_visible(False)
#加载并转换图像
while True:
#游戏主循环
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #接收到退出事件后退出程序
            pygame.quit()
            exit()
 
    screen.blit(background, (0,0))
    #将背景图画上去
 
    x, y = pygame.mouse.get_pos()
    #获得鼠标位置
    x-= mouse_cursor.get_width() / 2
    y-= mouse_cursor.get_height() / 2
    #计算光标的左上角位置
    screen.blit(mouse_cursor, (x, y))
    #把光标画上去
 
    pygame.display.update()
    #刷新一下画面
