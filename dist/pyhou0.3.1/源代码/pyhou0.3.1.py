#
#请先使用 
#pip install pygame-2.0.1-cp36-cp36m-win_amd64.whl
#指令安装pygame库！！！
'''
to do:
函数轨迹
吃P点范围扩大
'''
import pygame,sys,random,math
pygame.init()
clock = pygame.time.Clock()
score=0
i4=0
def vdig(v,dig):
    return[v*math.sin(dig/360*2*math.pi),v*math.cos(dig/360*2*math.pi)]
def word(position,words,size,color=(255,255,255)):
    text=pygame.font.Font("ttc/msyh.ttc",size)
    textprint=text.render(words,1,color)
    screen.blit(textprint,position)
    return text.get_linesize()
def lists(position=[0,0],tab=["",""],size=10):
    i=0
    f=1
    time=0
    #global clock
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        #clock.tick(30)
        time+=1
        keys_pressed = pygame.key.get_pressed()
        j=0
        posi=[0+position[0],0+position[1]]
        if f==1:
            for lis in tab:
                if j==i:
                    hight=word(posi,lis, size,(255,0,0))
                else:
                    hight=word(posi,lis, size)
                posi[1]+=int(hight*1.2)
                j+=1
            f=0
        if keys_pressed[pygame.K_DOWN] and time>220:
            i+=1
            f=1
            time=0
        if keys_pressed[pygame.K_UP] and time>220:
            i-=1
            f=1
            time=0
        if i>len(tab)-1:
            i=0
        if i<0:
            i=len(tab)-1
        if keys_pressed[pygame.K_RETURN]:
            return i
        
        pygame.display.update()
        
        pygame.event.pump()

def load(position,time):
    global clock
    loading = pygame.image.load("img/loading.PNG")#screen.blit(background, (0,0))
    while True:
        clock.tick(100)
        time-=1
        if time<0:
            break
        screen.blit(loading,position)
        pygame.display.update()

class ball(pygame.sprite.Sprite):
    def __init__(self,position,vy,vx):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/ball.PNG")
        self.rect=self.image.get_rect()
        self.rect.topleft=position
        self.vx=vx
        self.vy=vy
    def move(self):
        self.rect=self.rect.move([self.vx,self.vy])
        if self.rect.y<0:
            self.kill()
class image(pygame.sprite.Sprite):
    def __init__(self,sprite,img,change):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(img)
        self.rect=self.image.get_rect()
        self.rect.center=sprite.rect.center
        self.sprite=sprite
        self.change=change
        self.time=1
    def move(self):
        self.rect.center=self.sprite.rect.center
        '''if change>0:
            self.time+=1
            if self.time>self.change:
                self.time=0
            self.image=self.image+str(self.change)+".gif"'''
        screen.blit(self.image,self.rect)
class enball(pygame.sprite.Sprite):
    def __init__(self,position,vy=0.0,vx=0.0):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/enball1.PNG")
        self.rect=self.image.get_rect()
        self.rect.center=position
        self.vx=vx
        self.vy=vy
    def move(self):
        global enballs
        self.rect.x+=self.vx
        self.rect.y+=self.vy
        if pygame.sprite.collide_rect(self,ling)>0:
            ling.life-=1
            ling.rect.center=[350,420]
            for list in enballs.sprites():
                list.kill()
            self.kill()
        elif self.rect.y<=0 or self.rect.y>=510 or self.rect.x<=0 or self.rect.x>=670:
            self.kill()
class p(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/p.PNG")
        self.rect=self.image.get_rect()
        self.rect.topleft=position
    def move(self):
        global ling,score
        self.rect=self.rect.move([0,1.5])
        if pygame.sprite.collide_rect(self,ling)>0:
            ling.power+=1
            score+=1
            self.kill()
        elif self.rect.y<0:
            self.kill()
class player(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/ball.png")
        self.rect=self.image.get_rect()
        self.rect.topleft=position
        self.power=1
        self.life=5
        self.bomb=3
        self.time=4
    def move(self):
        global balls,key_pressed
        self.time+=1
        if self.time>4 and keys_pressed[pygame.K_z] :
            if self.power<=30:
                balls.add(ball([self.rect.x,self.rect.y-7],-15,0))
            elif 30<self.power<=50:
                balls.add(ball([self.rect.x-10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x+10,self.rect.y-7],-15,0))
            elif 50<self.power<=70:
                balls.add(ball([self.rect.x-10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x+10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x-20,self.rect.y-7],-15,-4))
                balls.add(ball([self.rect.x+20,self.rect.y-7],-15,4))
            elif 70<self.power:
                balls.add(ball([self.rect.x,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x-10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x+10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x-20,self.rect.y-7],-15,-4))
                balls.add(ball([self.rect.x+20,self.rect.y-7],-15,4))
            self.time=0
        if keys_pressed[pygame.K_LEFT] and self.rect.x>10:
            self.rect.x-=3*(2-int(keys_pressed[pygame.K_LSHIFT]))
        if keys_pressed[pygame.K_RIGHT] and self.rect.x<610:
            self.rect.x+=3*(2-int(keys_pressed[pygame.K_LSHIFT]))
        if keys_pressed[pygame.K_UP] and self.rect.y>10:
            self.rect.y-=3*(2-int(keys_pressed[pygame.K_LSHIFT]))
        if keys_pressed[pygame.K_DOWN] and self.rect.y<450:
            self.rect.y+=3*(2-int(keys_pressed[pygame.K_LSHIFT]))
class mob1(pygame.sprite.Sprite):
    def __init__(self,position,vy,vx):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/mob1.PNG")
        self.rect=self.image.get_rect()
        self.rect.topleft=position
        self.vx=vx
        self.vy=vy
        self.life=2
    def move(self):
        global balls,score
        self.rect=self.rect.move([self.vx,self.vy])
        self.life-=len(pygame.sprite.spritecollide(self,balls,True))
        if self.life<=0:
            balls.add(p([self.rect.x+random.randint(-10,10),self.rect.y+random.randint(-10,10)]))
            balls.add(p([self.rect.x+random.randint(-10,10),self.rect.y+random.randint(-10,10)]))
            score+=10
            self.kill()
        elif self.rect.y>480:
            self.kill()
class mob2(pygame.sprite.Sprite):
    def __init__(self,position,vy,vx,skip,num):
        global score
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/mob2.PNG")
        self.rect=self.image.get_rect()
        self.rect.bottomright=[300,-70]
        self.position=position
        self.vx=vx
        self.vy=vy
        self.life=15+score/200
        self.time=1
        self.skip=skip
        self.num=num
        self.kil=0
    def move(self):
        global balls,score
        self.rect=self.rect.move([self.vx,self.vy])
        self.life-=len(pygame.sprite.spritecollide(self,balls,True))
        self.time+=1
        self.kil+=1
        if self.rect.x!=self.position[0]:
            self.rect.x+=(self.position[0]-self.rect.x)/4
        if self.rect.y!=self.position[1]:
            self.rect.y+=(self.position[1]-self.rect.y)/4

        if self.time>self.skip:
            self.time=0
            if self.num>=4:
                enballs.add(enball([self.rect.x,self.rect.y],2*(ling.rect.x-self.rect.x)/math.sqrt((ling.rect.x-self.rect.x)**2+(ling.rect.y-self.rect.y)**2),2*(ling.rect.y-self.rect.y)/math.sqrt((ling.rect.x-self.rect.x)**2+(ling.rect.y-self.rect.y)**2)))
                #print(self.rect.x,self.rect.y,ling.rect.x,ling.rect.y,ling.rect.x-self.rect.x,ling.rect.y-self.rect.y,2*(ling.rect.x-self.rect.x)/math.sqrt((ling.rect.x-self.rect.x)**2+(ling.rect.y-self.rect.y)**2),2*(ling.rect.y-self.rect.y)/math.sqrt((ling.rect.x-self.rect.x)**2+(ling.rect.y-self.rect.y)**2))
            for ine in range(self.num):
                enballs.add(enball([self.rect.x,self.rect.y],vdig(2,ine*360/self.num+45)[0],vdig(2,ine*360/self.num+45)[1]))
        if self.life<=0:
            for ine in range(4):
                balls.add(p([self.rect.x+random.randint(-10,10),self.rect.y+random.randint(-10,10)]))
            score+=30
            self.kill()
        elif self.rect.y>480 or self.kil>3600:
            self.kill()
def how():
    background = pygame.image.load("img/background.jpg").convert()
    screen.blit(background, (0,0))
    h1=word([10,10],"游戏说明：",30)*1.5
    word([10,10+h1],"上下左右      操作自机方向",50)
    word([10,10+2*h1],"Z键             射击",50)
    word([10,10+3*h1],"Shift键 低速移动，显示判定点",40)
    word([10,10+4*h1],"ESC键暂停游戏",50)
    word([10,10+5*h1],"ESC键退出",30)
    pygame.display.update()
    while 1:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            break
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.event.pump()
def about():
    background = pygame.image.load("img/background.jpg").convert()
    screen.blit(background, (0,0))
    word([10,10],"关于：Pyhou0.3.0试玩版",30)
    word([10,50],"本游戏不定期更新",50)
    word([10,130],"作者很菜，还请不要在意",50)
    word([10,210],"思路及部分素材来自 东方辉针城",40)
    word([10,290],"ESC键退出",30)
    pygame.display.update()
    while 1:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            break
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.event.pump()
        


    

screen=pygame.display.set_mode([640,480])
background = pygame.transform.scale(pygame.image.load("img/background.jpg").convert(), (940,480)) #pygame.image.load("img/background.jpg").convert()
screen.blit(background, (0,0))
#screen.fill([255,255,255])
balls=pygame.sprite.Group()
mobs=pygame.sprite.Group()
enballs=pygame.sprite.Group()
ling=player([350,420])
lingimg=image(ling,"img\ling.png",10)
i1=0
i2=0
pygame.display.update()
#pygame.time.delay(5000)
choice=-1
while 1:
    screen.blit(background, (0,0))
    choice=lists([0,300],["开始游戏","游戏说明","关于"],30)
    if choice==0:
        break
    if choice==1:
        how()
    if choice==2:
        about()
load([400,350], 200)
background = pygame.transform.scale(pygame.image.load("img/stage1.png").convert(), (640,480)) 
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    i1+=1
    i2+=1
    if i1>math.log(score+10,2):
        i1=0
        mobs.add(mob1([random.randint(250,400),random.randint(-20,20)],random.randint(2,4),random.randint(-4,4)))
    if i2>30000/(score+1)+100:
        i2=0
        mobs.add(mob2([random.randint(80,600),random.randint(40,250)],0,0,70000/score+20,int(math.log(score/10+1,3))))

    clock.tick(60)
    screen.blit(background, (0,0))
    #screen.fill([255,255,255])
    keys_pressed = pygame.key.get_pressed()
    for list in balls.sprites():
        list.move()
        screen.blit(list.image,list.rect)
    for list in mobs.sprites():
        list.move()
        screen.blit(list.image,list.rect)
    for list in enballs.sprites():
        list.move()
        screen.blit(list.image,list.rect)
    ling.move()
    lingimg.move()
    screen.blit(lingimg.image,lingimg.rect)
    if keys_pressed[pygame.K_LSHIFT]:
        screen.blit(ling.image,ling.rect)
    word([10,10],"得分:"+str(score),30)
    word([10,38],"剩余命数:"+str(ling.life),30)
    word([10,68],"火力:"+str(ling.power),30)
    if keys_pressed[pygame.K_ESCAPE]:
        while 1:
            screen.blit(background, (0,0))
            #keys_pressed = pygame.key.get_pressed()
            #pygame.display.update()
            choice=-1
            choice=lists([0,200],["继续游戏","游戏说明","关于","退出"],30)
            if choice==0:
                break
            if choice==1:
                how()
            if choice==2:
                about()
            if choice==3:
                pygame.quit()
                sys.exit()
            screen.blit(background, (0,0))
            pygame.display.update()
            pygame.event.pump()
    pygame.display.update()
    if ling.life<=0:
        pygame.quit()
        sys.exit()
