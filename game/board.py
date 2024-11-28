import pygame
from .constants import *

def ermptyBoard():
    return ["0" for _ in range(19*19)]

def allJosekis():
    with open ("game/joseki.txt", "r") as f:
        josekis = [i[:-1] for i in f]
    return josekis

def translateToMoves(positioncode):
    moves = []
    for _ in range(len(positioncode)//3):
        moves.append(f"{positioncode[0]}{positioncode[1]}{positioncode[2]}")
        positioncode = positioncode[3:]
    return moves

def translateMoveToMouse(pos):
    if pos == "TEN": return "TEN"
    columns = "abcdefghjklmnopqrst"
    move = [columns.index(pos[0]), int(pos[1:])-1]
    return move

def translateListToPositioncode(moves):
    positioncode = ""
    for move in moves:
        positioncode += move
    return positioncode

class Board:

    def draw_goban(self, win):
        
        # DRAW BOARD
        win.fill(BOARD_COLOUR)
        pygame.draw.rect(win, BLACK, (BOARD_OFFSET+1, BOARD_OFFSET+1, WIDTH-SQUARE_SIZE-2, HEIGHT-SQUARE_SIZE-2), width = 1)
        for row in range(ROWS-1):
            for col in range(COLS-1):
                pygame.draw.rect(win, BLACK, ((row*SQUARE_SIZE) +BOARD_OFFSET, (col*SQUARE_SIZE) +BOARD_OFFSET, SQUARE_SIZE, SQUARE_SIZE), width = 1)
        for col in range(COLS_OF_DOTS):
            for row in range(ROWS_OF_DOTS):
                pygame.draw.circle(win, BLACK, (row*DIST_BETWEEN_DOTS + DOT_OFFSET, col*DIST_BETWEEN_DOTS + DOT_OFFSET), DOT_RADIUS)

        # DRAW BUTTONS
        tenuki = pygame.image.load("game/images/TENUKI.png").convert_alpha()
        test = pygame.image.load("game/images/TEST.png").convert_alpha()
        save = pygame.image.load("game/images/SAVE-JOSEKI.png").convert_alpha()
        delete = pygame.image.load("game/images/DELETE-JOSEKI.png").convert_alpha()
        undo = pygame.image.load("game/images/UNDO-MOVE.png").convert_alpha()
        clear = pygame.image.load("game/images/CLEAR-ALL.png").convert_alpha()
        buttonImages = [tenuki, test, save, delete, undo, clear]
        positions = [
            (BOARD_SIZE+PADDING, BOARD_OFFSET+564+PADDING), #tenuki
            (BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING, BOARD_OFFSET+564+PADDING), #test
            (BOARD_SIZE+PADDING, BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING), #save
            (BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING, BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING), #delete
            (BOARD_SIZE+PADDING, BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING+BUTTON_HEIGHT+PADDING), #undo
            (BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING, BOARD_OFFSET+564+PADDING+BUTTON_HEIGHT+PADDING+BUTTON_HEIGHT+PADDING) #clear
            ]
        for i in range(len(buttonImages)):
            image = buttonImages[i]
            rect = image.get_rect()
            x, y = positions[i][0], positions[i][1]
            rect.topleft = (x, y)
            win.blit(image, (rect.x, rect.y))

        # FILL SIDE PANEL
        panel = pygame.image.load("game/images/PANEL.png").convert_alpha()
        win.blit(panel, (BOARD_SIZE+PADDING, BOARD_OFFSET))

    def draw_piece(self, win, colour, move):
        x = SQUARE_SIZE * move[0] + BOARD_OFFSET
        y = SQUARE_SIZE * move[1] + BOARD_OFFSET
        pygame.draw.circle(win, colour, (x, y), PIECE_RADIUS)

    def draw_potential_piece(self, win, move):
        x = SQUARE_SIZE * move[0] + BOARD_OFFSET
        y = SQUARE_SIZE * move[1] + BOARD_OFFSET
        pygame.draw.circle(win, POTENTIAL, (x, y), PIECE_RADIUS//2)

    def draw_tenuki_dot(self, win):
        x = BOARD_SIZE+PADDING+BUTTON_WIDTH-53
        y = BOARD_OFFSET+564+PADDING+(BUTTON_HEIGHT//2)
        pygame.draw.circle(win, POTENTIAL, (x, y), PIECE_RADIUS)
    
    def drawTurnIndicator(self, win, colour):
        x = BOARD_SIZE+PADDING+BUTTON_WIDTH+PADDING+BUTTON_WIDTH-53
        y = BOARD_OFFSET+564+PADDING+(BUTTON_HEIGHT//2)
        pygame.draw.circle(win, colour, (x, y), PIECE_RADIUS)
    
    def check_captures(self, board, lastMove):

        global checked_positions, group
        checked_positions = []
        group = []

        def count_liberties(board, pos, liberties):
            
            def check_pieces(POSITION, liberties):
                if board[pos+POSITION] == colour and pos+POSITION not in group:
                    group.append(pos+POSITION)
                elif board[pos+POSITION] == "0":
                    liberties += 1
                return liberties

            checked_positions.append(pos)
            group.append(pos)
            if (pos-1)%19 < pos%19: liberties += check_pieces(-1, liberties)
            if (pos+1)%19 > pos%19: liberties += check_pieces(1, liberties)
            if pos-19 >= 0: liberties += check_pieces(-19, liberties)
            if pos+19 <= 360: liberties += check_pieces(19, liberties)
            
            for neighbour in group:
                if neighbour not in checked_positions: liberties += count_liberties(board, neighbour, liberties)
            return liberties

        for pos in range(len(board)):
            group = []
            liberties = 0
            if pos not in checked_positions:
                if board[pos] == "0":
                    checked_positions.append(pos)
                else:
                    colour = board[pos]
                    liberties = count_liberties(board, pos, 0)
                    if liberties == 0 and lastMove not in group:
                        for pos in group: board[pos] = "0"
        return board

    def isValid(self, move, moves):
        board = ermptyBoard()
        for m in moves:
            if m != "TEN":
                colour = "B" if max(index for index, item in enumerate(moves) if item == m)%2 == 0 else "W"
                m = translateMoveToMouse(m)
                pos = m[0] + m[1]*19
                board[pos] = colour
                board = self.check_captures(board, pos)
        move = translateMoveToMouse(move)
        if move == "TEN": return True
        pos = move[0] + move[1]*19
        if board[pos] == "0": return True
        return False

    def draw_board(self, win, moves, TESTING):
        self.draw_goban(win)
        board = ermptyBoard()
        for move in moves:
            colour = "B" if max(index for index, item in enumerate(moves) if item == move)%2 == 0 else "W"
            move = translateMoveToMouse(move)
            if move != "TEN":
                pos = move[0] + move[1]*19
                board[pos] = colour
                board = self.check_captures(board, pos)

        for pos in range(len(board)):
            if board[pos] != "0":
                colour = BLACK if board[pos] == "B" else WHITE
                move = [pos%19, pos//19]
                self.draw_piece(win, colour, move)

        # DISPLAYING POTENTIAL MOVES IF NOT IN TEST MODE
        if TESTING == False:
            josekiList = allJosekis()
            newJosekiList = []
            for joseki in josekiList:
                josekiMoves = translateToMoves(joseki)
                if len(josekiMoves) > len(moves):
                    if len(moves) == 0:
                        while len(josekiMoves) != len(moves)+1:
                            josekiMoves = josekiMoves[:-1]
                        newJosekiList.append(josekiMoves)
                    elif len(moves) > 0:
                        if josekiMoves[:len(moves)] == moves:
                            while len(josekiMoves) != len(moves)+1:
                                josekiMoves = josekiMoves[:-1]
                            newJosekiList.append(josekiMoves)
            for joseki in newJosekiList:
                move = translateMoveToMouse(joseki[-1])
                if move != "TEN":
                    self.draw_potential_piece(win, move)
                else: self.draw_tenuki_dot(win)
        
        if TESTING == True:
            colour = BLACK if len(moves)%2 == 0 else WHITE
            self.drawTurnIndicator(win, colour)
