import os, random, time

bParts = ["___","|   |","_I___I_","(-_-)","|","-|-", "|","[ ]"]

wrongGuessCt = 0
guessList = []
charList = []

##check how to create + add to list single line


def slow_print(text):
    for i in text:
        print(i, end='')
        speed = random.randrange(10)
        time.sleep(speed/100)
    time.sleep(0.2)


wordChoice = input("P1, enter your secret word: ").upper()
slow_print("Brilliant!\n" + ("\n")*10)

slow_print("H A N G M A N")
print("\n")


for i in range(len(wordChoice)):
    if wordChoice[i] == " ":
        charList.append("  ")
    else:
        charList.append("_")

#wordChoice = wordChoice.replace(" ", "")


while True:

    print(("\n"+("-==-"*4))*8)
    print("  -----|")
    for i in range(len(bParts)):
        print("  |    "+(" "*(4-int(len(bParts[i])/2)) + bParts[i]))
    print("  |\n[----]")
    print("\nWord:  " + (" ".join(charList)) + "\n")

    
    correct = False

    crtGuess = input("Enter your number " + str(len(guessList) + 1) + " guess: ").upper()
    try:
        while len(crtGuess) > 1 or crtGuess in guessList or type(int(crtGuess)) == int:
            crtGuess = input("hey silly boy. dont be so silly. guess again: ").upper()

    except ValueError:
        pass

    guessList.append(crtGuess)
    for i in range(len(wordChoice)):
        if wordChoice[i] == crtGuess:
            charList[i] = crtGuess
            correct = True

    if correct:
        slow_print("SLAYYYY")
        if "_" not in charList:
            slow_print("\nYou have won!" + "\n<"+(("".join(charList)+" ")*15)+">")
            break
    else:
        wrongGuessCt += 1
        slow_print("Rong numba silley o_o")
        if bParts[1] == "":
            slow_print("xD you #lose loser!!")
            print("\nx _______ x")
            break
            
        else:
            bParts[len(bParts)-wrongGuessCt] = ""            