import pygame
from utils import spritesheet, Textify

class FishTank():
    def __init__(self, wwid, whgt, win):
        #self.cannon = TankCannon(wwid,whgt,win) #add
        self.bullList = []

        self.RightSet = spritesheet("Rightfish_SS.png", 3, 3, 3, win)
        self.LeftSet = spritesheet("Leftfish_SS.png", 3, 3, 3, win)
        self.index = 0 #spritesheet location shit

        self.wwid = wwid
        self.whgt = whgt
        self.x = wwid/2
        self.y = whgt - (self.RightSet.cellHeight) + 2

        self.dir = 1
        self.vel = 0
        self.accel = 0.2

    def setBound(self):
        if self.dir == -1:
            if self.vel + self.x <= 0:
                self.vel = 0
                self.x = 0
        else:
            if self.x + self.vel >= self.wwid - self.RightSet.cellWidth:
                self.vel = 0
                self.x = self.wwid - self.RightSet.cellWidth
    
    def setDir(self, keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dir = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dir = -1
        else:
            self.decel()
            print("sloweing")


    def move(self):
        if (abs(self.vel) < 4):
            self.vel += self.accel * self.dir

        self.x += self.vel
        self.index = round(abs(self.vel))
        self.setBound()


    def decel(self):
        if self.vel != 0:
            self.vel += self.dir * -1 * self.accel

        if abs(self.vel) < 0.3: self.vel = 0

        self.index = -1 * round(abs(self.vel))
        self.setBound()

    def draw(self):
        if self.dir == 1:
            self.RightSet.draw(self.index, self.x, self.y)
        else:
            self.LeftSet.draw(self.index, self.x, self.y)



class TankCannon():
    def __init__(self, wwid, whgt, win):
        self.wwid = wwid
        self.whgt = whgt
        self.win = win
        self.ExpSet = spritesheet("exp_sheet2.png", 2, 12, 1, win)
        self.index = 0
        #self.fish = pass
        #self.x = 3

        self.canShoot = True
        self.bullList = []
        self.initTime = pygame.time.get_ticks()
        self.fireRate = 300

        self.magMax = 15
        self.mag = self.magMax
        self.totalAmmo = 20
        

    def shotsAnimate(self):
        self.x = self.fish.x + (self.fish.RightSet.cellWidth/2) * (self.fish.vector + 1) - 20

        if len(self.bullList) > 0:
            popList = []
            for i in range(len(self.bullList)):
                self.bullList[i].move()
                if self.bullList[i].hitCheck():
                    popList.append(i)  
                else:
                    self.bullList[i].draw()

            for i in range(len(popList)):
                self.bullList.pop(i)


        if self.canShoot == False and self.index < self.ExpSet.totalCellCount - 1:
            self.index += 1
            self.ExpSet.draw(self.index, self.x, self.y)


        if pygame.time.get_ticks()-self.initTime >= self.fireRate:
            self.canShoot = True
            self.index = 0

        Textify((str(self.mag)+" / "+str(self.totalAmmo)), 30, self.wwid - 77, 37, self.win)



class bullet():
    def __init__(self, direction, cannon, win):
        self.cannon = cannon
        self.win = win

        self.direction = direction
        self.x = self.cannon.x + (self.direction - 1 * -10)
        self.speed = 20
        self.bullLoad = pygame.image.load("bullet_px.png")
        self.img = pygame.transform.scale(self.bullLoad, (30, 15))
        self.bullRect = self.img.get_rect()
        self.bullfin = pygame.transform.rotate(self.img, (self.direction - 1)* 90)

    def move(self):
        self.x += self.direction * self.speed

    def draw(self):
        self.win.blit(self.bullfin, (round(self.x), round(self.cannon.y + 20)))
        
    def hitCheck(self):
        return False
        if (-1*self.bullRect.width > self.x) or (self.x > wwid):
            return True
