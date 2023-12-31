import pygame,time,random,os,math

pygame.init()
wwid=600
whgt=750
win=pygame.display.set_mode((wwid,wwid))
clock=pygame.time.Clock()
pygame.display.set_caption('---dot canvas---')

colWid = 170
colHgt = 100
sizeWid = 200
sizeHgt = 40
menu = False

cursor = pygame.image.load(os.path.join("Cursor_Media","cursor.png"))
cursor_icon = pygame.transform.scale(cursor, (8,14))
rainbowLoad = pygame.image.load(os.path.join("Cursor_Media","color_fade.jpeg"))
rainbow_img = pygame.transform.scale(rainbowLoad,(colWid,colHgt))
sizeLoad = pygame.image.load(os.path.join("Cursor_Media","size_adjust.png"))
size_img = pygame.transform.scale(sizeLoad,(sizeWid,sizeHgt))



#### global variables

numCursors = 1
inputNums = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
             pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]




dotSize = 2
newSize = dotSize
dotColor = (100,100,100)
newColor = dotColor

circleX = 330
circleY = 655

#### functions

def sizePos():
    global newSize, sizeWid, sizeHgt, mosX, mosY, circleX, circleY

    if 315<mosX<315+sizeWid and 640<mosY<670 and pressed[0]:
        circleX = mosX
    pygame.draw.circle(win,(150,150,150),(circleX,circleY),15)
    newSize = round((circleX-315)/20)+1


    lineY = round(690 + (sizeHgt/sizeWid)*(200-(circleX-315)))
    
    pygame.draw.line(win,(150,150,150),(circleX,circleY),(circleX, lineY ),4)


    
    

def Reset():
    global dotSize, dotColor, ultList, colTracker, sizeTracker, colList, sizeList, XposList, YposList
    XposList = []
    YposList = []
    ultList = []
    colTracker = [0]
    sizeTracker = [0]
    colList = [dotColor]
    sizeList = [dotSize]

def Caption(words,size,Cx,Cy):
    font = pygame.font.SysFont('simsunextb',size,True,False)
    text = font.render(words,1,(0,0,0))
    txtWid,txtHgt = font.size(words)
    Tx = Cx-(txtWid/2)
    Ty = whgt-Cy-(size/2)
    win.blit(text,(round(Tx),round(Ty)))

def getPos():
    global XposList,YposList,numCursors,Xneg,Yneg
    cursAng = round(360/numCursors)

    ## initial cursor
    
    mosX, mosY = pygame.mouse.get_pos()

    x = mosX-(wwid/2)
    y = mosY-(wwid/2)


    if x == 0:
        x += 1
    if y == 0:
        y += 1


    radius = math.hypot(x,y)
    
    innerAngle = math.degrees(math.atan((x/y)))
    if innerAngle<0:
        innerAngle = 90 + innerAngle
    
    wholeAngle = math.degrees(math.atan2(x,y))
    if wholeAngle<0:
        wholeAngle = 180 + (180+wholeAngle)
    
    ultAngle = wholeAngle


    XposList.append(mosX)
    YposList.append(mosY)

    
    ## rest of cursors
    
    if numCursors>1:

        for i in range(numCursors-1):
            ultAngle = (ultAngle+cursAng)%360
            innerAngle = ultAngle%90

            if innerAngle == 0:
                innerAngle += 1
            
            x = ((math.sin(math.radians(innerAngle)))*radius)
            y = ((math.cos(math.radians(innerAngle)))*radius)

            if 90<ultAngle<=180:
                z = -x
                x = y
                y = z
            elif 180<ultAngle<=270:
                x *= -1
                y *= -1
            elif 270<ultAngle<=360:
                z = -y
                y = x
                x = z
                                  
            x += (wwid/2)
            y += (wwid/2)



            XposList.append(x)
            YposList.append(y)
            
        
        
#### while loop initiation

Reset()



run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False

#### cursor num selection

    keys = pygame.key.get_pressed()
    for i in range(9):
        if keys[inputNums[i]]:
            numCursors = i+1

    mosX, mosY = pygame.mouse.get_pos()

    if mosY<wwid:
        getPos()
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)
        


    win.fill((255,255,255))

    pygame.draw.line(win,(0,0,0),(0,wwid),(wwid,wwid))


    pressed = pygame.mouse.get_pressed()

    
    if pressed[0] and mosY<wwid:
        for i in range(numCursors):
            if (XposList[i],YposList[i]) not in ultList and YposList[i]<wwid:
                ultList.append((round(XposList[i]),round(YposList[i])))
                if newColor != colList[len(colList)-1]:
                    colList.append(newColor)
                    colTracker.append(len(ultList)-1)

                if newSize != sizeList[len(sizeList)-1]:
                    sizeList.append(newSize)
                    sizeTracker.append(len(ultList)-1)
                

    
    if keys[pygame.K_UP]:
        win=pygame.display.set_mode((wwid,wwid))
        menu = False
    elif keys[pygame.K_DOWN]:
        win=pygame.display.set_mode((wwid,whgt))
        menu = True

        
    for i in range(len(ultList)):
        
        for x in range(len(colTracker)):
            if colTracker[x]==i:
                cval = x

        for x in range(len(sizeTracker)):
            if sizeTracker[x]==i:
                sval = x
            
        pygame.draw.circle(win,colList[cval],ultList[i],sizeList[sval])


    if menu:
        #color spectrum
        win.blit(rainbow_img,(70,635))
        Caption("color selector:",20,70+(colWid/2),135)
        if 70<mosX<70+colWid and 635<mosY<635+colHgt and pressed[0]:
            newColor = win.get_at((mosX, mosY))[:3]
            pygame.draw.circle(win,(255,255,255),(mosX,mosY),20)
            pygame.draw.circle(win,newColor,(mosX,mosY),16)
            

        #dot size
        win.blit(size_img,(315,690))
        Caption("size selector:",20,330+(sizeWid/2),135)

        sizePos()

        pygame.draw.rect(win,(0,0,0),(540,605, 40,40))
        pygame.draw.rect(win,(255,255,255),(545,610, 30,30))
        pygame.draw.circle(win,newColor,(560,625),newSize)
        
        

    if mosY<wwid:
        pygame.draw.circle(win, (255, 0, 0), (round(XposList[0]),round(YposList[0])), 5)
        for i in range(1, numCursors):
            win.blit(cursor_icon,(round(XposList[i]),round(YposList[i])))
    

    XposList=[]
    YposList=[]

    if keys[pygame.K_SPACE]:
        Reset()

    if keys[pygame.K_BACKSPACE]:
        try:
            ultList.pop(0)
            print(ultList[0])
            time.sleep(0.01)
            print("did it")
        except BaseException as err:
            print("cannot")
        
    pygame.display.update()

pygame.quit()