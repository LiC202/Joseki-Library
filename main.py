# Project

#####IMPORTS#####################################################################################################################################################################################

import os
import random
import pygame
from game.constants import *
from game.board import *


 ####   ###    ###   ####   ####    ####
#      #   #  #   #  #   #  #   #  #    
#      #   #  #   #  ####   #   #   ### 
#      #   #  #   #  #   #  #   #      #
 ####   ###    ###   #   #  ####   ####
#####COORDINATES#################################################################################################################################################################################

# TRANSLATES A POSITION CODE INTO A LIST OF MOVES
def translateToMoves(positioncode):
    moves = []
    for _ in range(len(positioncode)//3):
        moves.append(f"{positioncode[0]}{positioncode[1]}{positioncode[2]}")
        positioncode = positioncode[3:]
    return moves

# TRANSLATES A LIST OF MOVES INTO A POSITION CODE
def translateListToPositioncode(moves):
    positioncode = ""
    for move in moves:
        positioncode += move
    return positioncode

def translateMouseToMove(pos):
    if pos == "TEN": return "TEN"
    columns = "abcdefghjklmnopqrst"
    move = f"{columns[pos[0]]}{pos[1]+1}"
    if len(move) == 2: move = f"{move[0]}0{move[1]}"
    return move

def translateMoveToMouse(pos):
    if pos == "TEN": return "TEN"
    columns = "abcdefghjklmnopqrst"
    move = [columns.index(pos[0]), int(pos[1:])-1]
    return move



#####  #####  #      #####
#        #    #      #
###      #    #      ###
#        #    #      #
#      #####  #####  #####
#####SAVING TO FILE##############################################################################################################################################################################

# MIRRORS A JOSEKI
def mirror(joseki):
    joseki = translateToMoves(joseki)
    newJoseki = []
    for move in joseki:
        move = translateMoveToMouse(move)
        move[0], move[1] = move[1], move[0]
        move = translateMouseToMove(move)
        newJoseki.append(move)
    newJoseki = translateListToPositioncode(newJoseki)
    return newJoseki

# ROTATES A JOSEKI
def rotate90(joseki):
    joseki = translateToMoves(joseki)
    newJoseki = []
    for move in joseki:
        move = translateMoveToMouse(move)
        move[0], move[1] = 18-move[1], move[0]
        move = translateMouseToMove(move)
        newJoseki.append(move)
    newJoseki = translateListToPositioncode(newJoseki)
    return newJoseki

def getNewJosekis(joseki):
    newJosekis = []
    newJosekis.append(joseki)
    newJosekis.append(rotate90(joseki))
    newJosekis.append(rotate90(rotate90(joseki)))
    newJosekis.append(rotate90(rotate90(rotate90(joseki))))
    for j in range(4):
        newJosekis.append(mirror(newJosekis[j]))
    return newJosekis


# SAVES A JOSKI TO THE JOSEKI FILE
def saveJoseki(joseki):
    josekis = getNewJosekis(joseki)
    with open ("game/joseki.txt", "a") as f:
        for joseki in josekis:
            f.writelines(f"{joseki}\n")

# CLEARS THE JOSEKI FILE
def clearData():
    os.remove("game/joseki.txt")
    with open("game/joseki.txt", "w"):
        pass

# READS ALL JOSEKI POSITIONCODES
def allJosekis():
    with open ("game/joseki.txt", "r") as f:
        josekis = [i[:-1] for i in f]
    return josekis



#####  #####   ####  #####
  #    #      #        #
  #    ###     ###     #
  #    #          #    #
  #    #####  ####     #
#####TEST JOSEKI#################################################################################################################################################################################

def checkInputMove(move, moves, josekiList):
    correct = False
    mvs = moves
    mvs.append(move)
    for joseki in josekiList:
        joseki = translateToMoves(joseki)
        if len(joseki) >= len(mvs):
            if joseki[:len(mvs)] == mvs: correct = True
    return correct



 ####   ###   ## ##  #####
#      #   #  # # #  #
# ###  #####  # # #  ###
#   #  #   #  # # #  #
 ###   #   #  # # #  #####
#####GAME########################################################################################################################################################################################

FPS = 60
WIN = pygame.display.set_mode((WIDTH + 640, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Joseki Library")


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    TESTING = False
    moves = []
    
    while run:
        clock.tick(FPS)
        josekiList = allJosekis()

        # UPDATE
        board.draw_board(WIN, moves, TESTING)
        pygame.display.update()

        # EVENTS
        for event in pygame.event.get():

            # QUIT
            if event.type == pygame.QUIT: run = False

            # CLICK
            if event.type == pygame.MOUSEBUTTONDOWN:
                ORIGINALmousepos = pygame.mouse.get_pos()
                mousex = ORIGINALmousepos[0]//SQUARE_SIZE
                mousey = ORIGINALmousepos[1]//SQUARE_SIZE
                mousepos = [mousex, mousey]

                inrange = True if mousex <= 19 and mousey <= 19 else False
                
                x = ORIGINALmousepos[0]
                y = ORIGINALmousepos[1]

                if inrange or (x >= BOARD_SIZE+PADDING and x <= BOARD_SIZE+PADDING+BUTTON_WIDTH and y >= BOARD_OFFSET+564+PADDING and y <= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT):
                    
                    if x >= BOARD_SIZE+PADDING and x <= BOARD_SIZE+PADDING+BUTTON_WIDTH and y >= BOARD_OFFSET+564+PADDING and y <= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT:
                        move = "TEN"
                    elif inrange:
                        move = translateMouseToMove(mousepos)
                    
                    if board.isValid(move, moves):
                        if TESTING == False:
                            moves.append(move)
                        else:
                            if checkInputMove(move, moves, josekiList): # CORRECT
                                pass
                            else: # WRONG
                                moves.pop()
                            TESTING = False
                            print(moves)

                else:

                    x = ORIGINALmousepos[0]
                    y = ORIGINALmousepos[1]

                    if x >= BOARD_SIZE+PADDING and x <= BOARD_SIZE+PADDING+BUTTON_WIDTH and y >= BOARD_OFFSET+564+PADDING and y <= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT:
                        # TENUKI
                        moves.append("TEN")

                    elif x >= BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING and x <= BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING+BUTTON_WIDTH and y >= BOARD_OFFSET+564+PADDING and y <= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT:
                        # TEST
                        if len(josekiList) > 0:
                            TESTING = True
                            chosenjoseki = random.choice(josekiList)
                            moves = translateToMoves(chosenjoseki)
                            moves = moves[:random.randint(1, len(moves)-1)]
                
                    elif x >= BOARD_SIZE+PADDING and x <= BOARD_SIZE+PADDING+BUTTON_WIDTH and y >= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING and y <= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+BUTTON_HEIGHT+PADDING:
                        # SAVE JOSEKI
                        joseki = translateListToPositioncode(moves)
                        if joseki not in josekiList:
                            saveJoseki(joseki)

                    elif x >= BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING and x <= BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING+BUTTON_WIDTH and y >= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING and y <= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING+BUTTON_HEIGHT:
                        # DELETE JOSEKI
                        joseki = translateListToPositioncode(moves)
                        if joseki in josekiList:
                            josekiList.remove(joseki)
                            clearData()
                            for j in josekiList:
                                saveJoseki(j)

                    elif x >= BOARD_SIZE+PADDING and x <= BOARD_SIZE+PADDING+BUTTON_WIDTH and y >= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING+BUTTON_HEIGHT+PADDING and y <= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING+BUTTON_HEIGHT+BUTTON_HEIGHT+PADDING:
                        # UNDO MOVE
                        if moves != []: moves.pop()

                    elif x >= BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING and x <= BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING+BUTTON_WIDTH and y >= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING+BUTTON_HEIGHT+PADDING and y <= BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING+BUTTON_HEIGHT+BUTTON_HEIGHT+PADDING:
                        # CLEAR ALL
                        moves = []
    
    pygame.quit()

main()
