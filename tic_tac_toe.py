import time, random, math

def slow_print(text):
    for i in text:
        print(i, end='')
        speed = random.randrange(10)
        time.sleep(speed/500)
    time.sleep(0.1)


def continueCheck():
    global board, p1, p2, running, skipRest
    if input("Play again? (Y or N) ").upper() == "Y":
        board.reset()
        p1.choice = -1
        p2.choice = -1
    else:
        running = False


class boardType():
    def __init__(self, dims):

        self.dims = dims
        self.boardList = []
        self.openSlots = []
        self.reset()


    def reset(self):
        self.boardList = []
        self.openSlots = []
        for row in range(self.dims):
            subList = []
    
            for col in range(self.dims):
                subList.append(".")
            self.boardList.append(subList)

        for i in range(len(self.boardList) * len(self.boardList[0])):
            self.openSlots.append(i + 1)
        


    def print(self):
        print("   " + "|   " * (self.dims - 1))
        for i in range(len(self.boardList)):
            print("", " | ".join(self.boardList[i]))
            if i < len(self.boardList)-1:
                print("---" + "|---" * (self.dims - 1))
            else:
                print("   " + "|   " * (self.dims -1))


    def guidePrint(self):
        print("\nboard guide: ")
        for i in range(self.dims * self.dims):
            print("|" + (" "*(3-len(str(i+1))) ) + str(i + 1), end = "")
            if (i+1) % self.dims == 0:
                print("")
        

    def filledCheck(self):
        if len(self.openSlots) == 0:
            print("board is filled :(\n\n")
            continueCheck()
            return True

    def getGrid(self, num):
        rowNum = math.floor((num - 1) / self.dims)
        colNum = (num-1) % self.dims
        return (rowNum, colNum)


        

class playerType():
    def __init__(self, name, tack):
        self.name = name
        self.tack = tack
        self.wins = 0
        self.choice = -1

    def getChoice(self):
        global board
        while self.choice not in board.openSlots:
            while True:
                try:
                    self.choice = int(input(self.name + ", enter your next play: "))
                    break
                except ValueError:
                    print("that numpa doesn work !!") 
        board.openSlots.remove(self.choice)
        board.boardList[board.getGrid(self.choice)[0]].pop(board.getGrid(self.choice)[1])
        board.boardList[board.getGrid(self.choice)[0]].insert(board.getGrid(self.choice)[1], self.tack)


    def winCheck(self):
        if self.diagonalCheck() or self.lineCheck():
            self.wins += 1
            print(self.name + " WINS!! \n------------------\n")
            continueCheck()
            return True


    def diagonalCheck(self):
        global board
        if board.getGrid(self.choice)[0] == board.getGrid(self.choice)[1]:
            
            i = 0
            while (board.boardList[i][i] == self.tack):
                    if i == (board.dims - 1):
                        return True
                    i += 1

        elif board.getGrid(self.choice)[0] + board.getGrid(self.choice)[1] == 2:

            i = 0
            while (board.boardList[i][2 - i] == self.tack):
                    if i == (board.dims - 1):
                        return True
                    i += 1
        return False
    


    def lineCheck(self):
        ##horizontal
        i = 0
        while (board.boardList[board.getGrid(self.choice)[0]][i] == self.tack):
            if i == (board.dims - 1):
                    return True
            i += 1

        ##vertical
        i = 0
        while(board.boardList[i][board.getGrid(self.choice)[1]] == self.tack):
                if i == (board.dims - 1):
                    return True
                i += 1
        return False
                
        
        

        
running = True
skipRest = False

p1 = playerType("player 1", "X")
p2 = playerType("player 2", "O")
board = boardType(3)

board.print()
board.guidePrint()
while running:
    
    p1.getChoice()
    board.print()
    if p1.winCheck():
        skipRest = True

    
    if not skipRest:
        board.filledCheck()
        
        p2.getChoice()
        board.print()
        p2.winCheck()

        board.filledCheck()

    skipRest = False
    