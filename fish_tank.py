import pygame, time, random, os, pygame.freetype, math

pygame.init()
pygame.freetype.init()
wwid, whgt = 900, 500
win = pygame.display.set_mode((wwid,whgt))
clock = pygame.time.Clock()
pygame.display.set_caption('')

bgLoad = pygame.image.load(os.path.join("Fish_Media", "bg1.png"))
bgImg = pygame.transform.scale(bgLoad, (wwid, whgt))

bullLogo = pygame.image.load(os.path.join("Fish_Media", "ammoPack.png"))
logoImg = pygame.transform.scale(bullLogo, (35, 38))


class FishTank():
    def __init__(self):
        self.angle = 0
        self.vel = 0
        self.accel = 0.3
        
        self.RightSet = spritesheet("Rightfish_SS.png", "Fish_Media", 3, 3, 3)
        self.LeftSet = spritesheet("Leftfish_SS.png", "Fish_Media", 3, 3, 3)
        self.x = wwid/2
        self.y = whgt-(self.RightSet.cellHeight) + 2
        self.vector = 1
        self.index = 0

    def boundary(self):
        if self.vector == -1:
            if self.vel + self.x <= 0:
                self.vel = 0
        else:
            if self.x + self.vel >= wwid - self.RightSet.cellWidth:
                self.vel = 0
        
    def movement(self, vector):
        self.vector = vector
        if not (5*vector - 0.4 < self.vel < 5*vector + 0.4):
            self.vel += self.accel*self.vector

        self.boundary()
        self.x += self.vel
        self.index = round(abs(self.vel))


    def decel(self):
        self.boundary()
        
        if not (-0.4 < self.vel < 0.4):
            if self.vel > 0:
                self.vel -= self.accel
            else:
                self.vel += self.accel
            self.x += self.vel

        self.index = -1*round(abs(self.vel))



class TankCannon():
    def __init__(self):
        self.ExpSet = spritesheet("exp_sheet2.png", "Fish_Media", 2, 12, 1)
        self.index = 0
        self.y = fish.y + 80

        self.canShoot = True
        self.bullList = []
        self.initTime = pygame.time.get_ticks()
        self.fireRate = 300

        self.magMax = 15
        self.mag = self.magMax
        self.totalAmmo = 20
        

    def shotsAnimate(self):
        self.x = fish.x + (fish.RightSet.cellWidth/2) * (fish.vector + 1) - 20

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

        Textify((str(self.mag)+" / "+str(self.totalAmmo)), 30, wwid - 77, 37)



class bullet():
    def __init__(self, direction):
        self.direction = direction
        self.x = cannon.x + (self.direction - 1 * -10)
        self.speed = 20
        self.bullLoad = pygame.image.load(os.path.join("Fish_Media", "bullet_px.png"))
        self.img = pygame.transform.scale(self.bullLoad, (30, 15))
        self.bullRect = self.img.get_rect()
        self.bullfin = pygame.transform.rotate(self.img, (self.direction - 1)* 90)

    def move(self):
        self.x += self.direction * self.speed

    def draw(self):
        win.blit(self.bullfin, (round(self.x), round(cannon.y + 20)))
        
    def hitCheck(self):
        return False
        if (-1*self.bullRect.width > self.x) or (self.x > wwid):
            return True

class spritesheet:
    def __init__(self, filename, folder, size, cols, rows):
        self.load = pygame.image.load(os.path.join(folder,filename))
        left, top, initWid, initHgt = self.load.get_rect()
        self.sheet = pygame.transform.scale(self.load,(round(initWid/size), round(initHgt/size)))

        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        self.rect = self.sheet.get_rect() ##left, top, w, h
        w = self.cellWidth = self.rect.width / cols
        h = self.cellHeight = self.rect.height / rows + size * 0.15
        hw, hh = self.cellCenter = (w / 2, h / 2)

        self.cells = list([(index % cols * w, index // cols * h, w, h) for index in range(self.totalCellCount)])

    def draw(self, cellIndex, x, y):
        win.blit(self.sheet, (x, y), self.cells[cellIndex])



class upgrade():
    def __init__(self, image, w, h, x, index):
        self.lifespan = pygame.time.get_ticks()
        self.index = index
        self.w, self.h = w, h
        self.load = pygame.image.load(os.path.join("Fish_Media", image))
        self.resize = pygame.transform.scale(self.load, (w, h))

        self.x = x
        self.y = whgt - 130
        self.inc = 0

    def animate(self):
        self.y += math.sin(self.inc) * 2
        self.inc += 0.1
        win.blit(self.resize, (self.x, round(self.y)))

    def hitCheck(self):
        if fish.x <= self.x <= fish.x+fish.RightSet.cellWidth or fish.x <= self.x+self.w <= fish.x+fish.RightSet.cellWidth:
            return True

    def speedInc(self):
        self.lifespan = pygame.time.get_ticks()
                


def Textify(words, size, x, y):
    bitFont = pygame.freetype.Font(os.path.join("Fonts","8bitOperatorPlus8-Bold.ttf"), size)
    text, rect = bitFont.render(str(words), (0, 0, 0))
    x -= (rect.width)/2
    y -= (rect.height)/2
    win.blit(text, (round(x), round(y)))



def Timer(length, start):
    if start >= length:
        return True


fish = FishTank()
cannon = TankCannon()


#upgrade("speedUp.png", 50, 65, wwid-100, "speedBoost")
#upgrade("ammoPack.png", 60, 70, 200, "ammoBoost")

bUpgrades = [upgrade("ammoPack.png", 60, 70, 800, "ammoBoost")]

run = True

while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.blit(bgImg, (0, 0))


    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        fish.movement(1)

    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        fish.movement(-1)
        
    else:
        fish.decel()


    if keys[pygame.K_r] and cannon.totalAmmo > 0:
        if cannon.totalAmmo < cannon.magMax - cannon.mag:
            cannon.mag += cannon.totalAmmo
            cannon.totalAmmo = 0
        else:
            cannon.totalAmmo -= cannon.magMax - cannon.mag
            cannon.mag = cannon.magMax


    if fish.vector == 1:
        fish.RightSet.draw(fish.index, fish.x, fish.y)
    else:
        fish.LeftSet.draw(fish.index, fish.x, fish.y)

    if keys[pygame.K_SPACE] and cannon.canShoot == True and cannon.mag > 0:
        cannon.canShoot = False
        cannon.mag -= 1
        cannon.initTime = pygame.time.get_ticks()
        cannon.bullList.append(bullet(fish.vector))

    
    pygame.draw.rect(win, (0, 0, 0), (wwid - 174, 10, 161, 50))
    pygame.draw.rect(win, (200, 200, 200), (wwid - 172, 12, 157, 46))
    win.blit(logoImg, (wwid-170, 16))
    
    cannon.shotsAnimate()    

    popList = []
    for i in range(len(bUpgrades)):
        if bUpgrades[i].hitCheck() or pygame.time.get_ticks()-bUpgrades[i].lifespan > 1000:
            popList.append(i)
        bUpgrades[i].animate()
        
    for i in range(len(popList)):
        if bUpgrades[i].index == "ammoBoost":
            cannon.totalAmmo += 10
        elif bUpgrades[i].index == "speedBoost":
            pass
        
        bUpgrades.pop(popList[i])

    pygame.display.update()
    clock.tick(35)

pygame.quit()