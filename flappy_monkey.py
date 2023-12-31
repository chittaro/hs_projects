import pygame, random, time, math, os

pygame.init()
wwid=600
win=pygame.display.set_mode((wwid,wwid))
score=0
Highscore=0
pygame.display.set_caption('Monkey Bird ---- High score = ' + str(Highscore))
clock=pygame.time.Clock()

##ingame bird values
size=70
x=round((wwid/4)-(size/2))
PipeDiff=230
PipeSpeed=10

##startScreen values
Ssize=150
startX=round((wwid/2)-Ssize/2)
startY=round((wwid/6)+Ssize/2)

##moving ingame backgrounds
BG1=pygame.image.load(os.path.join("Flappy_Media","CS_background.PNG"))
BG2=pygame.image.load(os.path.join("Flappy_Media","CS_background.PNG"))
BackgroundIMG1=pygame.transform.scale(BG1,(1200,820))
BackgroundIMG2=pygame.transform.scale(BG2,(1200,820))
BGX1=0
BGX2=1200

##vine pipes
vineimg=pygame.image.load(os.path.join("Flappy_Media","vine.png"))
vine=pygame.transform.scale(vineimg,(70,70))

##monkey image types
    #brown
Basic=pygame.image.load(os.path.join("Flappy_Media","BrownMonkey1.png"))
BrownMonk1=pygame.transform.scale(Basic,(size,size))
BigMonk1=pygame.transform.scale(Basic,(Ssize,Ssize))
Basic2=pygame.image.load(os.path.join("Flappy_Media","BrownMonkey2.PNG"))
BrownMonk2=pygame.transform.scale(Basic2,(size,size))
    #red
Monk2=pygame.image.load(os.path.join("Flappy_Media","RedMonkey2.PNG"))
RedMonk=pygame.transform.scale(Monk2,(size,size))
Monk22=pygame.image.load(os.path.join("Flappy_Media","RedMonkey1.PNG"))
RedMonk2=pygame.transform.scale(Monk22,(size,size))
    #purple
Monk3=pygame.image.load(os.path.join("Flappy_Media","PurpleMonkey2.PNG"))
PurpleMonk=pygame.transform.scale(Monk3,(size,size))
Monk33=pygame.image.load(os.path.join("Flappy_Media","PurpleMonkey1.PNG"))
PurpleMonk2=pygame.transform.scale(Monk33,(size,size))
    #teal
Monk4=pygame.image.load(os.path.join("Flappy_Media","TealMonkey2.PNG"))
TealMonk=pygame.transform.scale(Monk4,(size,size))
Monk44=pygame.image.load(os.path.join("Flappy_Media","TealMonkey1.PNG"))
TealMonk2=pygame.transform.scale(Monk44,(size,size))
    #yellow
Monk5=pygame.image.load(os.path.join("Flappy_Media","YellowMonkey2.PNG"))
YellowMonk=pygame.transform.scale(Monk5,(size,size))
Monk55=pygame.image.load(os.path.join("Flappy_Media","YellowMonkey1.PNG"))
YellowMonk2=pygame.transform.scale(Monk55,(size,size))

Jmonkeys=[BrownMonk2,RedMonk,PurpleMonk,TealMonk,YellowMonk]
Smonkeys=[BrownMonk1,RedMonk2,PurpleMonk2,TealMonk2,YellowMonk2]
monkey=BrownMonk1

##custom screen background
CBG=pygame.image.load(os.path.join("Flappy_Media","CS_background2.PNG"))
CustomBG=pygame.transform.scale(CBG,(wwid,wwid))

easy=False
medium=False
hard=False
R=[200,200,200]
Rchecker=0
introvel=20
neg=-1


run=True
introScreen=True
startScreen=False
customScreen=False
deadScreen=False
Rainbow=False

def restart():
    global y, score, jcount, Coords, IDcheck, incvalue, NumPipes, Hgt1, Hgt, monkey
    incvalue=0
    Coords=[1000]
    NumPipes=len(Coords)
    Hgt1=random.randint(50,350)
    Hgt=[Hgt1]
    IDcheck=-1
    y=((wwid/2)-(size/2))
    score=0
    jcount=10
    monkey=BrownMonk1

def Movement():
    global jcount
    global y
    if jcount<=-15:
        pass
    else:
        jcount-=1
    neg=1
    if jcount<=0:
        neg=-1
    y-=(jcount**2)/2*neg

def introMovement():
    global introvel, startY, neg
    if introvel==0:
        neg*=-1
    elif startY==round((wwid/6)+Ssize/2):
        neg*=-1
    if startY>round((wwid/6)+Ssize/2)-1:
        pass
    else:
        introvel-=1*neg
    startY-=round(introvel*neg/4)

def PipesSpawn(Dist,Speed):
    global Coords, Hgt
    for i in range (NumPipes):
        Coords[i]-=Speed
    for i in range(NumPipes):
        for x in range(math.ceil(Hgt[i]/70)):
            win.blit(vine,(Coords[i],Hgt[i]-70-(70*x)))
        for x in range(math.ceil((wwid-Hgt[i]+Dist)/70)):
            win.blit(vine,(Coords[i],Dist+Hgt[i]+(x*70)))        
    
def Caption(words,size,Cx,Cy):
    font=pygame.font.SysFont('simsunextb',size,True,False)
    text=font.render(words,1,(255,255,255))
    txtWid,txtHgt = font.size(words)
    Tx=Cx-(txtWid/2)
    Ty=wwid-Cy-(size/2)
    win.blit(text,(round(Tx),round(Ty)))

def BSpawn(CX,CY,R,G,B,Wid,Height,buttonID,words):
    mosX,mosY=pygame.mouse.get_pos()
    pressed1,pressed2,pressed3=pygame.mouse.get_pressed()
    if ((mosX>=CX-(Wid/2)) and mosX<=CX+(Wid/2) and (mosY>=wwid-CY-(Height/2) and mosY<=wwid-CY+(Height/2))):
        R=R+20
        G=G+20
        B=B+20
        global IDcheck
        if pressed1==True:
            IDcheck=buttonID
    else:
        R=R
        G=G
        B=B
    length=len(words)
    pygame.draw.rect(win,(R,G,B),(round(wwid-(wwid-CX)-(Wid/2)),round(wwid-CY-(Height/2)),Wid,Height))
    Caption(words,Height,CX,CY)


def DifficultyBtns():
    global PipeDiff, PipeSpeed, easy, medium, hard
    if IDcheck==4:
        PipeDiff=280
        PipeSpeed=6
        easy=True
    if IDcheck==5:
        PipeDiff=260
        PipeSpeed=8
        easy=False
        medium=True
    if IDcheck==6:
        PipeDiff=210
        PipeSpeed=12
        easy=False
        medium=False
        hard=True
    if easy==True:
        C1=[100,100,100]
        C2=[231,180,22]
        C3=[204,50,50]
    elif medium==True:
        C1=[45,201,55]
        C2=[100,100,100]
        C3=[204,50,50]
    elif hard==True:
        C1=[45,201,55]
        C2=[231,180,22]
        C3=[100,100,100]
    else:
        easy=False
        medium=False
        hard=False
        C1=[45,201,55]
        C2=[231,180,22]
        C3=[204,50,50]
    BSpawn(100,200,C1[0],C1[1],C1[2],180,50,4,'Easy')
    BSpawn(300,200,C2[0],C2[1],C2[2],180,50,5,'Medium')
    BSpawn(500,200,C3[0],C3[1],C3[2],180,50,6,'Hard')


def ReturnBtn():
    BSpawn(80,570,220,20,60,130,30,0,'Return')
    if IDcheck==0:
        global introScreen, customScreen, startScreen
        introScreen=True
        customScreen=False
        startScreen=False

def WallpaperMove():
    global BGX1
    global BGX2
    if BGX1<=-1200:
        BGX1=1200
    elif BGX2<=-1200:
        BGX2=1200
    BGX1-=1
    BGX2-=1
    win.blit(BackgroundIMG1,(round(BGX1),-200))
    win.blit(BackgroundIMG2,(round(BGX2),-200))

restart()

while run==True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    keys = pygame.key.get_pressed()

    if introScreen==True:
        ##start screen
        restart()
        win.blit(BackgroundIMG1,(0,-200))
        ##monkey movement animation
        introMovement()
        ##monkeystart
        win.blit(BigMonk1,(startX,round(startY)))
        ##start button
        Caption("Monkey Bird",65,300,520)
        BSpawn(300,230,41,171,103,400,60,1,'Start')
        if IDcheck==1:
            introScreen=False
            startScreen=True
        ##custom button
        BSpawn(300,150,98,114,110,400,60,2,'Customize')
        if IDcheck==2:
            introScreen=False
            customScreen=True

                
    elif customScreen==True:
        win.blit(CustomBG,(0,0))
        ReturnBtn()
        ##Rainbow button
        BSpawn(300,380,R[0],R[1],R[2],350,60,9,'Rainbow')
        if IDcheck==9 and checker==0:
            checker=1
            if Rainbow==True:
                Rainbow=False
            else:
                Rainbow=True
        if Rainbow==True:
            R=[random.randint(0,235),random.randint(0,235),random.randint(0,235)]
        else:
            R=[150,150,150]
        if event.type == pygame.MOUSEBUTTONUP:
            checker=0
            IDcheck=10
        DifficultyBtns()           
    
    elif startScreen==True:
        if keys[pygame.K_SPACE]:
            jcount=7
            monkey=BrownMonk2
            if Rainbow==True:
                rand=random.randint(0,4)
                monkey=Jmonkeys[rand]
                
        if event.type==pygame.KEYUP:
            monkey=BrownMonk1
            if Rainbow==True:
                monkey=Smonkeys[rand]
        
        WallpaperMove()
        Movement()
        ##pipe addition+removal
        if Coords[NumPipes-1]<=600:
            Coords.append(1000)
            NumPipes=len(Coords)
            Hgt.append(random.randint(50,350))
        if Coords[0]<=-70:
            Coords.pop(0)
            NumPipes=len(Coords)
            Hgt.pop(0)
            Hgt.insert((NumPipes+1),random.randint(50,350))
        PipesSpawn(PipeDiff,PipeSpeed)
        Caption(str(score),50,300,575)
        ReturnBtn()
        win.blit(monkey,(x,round(y)))
        
        if y>=wwid:
            startScreen=False
            deadScreen=True
        if (x >= Coords[0] and x <= Coords[0]+70) or (x+size >= Coords[0] and x+size <= Coords[0]+70):
            if y<=Hgt[0] or y+size>=Hgt[0]+PipeDiff:
                startCheck=False
                startScreen=False
                deadScreen=True
            else:
                startCheck=True
        if x>=Coords[0]+70 and startCheck==True:
            score+=1
            startCheck=False

    elif deadScreen==True:
        Caption('You LOSE',70,300,435)
        pygame.draw.rect(win,(98,114,110),(175,200,250,350))
        Caption('Final Score:',30,300,350)
        Caption(str(score),50,300,310)
        if score>Highscore:
            Highscore=score
        Caption('High Score:',30,300,240)
        Caption(str(Highscore),50,300,200)
        BSpawn(300,140,220,20,60,250,50,7,'Restart')
        BSpawn(300,75,41,171,103,250,50,8,'Home')

        if IDcheck==7:
            deadScreen=False
            startScreen=True
            restart()

        if IDcheck==8:
            deadScreen=False
            introScreen=True
            restart()
        pygame.display.set_caption('Monkey Bird ---- High score = ' + str(Highscore))

    pygame.display.update()
    clock.tick(30)
pygame.quit()