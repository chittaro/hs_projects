import pygame
import time
import random

pygame.init()
wwid=600
whgt=500
win=pygame.display.set_mode((wwid,whgt))
clock=pygame.time.Clock()
pygame.display.set_caption('pong')
speed=38

font=pygame.font.SysFont('fixedsys',50,True,False)

class Player:
    wid=20
    hgt=80
    y=round(whgt/2-hgt/2)
## vel = divis by 210
    vel=15
    
        
    def __init__(self, x,score,depth):
        self.x=x
        self.score=score
        self.depth=depth

    def boundCheck(self):
        if self.y>=500-self.hgt:
            self.y=500-self.hgt
        elif self.y<=0:
            self.y=0

        global speed
        if (self.y-B1.size<=B1.y<=self.y+self.hgt) and (B1.x==self.x+self.depth):
            B1.Yvel=(B1.y+(B1.size/2)-self.y-50)/-5
            B1.Yneg=1
            B1.Xneg*=-1
            speed+=2
            
        

class Ball:
    size=Player.wid
    x=round(wwid/2-size/2)
    y=round(whgt/2-size/2)
##vel = divis by 250 [2,5,10,25]
    Xvel=10
    Yvel=0
    Xneg=1
    Yneg=1
    
    def __init__(self,color):
        self.color=color

    def move(self):            
        if (self.y<=0) or (self.y+self.size>=whgt):
            self.Yneg*=-1

        self.x-=self.Xvel*self.Xneg
        self.y-=self.Yvel*self.Yneg

def Restart():
    global speed
    B1.x=round(wwid/2-B1.size/2)
    B1.y=round(whgt/2-B1.size/2)
    B1.Xvel=10
    B1.Yvel=0
    P1.y=round(whgt/2-P1.hgt/2)
    P2.y=round(whgt/2-P2.hgt/2)
    speed=38

def Win(player,color):
    winText=font.render(player,1,color)
    win.blit(winText,(round(wwid/2-130),round(whgt/2-25)))
    pygame.display.update()
    time.sleep(2)
    P1.score=0
    P2.score=0
        
##X values = distance from border + width
P1=Player(20,0,20)    
P2=Player(560,0,-20)
B1=Ball([255,255,255])

run=True

while run==True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    keys=pygame.key.get_pressed()
    ## 15 = number divisible by starting y positions (210)
    if keys[pygame.K_w]:
        P1.y-=Player.vel
    if keys[pygame.K_s]:
        P1.y+=Player.vel
    if keys[pygame.K_UP]:
        P2.y-=Player.vel
    if keys[pygame.K_DOWN]:
        P2.y+=Player.vel

    P1.boundCheck()
    P2.boundCheck()
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
        
    

    pygame.draw.line(win,(255,255,255),(0,0),(wwid,0))
    pygame.draw.line(win,(255,255,255),(300,0),(300,whgt))
    
    pygame.draw.rect(win,(B1.color),(B1.x,B1.y,B1.size,B1.size))
    pygame.draw.rect(win,(255,255,255),(P1.x,P1.y,P1.wid,P1.hgt))
    win.blit(text1,(300-60,10))
    win.blit(text2,(300+30,10))    
    pygame.draw.rect(win,(255,255,255),(P2.x,P2.y,P2.wid,P2.hgt))
    if P1.score==10:
        Win("Player 1 WINS!",[255,0,0])
    elif P2.score==10:
        Win("Player 2 WINS!",[0,0,255])
    pygame.display.update()
    clock.tick(speed)

pygame.quit()