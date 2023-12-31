import pygame, time, random, os

pygame.init()
wwid = 900
whgt = 660
clock = pygame.time.Clock()
win = pygame.display.set_mode((wwid, whgt))
pygame.display.set_caption('Snake Blockus')

PRP = (128,0,128)
GRN = (60,179,113)
RED = (200, 0, 0)
BLK = (0, 0, 0)
WHT = (255, 255, 255)

hlfWid = round(wwid / 2)
hlfHgt = round(whgt / 2)


def caption(text, size, cX, cY, color):
    font = pygame.font.SysFont('simsunextb', size, True, False)
    initTxt = font.render(text, 1, color)
    
    txtWid, txtHgt = font.size(text)
    finalX = cX - (txtWid / 2)
    finalY = cY - (txtHgt / 2)
    win.blit(initTxt, (round(finalX), round(finalY)) )


class snake():

    def __init__(self, edgeVec, xVec, yVec, color, name):
        self.size = round(wwid / 60)
        self.color = color
        self.name = name
        self.score = 0

        self.edgeDist = 6 * self.size
        self.reset(edgeVec, xVec, yVec)


    def reset(self, edgeVec, xVec, yVec):
        if edgeVec == -1:
            self.crtX = wwid - self.edgeDist - self.size
            self.crtY = whgt - self.edgeDist - self.size
        else:
            self.crtX = self.edgeDist
            self.crtY = self.edgeDist

        self.xVector = xVec
        self.yVector = yVec
        self.blockList = []


    def setDir(self, newXVec, newYVec):
        if newXVec != self.xVector * -1:
            self.xVector = newXVec
        if newYVec != self.yVector * -1:
            self.yVector = newYVec

        
    
    def move(self):
        self.blockList.append([self.crtX, self.crtY])
        self.crtX = self.nextPos()[0]
        self.crtY = self.nextPos()[1]
        


    def nextPos(self):
        newX = self.crtX + (self.xVector * self.size)
        newY = self.crtY + (self.yVector * self.size)
        finList = [newX, newY]
        return finList



    def canMove(self, otherBlocks):
        ##check boundaries
        if 0 <= self.crtX <= wwid - self.size and 0 <= self.crtY <= whgt - self.size:
                
            ##check placed blocks
            if self.isntBlock(self.blockList, self.crtX, self.crtY) and self.isntBlock(otherBlocks, self.crtX, self.crtY):
                return True


        return False

    
    
    def isntBlock(self, blocks, xPos, yPos):
        for i in range(len(blocks)):
            if xPos == blocks[i][0] and yPos == blocks[i][1]:                
                return False


        return True
    


    def draw(self):
        for i in range(len(self.blockList)):
            if i == len(self.blockList) - 1:
                pygame.draw.rect(win, RED, (self.blockList[i][0], self.blockList[i][1], self.size, self.size))

            else:
    
                pygame.draw.rect(win, self.color, (self.blockList[i][0], self.blockList[i][1], self.size, self.size))
            

lSnake = snake(1, 0, 1, PRP, 'left player')
rSnake = snake(-1, 0, -1, GRN, 'right player')

screen = "start"
##all screens: start, game, defeat, pause?

        
run = True
while run == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()
    mosX, mosY = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()


    win.fill(WHT)

    if screen == "start":

        caption("snake blockus", 70, round(wwid/2), round(whgt/2) - 30, (0, 100, 0))
        caption("[press ENTER to play]", 20, round(wwid/2), round(whgt/2) + 20, (0, 0, 0))

        
        if keys[(pygame.K_RETURN)]:
            screen = "game"



        
    elif screen == "game":
        ####LEFT PLAYER:


        ## set direction w/ key inputs
        if keys[(pygame.K_w)]:
            lSnake.setDir(0, -1)
            
        if keys[(pygame.K_s)]:
            lSnake.setDir(0, 1)
            
        if keys[(pygame.K_a)]:
            lSnake.setDir(-1, 0)
            
        if keys[(pygame.K_d)]:
            lSnake.setDir(1, 0)

        ## move
        if lSnake.canMove(rSnake.blockList):      
            lSnake.move()
            lSnake.draw()
            
        else:
            screenCap = rSnake.name + " WINS"
            rSnake.score += 1
            screen = "defeat"        


        if screen != "defeat":
            ####RIGHT PLAYER:

        
            ## set direction w/ key inputs
            if keys[(pygame.K_UP)]:
                rSnake.setDir(0, -1)
                
            if keys[(pygame.K_DOWN)]:
                rSnake.setDir(0, 1)
                
            if keys[(pygame.K_LEFT)]:
                rSnake.setDir(-1, 0)
                
            if keys[(pygame.K_RIGHT)]:
                rSnake.setDir(1, 0)
                
            ## move
            if rSnake.canMove(lSnake.blockList):
                rSnake.move()
                rSnake.draw()

            else:
                screenCap = lSnake.name + " WINS"
                lSnake.score += 1
                screen = "defeat"



    elif screen == "defeat":
        caption(screenCap, 50, hlfWid, hlfHgt - 40, RED)
        caption("SCORE: " + str(lSnake.score), 40, round(wwid / 4), hlfHgt + 50, PRP)
        caption("SCORE: " + str(rSnake.score), 40, hlfWid + round(wwid / 4), hlfHgt + 50, GRN)
        lSnake.reset(1, 0, 1)
        rSnake.reset(-1, 0, -1)
        pygame.display.update()
        
        time.sleep(1.5)
        screen = "game"


    pygame.display.update()
    clock.tick(25)

pygame.quit()