#小五义 http://www.cnblogs.com/xiaowuyi
import pygame,sys
pygame.init()
clock = pygame.time.Clock()
class ball(pygame.sprite.Sprite):
    def __init__(self,position,vy,vx):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/ball.PNG")
        self.rect=self.image.get_rect()
        self.rect.topleft=position
        self.vx=vx
        self.vy=vy
    def move(self):
        self.rect.y+=self.vy
        #self.rect=self.rect.move([self.vx,self.vy])
        if self.rect.y<0:
            self.kill()
screen=pygame.display.set_mode([640,480])
screen.fill([255,255,255])
locations=([150,200],[350,360],[250,280])
balls=pygame.sprite.Group()
#for lo in locations:
#    balls.add(ball(lo,-7,0))
balls.add(ball([350,360],-7,0))
i0=0
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    #balls.add(ball([350,360],-7,0))
    if i0>5:
        balls.add(ball([350,360],-7,0))
        i0=0
    i0+=1
    clock.tick(60)
    screen.fill([255,255,255])
    for list in balls.sprites():
        list.move()
        screen.blit(list.image,list.rect)
    pygame.display.update()