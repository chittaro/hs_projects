import pygame, math

class spritesheet:
    def __init__(self, filename, size, cols, rows, win):
        self.win = win
        self.load = pygame.image.load(filename)
        left, top, initWid, initHgt = self.load.get_rect()
        self.win = win
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
        self.win.blit(self.sheet, (x, y), self.cells[cellIndex])



class upgrade():
    def __init__(self, image, w, h, x, index, whgt, win):
        self.load = pygame.image.load(image)
        self.resize = pygame.transform.scale(self.load, (w, h))

        self.birthday = pygame.time.get_ticks()
        self.w, self.h = w, h
        self.win = win
        self.index = index

        self.x = x
        self.y = whgt - 130
        self.inc = 0

    def animate(self):
        self.y += math.sin(self.inc) * 2
        self.inc += 0.1
        self.win.blit(self.resize, (self.x, round(self.y)))

    def getLife(self):
        return pygame.time.get_ticks() - self.birthday


                


def Textify(words, size, x, y, win):
    bitFont = pygame.freetype.Font("8bitOperatorPlus8-Bold.ttf", size)
    text, rect = bitFont.render(str(words), (0, 0, 0))
    x -= (rect.width)/2
    y -= (rect.height)/2
    win.blit(text, (round(x), round(y)))


