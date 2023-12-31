import pygame,time,random,os

pygame.init()
wwid = 600
whgt = 700
win = pygame.display.set_mode((wwid,whgt))
clock = pygame.time.Clock()
pygame.display.set_caption('mathsteroids')


initAsteroid = pygame.image.load(os.path.join("Asteroids_Media","asteroid_img.png"))
AsteroidImg = pygame.transform.scale(initAsteroid, (40,40))

initEarth = pygame.image.load(os.path.join("Asteroids_Media","2D_earth.png"))
EarthImg =  pygame.transform.scale(initEarth, (wwid, wwid-200))

initMult = pygame.image.load(os.path.join("Asteroids_Media","mult_symbol.png"))
MultImg =  pygame.transform.scale(initMult, (60, 60))

initGO = pygame.image.load(os.path.join("Asteroids_Media","game_over.png"))
GOImg = pygame.transform.scale(initGO, (400,60))

Score = 0
Lives = 5
boxColor = (150,150,150)
inputBoxY = whgt-60
inputBoxX = 0

numList = ["0","1","2","3","4","5","6","7","8","9"]
keyInput = [pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,
                pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]
numAnswer = []
numString = ""

Gamemode = -1

newPress = True
correct = False

def scoreUpdate(S, L):
    global Score, Lives, numAst, prevTime
    Lives += L
    Score += S
    if Lives == 0:
        for i in range(numAst):
            entities[i].y=(-1)*entities[i].radius
        numAst = 1
        Score = 0
        Lives = 5
        boxColor = (150,150,150)
        win.fill((0,0,0))
        win.blit(GOImg,(round((wwid/2)-200),round((whgt/2)-30)))
        ##
        pygame.display.update()
        time.sleep(1.5)
        prevTime = pygame.time.get_ticks()
        
        
class asteroid():

    def reset(self):
        global Gamemode
        if Gamemode == 1:
            self.val1 = random.randint(1,99)
            self.val2 = random.randint(1,self.val1)
            self.func = random.choice("+-")

        else:
            self.val1 = random.randint(0,11)
            self.val2 = random.randint(0,11)
            self.func = "x"
        
        self.Sfactor = len(str(self.val1))+len(str(self.val2)) + 3
        self.radius = 120
        self.x = random.randint(self.radius,wwid-self.radius-1)
        self.speed = 1
        self.y = (-1)*self.radius
        self.AsteroidImg = pygame.transform.scale(initAsteroid,(self.radius, self.radius))

    def fall(self):
        self.y += self.speed
        win.blit(self.AsteroidImg, (self.x, self.y))
        size = round((self.Sfactor*-1.5) + 50)
        Textify(str(self.val1)+" "+self.func+" "+str(self.val2), self.x+5, round(self.y+(self.radius/2)-5),size,(0,0,0))

    def collision(self):
        if self.y+self.radius>=inputBoxY-100:
            self.reset()
            scoreUpdate(0,-1)

    def AnsCheck(self):
        global numString, boxColor, correct
        if len(numString)>0:
            if self.func == "+":
                if int(self.val1) + int(self.val2) == int(numString):
                    correct = True
                else:
                    correct = False
                    
            elif self.func == "-":
                if self.val1 - self.val2 == int(numString):
                    correct = True
                else:
                    correct = False

            else:
                if self.val1 * self.val2 == int(numString):
                    correct = True
                else:
                    correct = False                
            
        

def NumCheck():
    global numList, keyInput, numAnswer, newPress, numString
    if newPress:
        for i in range(len(numList)):
            if keys[(keyInput[i])]:
                numAnswer.append(str(numList[i]))
                i = len(numList)
        StringAns()

def StringAns():
    global NumAnswer, numString
    numString = ""
    for i in range(len(numAnswer)):
        numString += numAnswer[i]


def Textify(text,Xpos,Ypos,size,txtcolor):
    font=pygame.font.SysFont('fixedsys',size,True,False)
    finalTxt = font.render(text,1,txtcolor)
    win.blit(finalTxt,(Xpos,Ypos))

def Delete():
    if len(numAnswer)>0:
        numAnswer.pop()
        StringAns()
  

A1 = asteroid()
A2 = asteroid()
A3 = asteroid()
A4 = asteroid()

entities = [A1, A2, A3, A4]
for i in range(4):
    entities[i].reset()

prevTime = 0
numAst = 1

scoreUpdate(0,0)

run=True

while run==True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    currentTime = pygame.time.get_ticks()
    if currentTime-prevTime>5000 and numAst<len(entities):
        numAst+=1
        prevTime = pygame.time.get_ticks()

    mosX, mosY = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    if wwid-80<=mosX<=wwid and inputBoxY-100<mosY<inputBoxY-20 and pressed[0]:
        Gamemode *= -1

    win.fill((0,0,0))
    win.blit(EarthImg, (0,inputBoxY-100))
    pygame.draw.rect(win,(200,200,200),(wwid-80,inputBoxY-100,80,80))
    if Gamemode == 1:
        rot_image = pygame.transform.rotate(MultImg, 45)
        win.blit(rot_image, (wwid-83,inputBoxY-103))
        
    else:
        rot_image = pygame.transform.rotate(MultImg, 0)
        win.blit(rot_image, (wwid-70,inputBoxY-90))
        
    pygame.draw.rect(win,boxColor,(inputBoxX,inputBoxY,wwid,whgt-inputBoxY))
    

    keys = pygame.key.get_pressed()

    if event.type==pygame.KEYDOWN and newPress:
        if keys[(pygame.K_BACKSPACE)]:
            Delete()
            
        elif keys[(pygame.K_RETURN)]:
            for i in range(numAst):
                print(i)
                entities[i-1].AnsCheck()
                if correct:
                    entities[i-1].reset()
                    scoreUpdate(1,0)
                    boxColor = (0,200,0)
                    i = numAst
                    #print(str(i)+" correct")


            if correct == False:
                boxColor = (200,0,0)
                scoreUpdate(-1,0)
                
                
            for i in range(len(numAnswer)):
                Delete()
            
        else:
            NumCheck()
        newPress = False

    elif event.type==pygame.KEYUP:
        newPress = True
    
    for i in range (numAst):
        entities[i-1].collision()
        entities[i-1].fall()

    Textify("Score: "+str(Score), 0, 0, 50, boxColor)
    Textify("Lives: "+str(Lives), wwid-160, 0, 50, (220,220,0))

        
    Textify("Answer: "+numString, inputBoxX, inputBoxY, round((whgt-inputBoxY)*1.5),(0,0,0))


    
    pygame.display.update()
    clock.tick(25)

pygame.quit()