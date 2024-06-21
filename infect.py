from pygame import *
from os import environ
import sys
import random 
import copy
init()

sys.setrecursionlimit(9000000)

inf=display.Info()
w,h=inf.current_w,inf.current_h
environ['SDL_VIDEO_WINDOW_POS']='350,30'

RED=(255,0,0)

GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)
MYYELLOW=(204,224,90)

size=(900,650)
screen=display.set_mode(size)

display.set_caption("Chain Infect")

#----------VARIABLES-----------#

mode='title'
rectList=[]
row = 6
col = 9
board=[[[0,0] for i in range(col)]for l in range(row)]
leftClick=False
playerTurn1=1
alivePlayers=[]

count=0
colours = [(255,0,0), (0, 255, 0), (0, 0, 255), (252,241,32)]
players=0
game=False
turnCol=(255,0,0)
boardCol=(255,0,0)
running=True

#--------------images-------------#
titlePic=image.load("images/menu/start.jpeg")
bigInfectedPic=image.load("images/menu/bigInfectedPic.png")
infectedPic=image.load("images/menu/infectedPic.png")
playPic=image.load("images/menu/playPic.png")
numOfPlayers=image.load("images/menu/numOfPlayers.png")
player2=image.load("images/menu/2Player.png")
player3=image.load("images/menu/3Player.png")
player4=image.load("images/menu/4Player.png")
rMine=image.load("images/mines/red/rMine.png")
gMine=image.load("images/mines/green/gMine.png")
bMine=image.load("images/mines/blue/bMine.png")
yMine=image.load("images/mines/yellow/yMine.png")
rrMine=image.load("images/mines/red/rrMine.png")
ggMine=image.load("images/mines/green/ggMine.png")
bbMine=image.load("images/mines/blue/bbMine.png")
yyMine=image.load("images/mines/yellow/yyMine.png")
rrrMine=image.load("images/mines/red/rrrMine.png")
gggMine=image.load("images/mines/green/gggMine.png")
bbbMine=image.load("images/mines/blue/bbbMine.png")
yyyMine=image.load("images/mines/yellow/yyyMine.png")
redWin=image.load("images/menu/redWin.png")
greenWin=image.load("images/menu/greenWin.png")
blueWin=image.load("images/menu/blueWin.png")
yellowWin=image.load("images/menu/yellowWin.png")
returnPic=image.load("images/menu/returnPic.png")
cornerEx=image.load("images/menu/cornerEx.png")
edgeEx=image.load("images/menu/edgeEx.png")
middleEx=image.load("images/menu/middleEx.png")
cornerText=image.load("images/menu/cornerText.png")
edgeText=image.load("images/menu/edgeText.png")
middleText=image.load("images/menu/middleText.png")
objectiveText=image.load("images/menu/objectiveText.png")
controlText=image.load("images/menu/controlText.png")

#-------------Rectangles------------#

playRect=Rect(340,390,190,70)
player2Rect=Rect(315,285,42,50)
player3Rect=Rect(415,285,42,50)
player4Rect=Rect(515,285,45,50)
gameRect=Rect(105,145,75*col,75*row)
winnerSub=screen.copy().subsurface(gameRect)
pieceImages={
    1 : [rMine,rrMine,rrrMine],
    2 : [gMine,ggMine,gggMine],
    3 : [bMine,bbMine,bbbMine],
    4 : [yMine,yyMine,yyyMine]}

def drawBoard(colr):
    for x in range(col):
        for y in range(row):
            draw.rect(screen,colr,(105+x*75,145+y*75,75,75),2)
         

def isCorner(x, y):
    if [x, y] == [0, 0] or [x, y] == [col-1, 0] or [x, y] == [0, row-1] or [x, y] == [col-1, row-1]:
        return True
    else:
         return False

def isEdge(x, y):
    if not isCorner(x, y):
        if y == row-1  or x == col-1 or y == 0 or x == 0:
            return True
    else:
         return False

def drawPieces(board):
    draw.rect(screen,BLACK,gameRect)
    for y in range(row):
        for x in range(col):
            placeX=x*75+110
            placeY=y*75+150
            placeType = board[y][x][0]
            numPieces = board[y][x][1]
            if placeType != 0:
                screen.blit(pieceImages[placeType][numPieces-1],(placeX,placeY))


def generate_population(size):
    population = []
    for x in range(col):
        for y in range(row):
            if board[y][x][0] == 0 or board[y][x][0] == player:
                population.append((x, y))
    return population

def evaluate_fitness( player, candidate):
    global board
    x, y = candidate
    if board[y][x][0] == player or board[y][x][0] == 0:
        board_copy = copy.deepcopy(board)
        dummy_add(x, y, player)
        fitness = evaluate_board(board, player)
        board = copy.deepcopy(board_copy)
        return fitness
    else:
        return float('-inf')

def rank_based_selection(population, fitness_scores, num_parents):
    ranked_population = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
    parents = [x[0] for x in ranked_population[:num_parents]]
    return parents

def crossover(parent1, parent2):
    child1 = (random.randint(0, col - 1), random.randint(0, row - 1))
    child2 = (random.randint(0, col - 1), random.randint(0, row - 1))
    return child1, child2

def mutate(candidate, mutation_rate):
    if random.random() < mutation_rate:
        x, y = candidate
        while board[y][x][0] != 0 and board[y][x][0] != player:
            x, y = random.randint(0, col - 1), random.randint(0, row - 1)
        return (x, y)
    else:
        return candidate

def genetic_algorithm(board, player, population_size, num_parents, num_generations, mutation_rate):
    population = generate_population(population_size)
    best_move = None
    best_score = float('-inf')
    all_candidate_moves = []

    for _ in range(num_generations):
        fitness_scores = [evaluate_fitness(player, candidate) for candidate in population]
        parents = rank_based_selection(population, fitness_scores, num_parents)

        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)

        population = new_population
        best_candidate = population[fitness_scores.index(max(fitness_scores))]
        best_score = max(fitness_scores)
        all_candidate_moves.append(best_candidate)
        if best_score > evaluate_board(board, player):
            best_move = best_candidate

    return all_candidate_moves

# Define the dummy_add and related explosion functions
def dummy_add(x, y, playerTurn1):
   
    if board[y][x][1] == 0:
        board[y][x] = [playerTurn1, 1]
    elif board[y][x][0] == playerTurn1:
        if isCorner(x, y):
            dummy_explodeCorner(x, y, playerTurn1, alivePlayers)
        elif isEdge(x, y):
            if board[y][x][1] < 2:
                board[y][x][1] += 1
            else:
                dummy_explodeEdge(x, y, playerTurn1, alivePlayers)
        else:
            if board[y][x][1] < 3:
                board[y][x][1] += 1
            else:
                dummy_explodeMiddle(x, y, playerTurn1, alivePlayers)

def dummy_explodeCorner(x, y, playerTurn1, alivePlayers):
    
    board[y][x] = [0, 0]
    if [x, y] == [0, 0]:
        board[y+1][x][0] = playerTurn1
        dummy_explodeAdd(x, y+1, x, y, playerTurn1, alivePlayers)
        board[y][x+1][0] = playerTurn1
        dummy_explodeAdd(x+1, y, x, y, playerTurn1, alivePlayers)
    elif [x, y] == [col-1, 0]:
        board[y+1][x][0] = playerTurn1
        dummy_explodeAdd(x, y+1, x, y, playerTurn1, alivePlayers)
        board[y][x-1][0] = playerTurn1
        dummy_explodeAdd(x-1, y, x, y, playerTurn1, alivePlayers)
    elif [x, y] == [0, row-1]:
        board[y-1][x][0] = playerTurn1
        dummy_explodeAdd(x, y-1, x, y, playerTurn1, alivePlayers)
        board[y][x+1][0] = playerTurn1
        dummy_explodeAdd(x+1, y, x, y, playerTurn1, alivePlayers)
    elif [x, y] == [col-1, row-1]:
        board[y-1][x][0] = playerTurn1
        dummy_explodeAdd(x, y-1, x, y, playerTurn1, alivePlayers)
        board[y][x-1][0] = playerTurn1
        dummy_explodeAdd(x-1, y, x, y, playerTurn1, alivePlayers)

def dummy_explodeEdge(x, y, playerTurn1, alivePlayers):
    board[y][x] = [0, 0]
    if x == 0:
        board[y+1][x][0] = playerTurn1
        dummy_explodeAdd(x, y+1, x, y, playerTurn1, alivePlayers)
        board[y][x+1][0] = playerTurn1
        dummy_explodeAdd(x+1, y, x, y, playerTurn1, alivePlayers)
        board[y-1][x][0] = playerTurn1
        dummy_explodeAdd(x, y-1, x, y, playerTurn1, alivePlayers)
    elif x == col-1:
        board[y+1][x][0] = playerTurn1
        dummy_explodeAdd(x, y+1, x, y, playerTurn1, alivePlayers)
        board[y][x-1][0] = playerTurn1
        dummy_explodeAdd(x-1, y, x, y, playerTurn1, alivePlayers)
        board[y-1][x][0] = playerTurn1
        dummy_explodeAdd(x, y-1, x, y, playerTurn1, alivePlayers)
    elif y == 0:
        board[y+1][x][0] = playerTurn1
        dummy_explodeAdd(x, y+1, x, y, playerTurn1, alivePlayers)
        board[y][x+1][0] = playerTurn1
        dummy_explodeAdd(x+1, y, x, y, playerTurn1, alivePlayers)
        board[y][x-1][0] = playerTurn1
        dummy_explodeAdd(x-1, y, x, y, playerTurn1, alivePlayers)
    elif y == row-1:
        board[y-1][x][0] = playerTurn1
        dummy_explodeAdd(x, y-1, x, y, playerTurn1, alivePlayers)
        board[y][x+1][0] = playerTurn1
        dummy_explodeAdd(x+1, y, x, y, playerTurn1, alivePlayers)
        board[y][x-1][0] = playerTurn1
        dummy_explodeAdd(x-1, y, x, y, playerTurn1, alivePlayers)

def dummy_explodeMiddle(x, y, playerTurn1, alivePlayers):
    board[y][x] = [0, 0]
    board[y-1][x][0] = playerTurn1
    dummy_explodeAdd(x, y-1, x, y, playerTurn1, alivePlayers)
    board[y][x+1][0] = playerTurn1
    dummy_explodeAdd(x+1, y, x, y, playerTurn1, alivePlayers)
    board[y][x-1][0] = playerTurn1
    dummy_explodeAdd(x-1, y, x, y, playerTurn1, alivePlayers)
    board[y+1][x][0] = playerTurn1
    dummy_explodeAdd(x, y+1, x, y, playerTurn1, alivePlayers)

def dummy_explodeAdd(x, y, oldx, oldy, player, alivePlayers):
    
 
    if board[y][x][1] == 0:
        board[y][x] = [player, 1]
    else:
        if isCorner(x, y):
            dummy_explodeCorner(x, y, player, alivePlayers)
        elif isEdge(x, y):
            if board[y][x][1] < 2:
                board[y][x][1] += 1
            else:
                dummy_explodeEdge(x, y, player, alivePlayers)
        else:
            if board[y][x][1] < 3:
                board[y][x][1] += 1
            else:
                dummy_explodeMiddle(x, y, player, alivePlayers)
    board[y][x] = [0, 0]

# Function to check if the game is won
def check_won(board):
    player_counts = {1: 0, 2: 0}
    for y in range(row):
        for x in range(col):
            if board[y][x][0] in player_counts:
                player_counts[board[y][x][0]] += 1
    if player_counts[1] == 0:
        return 2
    elif player_counts[2] == 0:
        return 1
    else:
        return 9999

def evaluate_board(board, player):
    score = 0
    for y in range(row):
        for x in range(col):
            if board[y][x][0] == player:
                # Basic score based on atom count
                score += board[y][x][1]
                # Additional scores for controlling corners and edges
                if isCorner(x, y):
                    score += 3
                elif isEdge(x, y):
                    score += 2
            elif board[y][x][0] != 0:
                score -= board[y][x][1]
                if isCorner(x, y):
                    score -= 3
                elif isEdge(x, y):
                    score -= 2
    return score

def minimax( depth, alpha, beta, maximizing_player, player):
  
    global alivePlayers,board
    opponent = 1 
    if depth == 0 or check_won(board) != 9999:
        return evaluate_board(board, player if maximizing_player else opponent), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for y in range(row):
            for x in range(col):
                if board[y][x][0] == player or board[y][x][0] == 0:
                    board_copy = copy.deepcopy(board)
                    dummy_add(x, y, player)
                    
                    eval, _ = minimax(depth - 1, alpha, beta, False, player)
                   
                    board = copy.deepcopy(board_copy)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (x, y)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for y in range(row):
            for x in range(col):
                if board[y][x][0] == opponent or board[y][x][0] == 0:
                    board_copy = copy.deepcopy(board)
                    alivePlayers_copy = copy.deepcopy(alivePlayers)
                    dummy_add(x, y, opponent)
                    eval, _ = minimax(depth - 1, alpha, beta, True, player)
                    
                    board = copy.deepcopy(board_copy)
                    alivePlayers = copy.deepcopy(alivePlayers_copy)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (x, y)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, best_move

def best_move(player):
    global board
    best_val = -float('inf')
    best_move = None
    candidate_moves = genetic_algorithm(board, player, 50, 10, 5, 0.2)
    for move in candidate_moves:
        x, y = move
        if board[y][x][0] == player or board[y][x][0] == 0:
            board_copy = copy.deepcopy(board)
                
            dummy_add(x, y, player)
            move_val, _ = minimax( 2, float('-inf'), float('inf'), False, player)
            board = copy.deepcopy(board_copy)
            if move_val > best_val:
                best_val = move_val
                best_move = (x, y)

    print(f"Best move so far: {best_move} with value: {best_val}")               
    return best_move


def add(x, y, playerTurn1):
    if board[y][x][1] == 0:
        board[y][x] = [playerTurn1, 1]
            
    elif board[y][x][0] == playerTurn1:
        if isCorner(x, y):
            explodeCorner(x, y, playerTurn1)
        elif isEdge(x, y):
            if board[y][x][1] < 2:
                board[y][x][1] += 1
            else:
                explodeEdge(x, y, playerTurn1)
        else:
            if board[y][x][1] < 3:
                board[y][x][1] += 1
            else:
                explodeMiddle(x, y, playerTurn1)

def explodeCorner(x, y, playerTurn1):
    temp = alivePlayers[:]
    for player in temp:
        if not boardCheck(board, player) and count>players:
            alivePlayers.remove(player)
            winnerSub=screen.copy().subsurface(gameRect)
            

    # Check if game should end
    if len(alivePlayers) == 1:
        global mode
        screen.set_clip()
        mode = 'winner'
        drawPieces(board)
        drawBoard(colours[playerTurn1-1])
        return

    board[y][x] = [0, 0]
    if [x, y] == [0, 0]:
        board[y+1][x][0] = playerTurn1
        explodeAdd(x, y+1, x, y, playerTurn1)
        board[y][x+1][0] = playerTurn1
        explodeAdd(x+1, y, x, y, playerTurn1)
        
    elif [x, y] == [col-1, 0]:
        board[y+1][x][0] = playerTurn1
        explodeAdd(x, y+1, x, y, playerTurn1)
        board[y][x-1][0] = playerTurn1
        explodeAdd(x-1, y, x, y, playerTurn1)

    elif [x, y] == [0, row-1]:
        board[y-1][x][0] = playerTurn1
        explodeAdd(x, y-1, x, y, playerTurn1)
        board[y][x+1][0] = playerTurn1
        explodeAdd(x+1, y, x, y, playerTurn1)

    elif [x, y] == [col-1, row-1]:
        board[y-1][x][0] = playerTurn1
        explodeAdd(x, y-1, x, y, playerTurn1)
        board[y][x-1][0] = playerTurn1
        explodeAdd(x-1, y, x, y, playerTurn1)
   

def explodeEdge(x, y, playerTurn1):
    temp = alivePlayers[:]
    for player in temp:
        if not boardCheck(board, player) and count>players:
            alivePlayers.remove(player)
            winnerSub=screen.copy().subsurface(gameRect)
            
            

    # Check if game should end
    if len(alivePlayers) == 1:
        global mode
        screen.set_clip()
        mode = 'winner'
        drawPieces(board)
        drawBoard(colours[playerTurn1-1])
        return

    board[y][x] = [0, 0]
    if x == 0:
        board[y+1][x][0] = playerTurn1
        explodeAdd(x, y+1, x, y, playerTurn1)
        board[y][x+1][0] = playerTurn1
        explodeAdd(x+1, y, x, y, playerTurn1)
        board[y - 1][x][0] = playerTurn1
        explodeAdd(x, y - 1, x, y, playerTurn1)
    elif x == col-1:
        board[y+1][x][0] = playerTurn1
        explodeAdd(x, y+1, x, y, playerTurn1)
        board[y][x-1][0] = playerTurn1
        explodeAdd(x-1, y, x, y, playerTurn1)
        board[y - 1][x][0] = playerTurn1
        explodeAdd(x, y - 1, x, y, playerTurn1)
    elif y == 0:
        board[y+1][x][0] = playerTurn1
        explodeAdd(x, y+1, x, y, playerTurn1)
        board[y][x+1][0] = playerTurn1
        explodeAdd(x+1, y, x, y, playerTurn1)
        board[y][x - 1][0] = playerTurn1
        explodeAdd(x - 1, y, x, y, playerTurn1)
    elif y == row-1:
        board[y-1][x][0] = playerTurn1
        explodeAdd(x, y-1, x, y, playerTurn1)
        board[y][x+1][0] = playerTurn1
        explodeAdd(x+1, y, x, y, playerTurn1)
        board[y][x - 1][0] = playerTurn1
        explodeAdd(x - 1, y, x, y, playerTurn1)
   

def explodeMiddle(x, y, playerTurn1):
    temp = alivePlayers[:]
    for player in temp:
        if not boardCheck(board, player) and count>players:
            alivePlayers.remove(player)
            winnerSub=screen.copy().subsurface(gameRect)
            

    # Check if game should end
    if len(alivePlayers) == 1:
        global mode
        screen.set_clip()
        mode = 'winner'
        drawPieces(board)
        drawBoard(colours[playerTurn1-1])
        return


    board[y][x] = [0, 0]
    board[y-1][x][0] = playerTurn1
    explodeAdd(x, y-1, x, y, playerTurn1)
    board[y][x+1][0] = playerTurn1
    explodeAdd(x+1, y, x, y, playerTurn1)
    board[y][x - 1][0] = playerTurn1
    explodeAdd(x - 1, y, x, y, playerTurn1)
    board[y+1][x][0] = playerTurn1
    explodeAdd(x, y+1, x, y, playerTurn1)

    
def explodeAdd(x, y, oldx, oldy, player):
    if board[y][x][1] == 0:
        board[y][x] = [player, 1]
        explodeAnimation(oldx, oldy, x, y, player)

    else:
        if isCorner(x, y):
            explodeCorner(x, y, player)
        elif isEdge(x, y):
            if board[y][x][1] < 2:
                explodeAnimation(oldx, oldy, x, y, player)
                board[y][x][1] += 1
            else:
                explodeEdge(x, y, player)
        else:
            if board[y][x][1] < 3:
                explodeAnimation(oldx, oldy, x, y, player)
                board[y][x][1] += 1
            else:
                explodeMiddle(x, y, player)

def explodeAnimation(oldx, oldy, x, y, playerTurn1):
    preExplosion = screen.copy()
    for i in range(75):
        screen.blit(preExplosion, (0, 0))
        px=((mx-110)//75)*75+110
        py=((my-150)//75)*75+150
        draw.rect(screen,BLACK,(px,py,68,68))
        screen.blit(pieceImages[playerTurn1][0], (113 + oldx*75 + (x-oldx)*i, 153 + oldy*75 + (y-oldy)*i))
        display.flip()
        

def validClick(gameRect, leftClick, mx, my):
    return gameRect.collidepoint(mx,my) and leftClick

def boardCheck(board, playerTurn1):
    for y in range(row):
        for x in range(col):
            placeType = board[y][x][0]
            if placeType == playerTurn1:
                return True
    return False

def validMove(board, px, py, playerTurn1):
    return board[py][px][0]==0 or board[py][px][0]==playerTurn1       


# Function to get a list of valid moves for the AI
def get_valid_moves(board, player):
    valid_moves = []
    for y in range(row):
        for x in range(col):
            if board[y][x][0] == player or board[y][x][1] == 0:
                valid_moves.append((x, y))
    return valid_moves


while running:
    leftClick=False
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==MOUSEBUTTONDOWN:
            leftClick=True
        if evt.type==KEYDOWN:
            if evt.key==K_ESCAPE:
                playerTurn1=1
                count=0
                alivePlayers=[]
                board=[[[0,0] for i in range(col)]for l in range(row)]
                mode='title'
                
    mb=mouse.get_pressed()
    mx,my=mouse.get_pos()  

    if mode=='title':
        screen.blit(titlePic,(0,0))
        screen.blit(bigInfectedPic,(125,100))
        screen.blit(playPic,(350,400))
        if playRect.collidepoint(mx,my):
            draw.rect(screen,WHITE,playRect,5)
        if evt.type==KEYDOWN:
            if evt.key==K_RETURN:
                mode='instructions'
                time.wait(100)
        if playRect.collidepoint(mx,my) and leftClick:
            mode='instructions'
            time.wait(100)
    
    elif mode=='instructions':
        screen.fill(BLACK)
        screen.blit(titlePic,(0,-10))
        screen.blit(numOfPlayers,(195,220))
        screen.blit(player2,(320,290))
        screen.blit(player3,(420,290))
        screen.blit(player4,(520,290))
   
        
        if player2Rect.collidepoint(mx,my):
            draw.rect(screen,WHITE,player2Rect,5)
        elif player3Rect.collidepoint(mx,my):
            draw.rect(screen,WHITE,player3Rect,5)
        elif player4Rect.collidepoint(mx,my):
            draw.rect(screen,WHITE,player4Rect,5)
            
        if validClick(player2Rect, leftClick, mx, my):
            players=2
            alivePlayers=[1,2]
            mode='game'
            game=True
            time.wait(100)
        if validClick(player3Rect, leftClick, mx, my):
            players=3
            alivePlayers=[1,2,3]
            mode='game'
            game=True
            time.wait(100)
        if validClick(player4Rect, leftClick, mx, my):
            players=4
            alivePlayers=[1,2,3,4]
            mode='game'
            game=True
            time.wait(100)



    elif mode=='game':
        if game==True:
            screen.fill(BLACK)
            screen.blit(infectedPic,(290,45))
            game=False

        px=((mx-105)//75)
        py=((my-145)//75)
        
        if not boardCheck(board, playerTurn1) and count>players:
            playerTurn1 = playerTurn1 % players + 1
        
        # AI move for player 2
        if playerTurn1 == 2:
            time.wait(10)
            ai_move_res = best_move(2)
            if ai_move_res:
                x, y = ai_move_res
                add(x, y, 2)    
            if playerTurn1==players:
                playerTurn1=1
            else:
                playerTurn1+=1
            count+=1

        elif validClick(gameRect, leftClick, mx, my) and validMove(board, px, py, playerTurn1):
            add(px,py,playerTurn1)
                        
            if playerTurn1==players:
                playerTurn1=1
            else:
                playerTurn1+=1
            count+=1
        
        temp=alivePlayers
        for player in temp:
            if not boardCheck(board, player) and count>players:
                alivePlayers.remove(player)
                drawPieces(board)
                winnerSub=screen.copy().subsurface(gameRect)
            if len(alivePlayers)==1:
                screen.set_clip()

                mode='winner'


        drawPieces(board)
        drawBoard(colours[playerTurn1-1])


 
    elif mode == 'winner':
        screen.blit(titlePic,(0,0))
        screen.blit(infectedPic,(290,45))
        screen.blit(winnerSub,(105,145))
        drawBoard((255,255,255))
        drawPieces(board)
        
        draw.rect(screen,WHITE,(212,263,480,200))
        if alivePlayers==[1]:
            screen.blit(redWin,(295,330))
        if alivePlayers==[2]:
            screen.blit(greenWin,(248,330))
        if alivePlayers==[3]:
            screen.blit(blueWin,(270,330))
        if alivePlayers==[4]:
            screen.blit(yellowWin,(225,330))
        screen.blit(returnPic,(310,410))

    display.flip()      
quit()