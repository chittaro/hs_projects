import pygame, time, random, os, pygame.freetype, math
from tank import FishTank
from utils import upgrade

pygame.init()
pygame.freetype.init()
wwid, whgt = 900, 500
win = pygame.display.set_mode((wwid,whgt))
clock = pygame.time.Clock()
pygame.display.set_caption('')

bgLoad = pygame.image.load("bg1.png")
bgImg = pygame.transform.scale(bgLoad, (wwid, whgt))

bullLogo = pygame.image.load("ammoPack.png")
logoImg = pygame.transform.scale(bullLogo, (35, 38))
        

        

fish = FishTank(wwid, whgt, win)
#cannon = TankCannon(wwid, whgt, fish, win)


#upgrade("speedUp.png", 50, 65, wwid-100, "speedBoost")
#upgrade("ammoPack.png", 60, 70, 200, "ammoBoost")

#bUpgrades = [upgrade("ammoPack.png", 60, 70, 800, "ammoBoost", whgt, win)]

run = True

while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.blit(bgImg, (0, 0))


    keys = pygame.key.get_pressed()
    fish.setDir(keys)

    fish.move()


    #if keys[pygame.K_r] and cannon.totalAmmo > 0:
    #    if cannon.totalAmmo < cannon.magMax - cannon.mag:
    #        cannon.mag += cannon.totalAmmo
    #       cannon.totalAmmo = 0
    #    else:
    #        cannon.totalAmmo -= cannon.magMax - cannon.mag
    #        cannon.mag = cannon.magMax



    fish.draw()

    pygame.draw.rect(win, (0, 0, 0), (wwid - 174, 10, 161, 50))
    pygame.draw.rect(win, (200, 200, 200), (wwid - 172, 12, 157, 46))
    win.blit(logoImg, (wwid-170, 16))

    pygame.display.update()
    clock.tick(35)

pygame.quit()
