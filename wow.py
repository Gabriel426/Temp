import pygame
import random
import sys
from pygame.locals import *
pygame.init()

#Screen
WINDOWWIDTH = 900
WINDOWHEIGHT = 700
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Welcome to Card Game")

#Background
White = (255,255,255)
Green = (0, 51, 0)
boxColor = White
bgcolor = Green
screen.fill(bgcolor)
mouse_x = 0
mouse_y = 0
#Card
cd1 = pygame.image.load('C:/Users/hp/Pictures/0.png').convert()
cd2 = pygame.image.load("C:/Users/hp/Pictures/1.png").convert()
cd3 = pygame.image.load("C:/Users/hp/Pictures/2.png").convert()
CardSize = 120
GapSize = 50
cardWidth = 2
cardHeight = 3
firstSelection = 0,0
marginX = int((900 - (cardWidth * (CardSize + GapSize)))/2)
marginY = int((700- (cardHeight * (CardSize + GapSize)))/2)

def revealCardsData(val):
    revealedCards = []
    for i in range(cardWidth):
        revealedCards.append([val] * cardHeight)
    return revealedCards

#Shuffle the Card
CardList = [1,2,3]
PositionList = [[(200,100), (200,300), (200,500)], [(500,100), (500,300), (500,500)]]
ListRecord = []
coveredCard = revealCardsData(False)

def addOne(count1, count2, count3):
    count1    += 1
    count2    += 1
    if count3[0] == 0 and count3[1] < 2:
        count3[1] += 1
    elif count3[0] == 0 and count3[1] == 2:
        count3[0] += 1
        count3[1] =  0
    else:
        count3[1] += 1
    return count1,count2,count3

def randomCards():
    c = random.choice(CardList)
    ListRecord.append(c)
    if ListRecord.count(c) > 2:
        CardList.remove(c)
        ListRecord.pop()
        return randomCards()
    elif len(ListRecord) < 6:
        return randomCards()
    else:
        return ListRecord

cCard  = 0
cCover = 0
cPos   = [0, 0]
ListRecord = randomCards()
for card in ListRecord:
    if not coveredCard[0][cCover]:
        pygame.draw.rect(screen, boxColor, (PositionList[cPos[0]][cPos[1]][0], PositionList[cPos[0]][cPos[1]][1], CardSize, CardSize))
        addOne(cCard, cCover, cPos)
    else:
        if card == 1:
            screen.blit(cd1, (PositionList[cPos[0]][cPos[1]][0], PositionList[cPos[0]][cPos[1]][1]))
            addOne(cCard, cCover, cPos)
        elif card == 2:
            screen.blit(cd2, (PositionList[cPos[0]][cPos[1]][0], PositionList[cPos[0]][cPos[1]][1]))
            addOne(cCard, cCover, cPos)
        else:
            screen.blit(cd3, (PositionList[cPos[0]][cPos[1]][0], PositionList[cPos[0]][cPos[1]][1]))
            addOne(cCard, cCover, cPos)
pygame.display.update()

def leftTopcardCoords(card_x,card_y):
    left = card_x * (CardSize + GapSize) + marginX
    top = card_y * (CardSize + GapSize) + marginY
    return (left,top)

def cardCoords(x,y):
    for card_x in range(cardWidth):
        for card_y in range(cardHeight):
            left, top = leftTopcardCoords(card_x,card_y)
            boardRect = pygame.Rect(left, top, CardSize, CardSize)
            if boardRect.collidepoint(x,y):
                return (card_x, card_y)
    return (None, None)

def cardCover(cards):
    return None

def revealCardAnimation(coverage):
    for coverage in range(CardSize,-5):
        cardCover(revealCards)

def coverCardAnimation():
    for coverange in range(0, CardSize):
        cardCover(revealCards)

def Win(revealCards):
    for r in revealCards:
        if False in r:
            return False
    return True

def gameWinAnimation():
    font = pygame.font.Font(None, 50)
    text = font.render("You Win the Game!", True, White, None)
    textRect = text.get_rect()
    textRect.center = (300,300)
    screen.fill(Green)
    screen.blit(text, textRect)

    coveredCard = revealCardsData(False)

while True:
    mouseClicked = False


    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        elif event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            mouseClicked = True

    card_x, card_y = cardCoords(mouse_x, mouse_y)
    if card_x != None and card_y != None:
        revealCards = revealCardsData(False)
        if not revealCards[card_x][card_y] and mouseClicked:
            revealCardAnimation([(card_x, card_y)])
            revealCards[card_x][card_y] = True
            if firstSelection == None:
                firstSelection = (card_x,card_y)
            else:
                card1 = firstSelection[0], firstSelection[1]
                card2 = card_x, card_y
            if card1 != card2:
                pygame.time.wait(500)
                coverCardAnimation()
                revealCards[card_x][card_y] = False
            elif Win(revealCards):
                gameWinAnimation()

    pygame.display.update()
