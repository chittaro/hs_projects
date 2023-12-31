import pygame, time, random, os, math

pygame.init()
wwid, whgt = 650, 650
win = pygame.display.set_mode((wwid,whgt))
clock = pygame.time.Clock()
pygame.display.set_caption('homescapes')

boxSize = 50
itemTypes = [1, 2, 3] # change spawnFill()


########################################################
class item():
    def __init__(self, objtype, xinit, yinit):
        self.x = xinit
        self.y = yinit
        self.objtype = objtype
        self.offset = mainGrid.cornerOffset
        self.size = boxSize - (2*self.offset)
        self.xHandles, self.yHandles = mainGrid.xHandles, mainGrid.yHandles
        self.allTypes = itemTypes

        if objtype == self.allTypes[0]:
            cImport = pygame.image.load(os.path.join("Homescapes_Media", "candy1.png"))
        elif objtype == self.allTypes[1]:
            cImport = pygame.image.load(os.path.join("Homescapes_Media", "candy2.png"))
        elif objtype == self.allTypes[2]:
            cImport = pygame.image.load(os.path.join("Homescapes_Media", "candy3.png"))
        #elif objtype == self.allTypes[3]:
            #cImport = pygame.image.load(os.path.join("Homescapes_Media", "candy3.png"))
        #elif objtype == self.allTypes[4]:
            #cImport = pygame.image.load(os.path.join("Homescapes_Media", "candy3.png"))

        self.cImg = pygame.transform.scale(cImport, (self.size, self.size))


    
    def fall(self, boxLimit, vel):        
        if self.y + (vel**2) < self.yHandles[boxLimit]:
            self.y += (vel**2)
        else:
            self.y = self.yHandles[boxLimit]


    def draw(self):
        win.blit(self.cImg, (self.x, self.y))


########################################################
class itemsControl():
    def __init__(self):
        self.falling = True
        self.checking = False

        self.pressedCol, self.pressedRow = 0, 0
        self.mosUp = True
        
        self.rows = mainGrid.rows
        self.cols = mainGrid.cols
        self.xHandles, self.yHandles = mainGrid.xHandles, mainGrid.yHandles
        self.emptysq = mainGrid.rows - 1
        self.spawnsq = self.yHandles[0] - boxSize

        self.vel = 0
        self.accel = 0.05

        self.mainList = []
        for i in range(self.cols):
            self.mainList.append([])



    def fillGrid(self, numFills, startCol, maxHandle):
        if self.vel < 3:
            self.vel += self.accel
            
        if len(self.mainList[0]) == 0 or self.mainList[startCol][0].y >= self.yHandles[1]:
            self.spawnFill(numFills, startCol)

        if len(self.mainList[0]) >= 1:
            for c in range(numFills):
                for r in range(len(self.mainList[startCol])):
                    self.mainList[c][r].fall(len(self.yHandles)-(len(self.mainList[0])-r), self.vel)

        if self.mainList[0][len(self.mainList[0])-1].y == self.yHandles[len(self.yHandles)-1] and len(self.mainList[0]) == self.rows and self.mainList[0][0].y == self.yHandles[1]:
            self.falling = False
            self.vel = 0
        
    
    def spawnFill(self, numFills, startCol):
        for i in range(numFills):
            typeSelection = [1, 2, 3]
            if numFills < self.cols - 2 or i > 1:
                if self.rowChecker(startCol + 1 + i) in typeSelection:
                    typeSelection.remove(self.rowChecker(startCol + 1 + i))
            
            if len(self.mainList[0]) > 2:
                if self.colChecker(startCol + 1 + i) in typeSelection:
                    typeSelection.remove(self.colChecker(startCol + 1 + i))
                
            self.mainList[startCol+i].insert(0, item(random.choice(typeSelection), self.xHandles[startCol + i], self.yHandles[0]))
            

    def rowChecker(self, currentCols):
        if self.mainList[currentCols-2][0].objtype==self.mainList[currentCols-3][0].objtype:
            return (self.mainList[currentCols-2][0].objtype)
        else: return None 


    def colChecker(self, currentCols):
        if self.mainList[currentCols-1][0].objtype == self.mainList[currentCols-1][1].objtype:
            return (self.mainList[currentCols-1][0].objtype)
        else: return None
    

    def boardDraw(self):
        for i in range(len(self.mainList)):
            for x in range(len(self.mainList[i])):
                self.mainList[i][x].draw()


#----board movement----#
    def ptsCheck(self):
        pass

    def colPtsCheck(self):
        pass

    def rowPtsCheck(self):
        pass


    def getSelection(self, pressed, mosX, mosY):
        if self.mosUp and pressed[0] and mainGrid.origin < mosX < mainGrid.origin + boxSize*mainGrid.cols and mainGrid.origin < mosY < mainGrid.origin + boxSize*mainGrid.rows:
            self.pressedCol = math.floor((mosX - mainGrid.origin) / boxSize) + 1
            self.pressedRow = math.floor((mosY - mainGrid.origin) / boxSize)+ 1
            pygame.draw.rect(win, (200, 200, 200), (mainGrid.xHandles[self.pressedCol-1] - mainGrid.cornerOffset, mainGrid.yHandles[self.pressedRow] - mainGrid.cornerOffset, boxSize, boxSize))
            self.mosUp = False

        

        
        elif self.mosUp == False and math.floor((mosX - mainGrid.origin) / boxSize) + 1 != self.pressedCol:
            self.swapCol = (math.floor((mosX - mainGrid.origin) / boxSize)) - self.pressedCol / abs((math.floor((mosX - mainGrid.origin) / boxSize)) - self.pressedCol)
            self.swapRow = 0

        elif self.mosUp == False and math.floor((mosY - mainGrid.origin) / boxSize) + 1 != self.pressedCol:
            self.swapCol = 0
            self.swapRow = -1


        elif self.mosUp == False and pressed[0]==False:
            self.mosUp = True
            self.pressedCol, self.pressedRow = 0, 0
            


    def selectionDraw(self):
        pass
    

########################################################
class grid():
    def __init__(self, cols, rows, origin):
        self.rows = rows
        self.cols = cols
        self.origin = origin
        self.thickness = 2

        self.sqsize = boxSize
        self.cornerOffset = math.ceil(self.sqsize/8)
        self.xHandles, self.yHandles = [], []
        for i in range(cols):
            self.xHandles.append(self.origin + self.sqsize*i + self.cornerOffset)
        for i in range(rows+1):
            self.yHandles.append(self.origin - self.sqsize + self.sqsize*i + self.cornerOffset)
        

    def draw(self):
        for i in range(self.cols + 1):
            xpos = self.origin + (self.sqsize*i-1)
            pygame.draw.line(win, (0, 0, 0), (xpos, self.origin), (xpos, self.origin + (self.sqsize*self.rows)), self.thickness)
            
        for x in range(self.rows + 1):
            ypos = self.origin + (self.sqsize*x-1)
            pygame.draw.line(win, (0, 0, 0), (self.origin, ypos), (self.origin + (self.sqsize*self.cols), ypos), self.thickness)

#########################################################
            

mainGrid = grid(10, 10, 80)
allItems = itemsControl()


run = True
while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    mosX, mosY = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
        
    

    if allItems.falling:
        #numFills, startCol, maxHandle
        allItems.fillGrid(allItems.cols, 0, len(allItems.yHandles)-1)

    elif allItems.checking:
        pass

    else:
        pass


    allItems.getSelection(pressed, mosX, mosY)


    # -- DRAW -- #
    win.fill((255,255,255))

    
    mainGrid.draw()
    #if pressed[0]:
        #allItems.selectionDraw()
    allItems.boardDraw()
    

    pygame.draw.rect(win, (255, 255, 255), (mainGrid.xHandles[0] - mainGrid.cornerOffset, mainGrid.yHandles[0] - mainGrid.cornerOffset - 1, boxSize*mainGrid.cols, boxSize))


    pygame.display.update()
    clock.tick(40)

pygame.quit()