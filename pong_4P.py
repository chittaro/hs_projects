import pygame, time, random

pygame.init()
wwid=1220
whgt=800
win=pygame.display.set_mode((wwid,whgt))
clock=pygame.time.Clock()
pygame.display.set_caption('pong')

#pygame.mixer.init()
font=pygame.font.SysFont('fixedsys',50,True,False)

class Player:
    wid=20
    hgt=80
## vel = divis by 210 (y)
    vel=15
    
        
    def __init__(self,x,score,depth,y,startY,endY):
        self.x=x
        self.score=score
        self.depth=depth
        self.y=y
        self.startY=startY
        self.endY=endY

    def boundCheck(self):
        if self.y>=self.endY-self.hgt:
            self.y=self.endY-self.hgt
        elif self.y<=self.startY:
            self.y=self.startY

        if (self.y-B1.size<=B1.y<=self.y+self.hgt) and (B1.x==self.x+self.depth):
            #pygame.mixer.music.load('PongBang.mp3')
            #pygame.mixer.music.play()

            B1.Yvel=(B1.y+(B1.size/2)-self.y-50)/-3
            B1.Yneg=1
            B1.Xneg*=-1
            B1.hitcount+=1
            if B1.hitcount>=12:
                B1.Xvel=B1.speeds[4]
            elif B1.hitcount>=9:
                B1.Xvel=B1.speeds[3]
            elif B1.hitcount>=6:
                B1.Xvel=B1.speeds[2]
            elif B1.hitcount>=3:
                B1.Xvel=B1.speeds[1]
            elif B1.hitcount>=0:
                B1.Xvel=B1.speeds[0]                
            B1.color=[(random.randint(50,255)),(random.randint(50,255)),(random.randint(50,255))]
            
        self.y=round(self.y)            
        

class Ball:
    speeds=[12, 15, 18, 20, 27]
    size=Player.wid
    x=round(wwid/2-size/2)
    y=round(whgt/2-size/2)
##vel = divis by 250 [2,5,10,25]
    Xvel=12#
    Yvel=0
    Xneg=1
    Yneg=1
    
    def __init__(self,color,hitcount):
        self.color=color
        self.hitcount=hitcount

    def move(self):            
        if (self.y<=0) or (self.y+self.size>=whgt):
            self.Yneg*=-1
            #pygame.mixer.music.load('WallBang.mp3')
            #pygame.mixer.music.play()

        self.x-=self.Xvel*self.Xneg
        self.y-=self.Yvel*self.Yneg

def Restart():
    #global deathSound
    B1.hitcount=0
    B1.x=round(wwid/2-B1.size/2)
    B1.y=round(whgt/2-B1.size/2)
    B1.Xvel=12#
    B1.Yvel=0
    P1.y=160
    P2.y=160
    P3.y=560
    P4.y=560
    #pygame.mixer.music.load('DeathSound.mp3')
    #pygame.mixer.music.play()

def Win(player,color):
    winText=font.render(player,1,color)
    win.blit(winText,(round(wwid/2-130),round(whgt/2-25)))
    pygame.display.update()
    time.sleep(2)
    P1.score=0
    P2.score=0
        
##X values = distance from border + width
P1=Player(40,0,20,160,0,(whgt/2))#
P2=Player(1160,0,-20,160,0,(whgt/2))#
P3=Player(40,0,20,560,(whgt/2),whgt)
P4=Player(1160,0,-20,560,(whgt/2),whgt)

B1=Ball([255,255,255],0)#

run=True

while run==True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    keys=pygame.key.get_pressed()
    ## 15 = number divisible by starting y positions (210)
    
    ##P1
    if keys[pygame.K_1]:
        P1.y-=Player.vel
    if keys[pygame.K_q]:
        P1.y+=Player.vel
    ##P2
    if keys[pygame.K_BACKSPACE]:
        P2.y-=Player.vel
    if keys[pygame.K_BACKSLASH]:
        P2.y+=Player.vel
    ##P3
    if keys[pygame.K_d]:
        P3.y-=Player.vel
    if keys[pygame.K_c]:
        P3.y+=Player.vel
    ##P4
    if keys[pygame.K_UP]:
        P4.y-=Player.vel
    if keys[pygame.K_DOWN]:
        P4.y+=Player.vel

    P1.boundCheck()
    P2.boundCheck()
    P3.boundCheck()
    P4.boundCheck()
    B1.move()

    if B1.x+B1.size<=0:
        P2.score+=1
        Restart()
        
    elif B1.x>=wwid:
        P1.score+=1
        Restart()        
        
    win.fill((0,0,0))
    text1=font.render(str(P1.score),1,(255,0,0))
    text2=font.render(str(P2.score),1,(0,0,255))
        
    pygame.draw.rect(win,(255,255,255),(P1.x,P1.y,P1.wid,P1.hgt))
    pygame.draw.rect(win,(255,255,255),(P2.x,P2.y,P2.wid,P2.hgt))
    pygame.draw.rect(win,(255,255,255),(P3.x,P3.y,P3.wid,P3.hgt))
    pygame.draw.rect(win,(255,255,255),(P4.x,P4.y,P4.wid,P4.hgt))
    
    pygame.draw.line(win,(50,50,50),(0,round(whgt/2)),(wwid,round(whgt/2)))
    pygame.draw.line(win,(255,255,255),(round(wwid/2),0),(round(wwid/2),whgt))
    pygame.draw.rect(win,(B1.color),(B1.x,round(B1.y),B1.size,B1.size))
    win.blit(text1,(round(wwid/2)-60,10))#
    win.blit(text2,(round(wwid/2)+30,10))#


    if P1.score==10:
        Win("Red team WINS!",[255,0,0])
    elif P2.score==10:
        Win("Blue team WINS!",[0,0,255])
    pygame.display.update()
    clock.tick(30)

pygame.quit()