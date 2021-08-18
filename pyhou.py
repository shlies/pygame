'''
to do:
函数轨迹
符卡
火力收束
stage（SSSS）
'''
import pygame,sys,random,math,urllib.request,time

pygame.init()
clock = pygame.time.Clock()
score=0
i4=0
screen=pygame.display.set_mode([640,480])

background = pygame.transform.scale(pygame.image.load("img/background.jpg").convert(), (940,480)) #pygame.image.load("img/background.jpg").convert()
screen.blit(background, (0,0))
balls=pygame.sprite.Group()
mobs=pygame.sprite.Group()
enballs=pygame.sprite.Group()
bombs=pygame.sprite.Group()
i1=0
i2=0
space=0
keys_pressed=pygame.key.get_pressed()

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
        if keys_pressed[pygame.K_DOWN] and time>330:
            i+=1
            f=1
            time=0
        if keys_pressed[pygame.K_UP] and time>330:
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
def save(score,time):
    screen.blit(background, (0,0))
    word([10,10],"得分："+str(score)+" 用时："+str(int(time)),40,(0,0,0))
    word([10,70],"请在命令行界面输入保存时使用的用户名",30)
    pygame.display.update()
    username=input("用户名（英文，重复使用已有名称将会覆盖原有记录）：")
    print("正在连接服务器。。。")
    header = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'} 
    i=0
    while i<5:
        try:
            request = urllib.request.Request("http://rank.wgma.pp.ua/wr.php?id="+str(username)+"&score="+str(score)+"&time="+str(int(time)),headers=header)
            reponse = urllib.request.urlopen(request).read()
        except ConnectionResetError or urllib.error.HTTPError:
            print("正在重连。。。")
            pygame.time.delay(700)
            i+=1
        else:
            result=str(reponse)
            i=10
    if i==5:
        print("无法连接服务器，请稍后再试")
    else:
        print("保存成功，请回到游戏界面")
def refresh(keys_pressed):
    global enballs,mobs,balls,ling,lingimg,spotimg,score,space
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    for list in enballs.sprites():
        list.move()
        screen.blit(list.image,list.rect)
    for list in mobs.sprites():
        list.move()
        screen.blit(list.image,list.rect)
    for list in balls.sprites():
        list.move()
        screen.blit(list.image,list.rect)
    for list in bombs.sprites():
        list.move()
        screen.blit(list.image,list.rect)
    ling.move()
    lingimg.move()
    spotimg.move()
    if ling.wudi%8<4 or ling.wudi>50:
        screen.blit(lingimg.image,lingimg.rect)
    if keys_pressed[pygame.K_LSHIFT]:
        screen.blit(spotimg.image,spotimg.rect)
        #screen.blit(ling.image,ling.rect)
    word([10,10],"得分:"+str(score),30)
    word([10,38],"残机:"+str(ling.life),30)
    word([10,68],"火力:"+str(ling.power),30)
    word([10,98],"bomb:"+str(ling.bomb),30)
    if keys_pressed[pygame.K_ESCAPE]:
        tamp1=time.time()
        while 1:
            screen.blit(background, (0,0))
            choice=-1
            choice=lists([0,250],["继续游戏","游戏说明","关于","退出"],30)
            if choice==0:
                break
            if choice==1:
                how()
            if choice==2:
                about()
            if choice==3:
                return 1
            screen.blit(background, (0,0))
            pygame.display.update()
            pygame.event.pump()
        space+=time.time()-tamp1
    pygame.display.update()
    if ling.life<=0:
        usetime=time.time()-ticks-space
        while 1:
            screen.blit(background, (0,0))
            word([100,100],"游戏结束",50,(255,0,0))
            choice=lists([0,200],["退出游戏","排行榜","保存记录","关于","游戏说明"],30)
            if choice==0:
                return 1
            elif choice==1:
                rank()
            elif choice==2:
                save(score,usetime)
            elif choice==3:
                how()
            elif choice==4:
                about()

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
class bomb(pygame.sprite.Sprite):
    def __init__(self,position,vy,vx,mode=1):
        pygame.sprite.Sprite.__init__(self)
        if mode==1:
            self.image=pygame.image.load("img/bomb.PNG")
        self.rect=self.image.get_rect()
        self.rect.topleft=position
        self.vx=vx
        self.vy=vy
        self.mode=mode
        self.time=350
        ling.wudi=350
    def move(self):
        self.time-=1
        if self.time<230:
            self.rect=self.rect.move([random.randint(-10,10),random.randint(-10,10)])
        else:
            self.rect=self.rect.move([self.vx,self.vy])
        if self.rect.y<0 or self.time<0:
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
        #screen.blit(self.image,self.rect)
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
        if pygame.sprite.collide_rect(self,ling)>0 and ling.wudi==0:
            ling.life-=1
            if ling.power>20:
                ling.power-=20
            ling.wudi=50
            ling.rect.center=[350,420]
            for list in enballs.sprites():
                list.kill()
            self.kill()
        elif self.rect.y<=0 or self.rect.y>=510 or self.rect.x<=0 or self.rect.x>=670 or len(pygame.sprite.spritecollide(self,bombs,False))>0:
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
        if ling.rect.y<170:
            self.rect.x+=(ling.rect.x-self.rect.x)/6
            self.rect.y+=(ling.rect.y-self.rect.y)/6
        if pygame.sprite.collide_rect(self,spotimg)>0:
            ling.power+=1
            score+=1
            self.kill()
        elif self.rect.y<0:
            self.kill()
class lifeup(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/lifeup.png")
        self.rect=self.image.get_rect()
        self.rect.topleft=position
    def move(self):
        global ling,score
        self.rect=self.rect.move([0,1.5])
        if ling.rect.y<170:
            self.rect.x+=(ling.rect.x-self.rect.x)/6
            self.rect.y+=(ling.rect.y-self.rect.y)/6
        if pygame.sprite.collide_rect(self,spotimg)>0:
            ling.life+=1
            self.kill()
        elif self.rect.y<0:
            self.kill()
class bombup(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/bombup.png")
        self.rect=self.image.get_rect()
        self.rect.topleft=position
    def move(self):
        global ling,score
        self.rect=self.rect.move([0,1.5])
        if ling.rect.y<170:
            self.rect.x+=(ling.rect.x-self.rect.x)/6
            self.rect.y+=(ling.rect.y-self.rect.y)/6
        if pygame.sprite.collide_rect(self,spotimg)>0:
            ling.bomb+=1
            score+=5
            self.kill()
        elif self.rect.y<0:
            self.kill()
class player(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/spot.png")
        self.rect=self.image.get_rect()
        self.rect.topleft=position
        self.power=1
        self.life=5
        self.bomb=3
        self.time=4
        self.wudi=50
    def move(self):
        global balls,key_pressed
        self.time+=1
        if self.wudi>0:
            self.wudi-=1
        if self.time>4 and keys_pressed[pygame.K_z] :
            if self.power<=30:
                balls.add(ball([self.rect.x,self.rect.y-7],-15,0))
            elif 30<self.power<=60:
                balls.add(ball([self.rect.x-10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x+10,self.rect.y-7],-15,0))
            elif 60<self.power<=120:
                balls.add(ball([self.rect.x-10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x+10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x-20,self.rect.y-7],-15,-4))
                balls.add(ball([self.rect.x+20,self.rect.y-7],-15,4))
            elif 100<self.power:
                balls.add(ball([self.rect.x,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x-10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x+10,self.rect.y-7],-15,0))
                balls.add(ball([self.rect.x-20,self.rect.y-7],-15,-4))
                balls.add(ball([self.rect.x+20,self.rect.y-7],-15,4))
            self.time=0
        if self.time>70 and keys_pressed[pygame.K_x] and self.bomb>0:
            for ine in range(8):
                bombs.add(bomb([self.rect.x-7,self.rect.y-7],vdig(2,ine*360/8+45)[0],vdig(2,ine*360/8+45)[1]))
            #bombs.add(bomb([self.rect.x,self.rect.y-7],-2,0))
            self.time=0
            self.bomb-=1
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
        self.life-=len(pygame.sprite.spritecollide(self,bombs,False))
        if pygame.sprite.collide_rect(self,ling)>0 and ling.wudi==0:
            ling.life-=1
            if ling.power>20:
                ling.power-=20
            ling.wudi=50
            ling.rect.center=[350,420]
            for list in enballs.sprites():
                list.kill()
            self.kill()
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
        self.life-=len(pygame.sprite.spritecollide(self,bombs,False))
        self.time+=1
        self.kil+=1
        if self.rect.x!=self.position[0]:
            self.rect.x+=(self.position[0]-self.rect.x)/4
        if self.rect.y!=self.position[1]:
            self.rect.y+=(self.position[1]-self.rect.y)/4
        if pygame.sprite.collide_rect(self,ling)>0 and ling.wudi==0:
            ling.life-=1
            if ling.power>20:
                ling.power-=20
            ling.wudi=50
            ling.rect.center=[350,420]
            for list in enballs.sprites():
                list.kill()
            self.kill()
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
            for i in range(random.randint(0,1)):
                balls.add(lifeup([self.rect.x+random.randint(-10,10),self.rect.y+random.randint(-10,10)]))
            for i in range(random.randint(0,1)):
                balls.add(bombup([self.rect.x+random.randint(-10,10),self.rect.y+random.randint(-10,10)]))
            score+=30
            self.kill()
        elif self.rect.y>480 or self.kil>360:
            self.kill()

def how():
    background = pygame.image.load("img/background.jpg").convert()
    screen.blit(background, (0,0))
    h1=word([10,10],"游戏说明：",30)*1.5
    word([10,10+h1],"上下左右      操作自机方向",50)
    word([10,10+2*h1],"Z键             射击",50)
    word([10,10+3*h1],"Shift键 低速移动，显示判定点",40)
    word([10,10+4*h1],"移至画面顶端收集P点，修复了碰到怪不会死的Bug",20)
    word([10,10+5*h1],"死后有短暂无敌时间，新增分数联网保存",30)
    word([10,10+6*h1],"ESC键暂停游戏",50)
    word([10,10+7*h1],"ESC键退出",30)
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
    word([10,10],"关于：Pyhou0.4.0",30)
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
def rank():
    background = pygame.image.load("img/background.jpg").convert()
    screen.blit(background, (0,0))
    i=0
    word([10,10],"正在连接服务器",40)
    load([10,60],1)
    header = {
    'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    } 
    while i<5:
        try:
            request = urllib.request.Request("http://rank.wgma.pp.ua/ls.php",headers=header)
            reponse = urllib.request.urlopen(request).read()
        except ConnectionResetError or urllib.error.HTTPError:
            print("正在重连。。。")
            pygame.time.delay(700)
            i+=1
        else:
            result=str(reponse)[2:-1].replace(".","\n")
            result=result.replace(",","    ")
            l=result.split("\n")
            i=10
    
    screen.blit(background, (0,0))
    word([10,10],"排行榜：",30)
    if i==5:
        word([10,50],"无法连接服务器，请稍后再试，ESC退出",30)
    else:
        y=70
        word([10,50],"ID     得分      用时",15)
        word([10,430],"ESC键退出",25)
        for j in l:
            h=word([10,y],j,15)
            y+=h
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

def stage1():
    global i1,i2,keys_pressed
    load([400,350], 100)
    background = pygame.transform.scale(pygame.image.load("img/stage1.png").convert(), (640,480)) 
    while True:
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
        keys_pressed = pygame.key.get_pressed()
        if refresh(keys_pressed)==1:
            return 0

ling=player([350,420])
lingimg=image(ling,"img\ling.png",10)
spotimg=image(ling,"img\spotimg.png",1)
choice=-1
while 1:
    screen.blit(background, (0,0))
    choice=lists([0,270],["开始游戏","排行榜 *新增","关于","游戏说明 *新内容"],30)
    if choice==0:
        ticks = time.time()
        stage1()
        break
    elif choice==1:
        rank()
    elif choice==2:
        about()
    elif choice==3:
        how()

