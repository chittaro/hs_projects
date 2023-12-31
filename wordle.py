from pathlib import Path
import pygame, time, random, os

pygame.init()
wwid = 550
whgt = 650
clock = pygame.time.Clock()
win = pygame.display.set_mode((wwid ,whgt))
pygame.display.set_caption('WORDLE')

###---Word Bank list
masterLoc = str(Path(r"wordleSet5.txt"))
#lowerLoc = str(Path(r"C:\Users\chitt\Documents\wordleCustom.txt"))


newFile = open(masterLoc)
wordBank = newFile.readlines()

for i in range(len(wordBank)):
    wordBank.insert(i, wordBank[i][0:5])
    wordBank.pop(i+1)


###---Key lists
letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p",
           "q","r","s","t","u","v","w","x","y","z"]
keyInput = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,
            pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,
            pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,
            pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,
            pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,
            pygame.K_z,]


###---Text control
def caption(text, size, cX, cY):
    font = pygame.font.SysFont('simsunextb', size, True, False)
    initTxt = font.render(text, 1, (0, 0, 0))
    
    txtWid, txtHgt = font.size(text)
    finalX = cX - (txtWid / 2)
    finalY = cY - (txtHgt / 2)
    win.blit(initTxt, (round(finalX), round(finalY)) )


###---Word control
class wClass():

    def __init__(self):
        global wordBank
        self.wordBank = wordBank
        self.pressed = False
        
        self.word = ""
        self.crtGuess = ""
        self.prevGuesses = []
        
        self.msg = ""
        
        self.wrdRad = 30
        self.xInit = (wwid / 2) - (self.wrdRad * 4)
        self.yInit = (whgt / 2) - (self.wrdRad * 5) - 50

        self.isOver = False

        self.yellowL, self.grayL, self.greenL = [], [], []

    def newWord(self):
        newIdx = random.randint(0, len(self.wordBank) - 1)
        self.word = self.wordBank[newIdx]
        self.isOver = False
        
        self.crtGuess = ""
        self.msg = ""
        self.prevGuesses = []

        self.yellowL, self.grayL, self.greenL = [], [], []
        print("the word is : " + wordle.word)
        

    def setPressed(self):
        if event.type == pygame.KEYUP:
            self.pressed = False
        if event.type == pygame.KEYDOWN:
            self.pressed = True

    def addChar(self, val):
        if len(self.crtGuess) < 5:
            self.crtGuess += val
    

    def delChar(self):
        if len(self.crtGuess) > 0:
            self.crtGuess = self.crtGuess[0: len(self.crtGuess) - 1]

    def doEnter(self):
        if len(self.crtGuess) == 5:
            if self.crtGuess in self.wordBank:
                self.prevGuesses.append(self.crtGuess)
                self.crtGuess = ""
                self.msg = ""
                if len(self.prevGuesses) == 6:
                    self.isOver = True
                    self.msg = "loser! lol. word was: " + self.word
                
            else:
                self.msg = "not a real word idot!"
                
        else:
            self.msg = "word 2 short.."

    def showCaption(self):
        caption(self.msg, 25, wwid/2, 480)


    def drawWord(self):
        for i in range(len(self.prevGuesses)):
            tempWord = self.word
            yPos = round(self.yInit + i * self.wrdRad * 2)
            picked = []

            
            for x in range(5):
                xPos = round(self.xInit + x * self.wrdRad * 2)
                crtChar = self.prevGuesses[i][x]
                
                if crtChar == tempWord[x]:
                    picked.append(x)
                    if crtChar not in self.greenL:
                        self.greenL.append(crtChar)
                    color = (100, 250, 100)
                    tempWord = tempWord[:x] + " " + tempWord[(x + 1):]
                    if len(picked) == 5:
                        self.isOver = True
                        self.msg = "winna!"

                else:
                    if crtChar not in self.grayL:
                        self.grayL.append(crtChar)
                    color = (250, 250, 250)
                    

                pygame.draw.circle(win, color, (xPos, yPos), self.wrdRad - 5)    
                caption(crtChar.upper(), 40, xPos, yPos)

                
            
            for x in range(5):
                xPos = round(self.xInit + x * self.wrdRad * 2)
                crtChar = self.prevGuesses[i][x]
                
                if crtChar in tempWord and x not in picked:
                    tempWord = tempWord[:tempWord.index(crtChar)] \
                    + " " + tempWord[(tempWord.index(crtChar) + 1):]
                    if crtChar not in self.yellowL:
                        self.yellowL.append(crtChar)
                    
                    pygame.draw.circle(win, (250, 250, 100), (xPos, yPos), self.wrdRad - 5)    
                    caption(crtChar.upper(), 40, xPos, yPos)

        
        for i in range(len(self.crtGuess)):
            xPos = round(self.xInit + i * self.wrdRad * 2)
            yPos = round(self.yInit + (len(self.prevGuesses)) * self.wrdRad * 2)
            caption(self.crtGuess[i].upper(), 40, xPos, yPos)


        
    def drawGrid(self):
        for i in range(6):
            yPos = round(self.yInit + i*self.wrdRad * 2)
            for i in range(5):
                xPos = round(self.xInit + i * self.wrdRad * 2)
                pygame.draw.circle(win, (200, 200, 200), (xPos, yPos), self.wrdRad)


    def drawLetters(self):
        global letters
        rad = 18
        startX = (wwid / 2) - (rad * 12)
        startY = 520

        for i in range(2):
            crtY = round(startY + i * rad * 2)
            
            for x in range(13):
                letIdx = x + (i * 13)
                
                crtX = round(startX + x * rad * 2)
                color = (200, 200, 200)
                if letters[letIdx] in self.greenL:
                    color = (100, 200, 100)
                elif letters[letIdx] in self.yellowL:
                    color = (250, 250, 100)
                elif letters[letIdx] in self.grayL:
                    color = (240, 240, 240)
                    
                pygame.draw.circle(win, color, (crtX, crtY), rad)
                caption(letters[letIdx].upper(), 16, crtX, crtY)

    def endCheck(self):
        if self.isOver == True:
            self.showCaption()
            pygame.display.update()
            time.sleep(3)
            self.newWord()            
                
        
            

wordle = wClass()
wordle.newWord()

###--- Main loop
run = True
while run == True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()
    mosX, mosY = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    
    if wordle.pressed == False and event.type == pygame.KEYDOWN:
        for i in range(len(letters)):
            if keys[ (keyInput[i]) ]:
                wordle.addChar( letters[i] )
                                
        if keys[(pygame.K_BACKSPACE)]:
            wordle.delChar()

        if keys[(pygame.K_RETURN)]:
            wordle.doEnter()
                
    wordle.setPressed()
    
    
    win.fill((255,255,255))
    caption("W O R D L E", 70, wwid/2, 30)
    caption("W O R D L E", 70, wwid/2 + 5, 30 + 5)
    caption("W O R D L E", 70, wwid/2 + 10, 30 + 10)


    wordle.drawGrid()
    wordle.drawWord()
    wordle.drawLetters()
    wordle.showCaption()

    wordle.endCheck()
    

    
    pygame.display.update()
    clock.tick(50)

pygame.quit()

