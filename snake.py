import pygame
import random
import time

pygame.init()
wwid=600
win=pygame.display.set_mode((wwid,wwid))
clock = pygame.time.Clock()
size=30

##snake head/body images
#face=pygame.image.load("face.png")
#goodface=pygame.transform.scale(face,(size,size))

#snh=pygame.image.load("snake_face.png")
#snhresize=pygame.transform.scale(snh,(size,size))
#angle=0
#snhfinal=pygame.transform.rotate(snhresize,angle)

##coordinate grid
gridlength=round(wwid/size)
coordinates=[]
incvalue=0
for i in range(gridlength):
    point=size*incvalue
    coordinates.append(point)
    incvalue+=1

##game initialization
xval=0
yval=0
x=coordinates[round(len(coordinates)/2)]
y=coordinates[round(len(coordinates)/2)]
Score=0
position=random.randint(0,len(coordinates)-1)
foodx=coordinates[position]
position=random.randint(0,len(coordinates)-1)
foody=coordinates[position]
R=0
G=60
B=0

##game over
GOsize=int(round(wwid/6))
GOtxt="Game over"
GOfont=pygame.font.SysFont('arcade',GOsize,True,False)
GOtext=GOfont.render(GOtxt,1,(255,0,0))

##grid display
def Line():
    yincvalue=0
    xincvalue=0
    for i in range(gridlength*2):
        if yincvalue<(gridlength):
            yline=coordinates[yincvalue]
            pygame.draw.line(win,(100,100,100),(0,yline),(wwid,yline),1)
            yincvalue+=1
        else:
            xline=coordinates[xincvalue]
            pygame.draw.line(win,(0,0,0),(xline,0),(xline,wwid),1)
            xincvalue+=1

##snake body
snakebodyX=[]
snakebodyY=[]
def list_add():
    snakebodyX.append(x)
    snakebodyY.append(y)
def list_pop(pos):
    snakebodyX.pop(pos)
    snakebodyY.pop(pos)

HS=Score

##previous x position [second to last]
list_add()

run=True
GameOver=False

while run==True:    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

##snake direction control
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle=270
                xval=-1
                yval=0
            if event.key == pygame.K_RIGHT:
                angle=90
                xval=1
                yval=0
            if event.key == pygame.K_UP:
                angle=180                
                xval=0
                yval=-1
            if event.key == pygame.K_DOWN:
                angle=0
                xval=0
                yval=1
        #snhfinal=pygame.transform.rotate(snhresize,angle)

##border collision
    if -size<x+(xval*size)<wwid:
        x+=xval*size
    else:
        GameOver=True
    if -size<y+(yval*size)<wwid:
        y+=yval*size
    else:
        GameOver=True
       
##snake food values
    if x==foodx and y==foody:
        position=random.randint(0,len(coordinates)-1)
        foodx=coordinates[position]
        position=random.randint(0,len(coordinates)-1)
        foody=coordinates[position]
        Score+=1
    else:
        list_pop(0)
##old x position removal


##scoreboard
    pygame.display.set_caption('Score= '+str(Score)+" ---- High Score= "+str(HS))
    win.fill((255,255,255))
    Line()
    list_add()

#snakebody call
    snakeinc=0
    for i in range(Score+1):
        if G+(snakeinc*5)>255:
            G=255
            R=195
        else:
            G+=snakeinc*5
            R+=snakeinc*5
        X=snakebodyX[Score-snakeinc]
        Y=snakebodyY[Score-snakeinc]
        if snakeinc>=1:
            pygame.draw.rect(win,(R,G,R),(X,Y,size,size))
            if X==snakebodyX[Score] and Y==snakebodyY[Score]:
                GameOver=True
            
        else:
            pygame.draw.rect(win,(R,G,R),(X,Y,size,size))
            #win.blit(snhfinal,(X,Y))
            
        snakeinc+=1
        R=0
        G=60             
        
#gameover
    if GameOver==True:
        pygame.draw.rect(win,(0,0,0),(x,y,size,size))
        ##sound
        pygame.display.update()
        time.sleep(1)
        win.fill((255,255,255))
        win.blit(GOtext,(int(wwid/2-200),int((wwid/2)-GOsize)))
        pygame.display.update()
        time.sleep(2)
        ##reset
        xval=0
        yval=0
        x=coordinates[round(len(coordinates)/2)]
        y=coordinates[round(len(coordinates)/2)]
        if Score>=HS:
            HS=Score
        Score=0
        position=random.randint(0,len(coordinates)-1)
        foodx=coordinates[position]
        position=random.randint(0,len(coordinates)-1)
        foody=coordinates[position]
        snakebodyX.clear()
        snakebodyY.clear()
        GameOver=False
        list_add()
             
    #win.blit(goodface,(x,y))
    pygame.draw.rect(win,(255,0,0),(foodx,foody,size,size))
    pygame.display.update()
    clock.tick(15)
    
pygame.quit()