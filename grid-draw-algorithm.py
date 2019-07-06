import random, pygame, sys
from pygame.locals import *
from Grafos.Grafo import *
from pprint import pprint

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 1250 # size of window's width in pixels
WINDOWHEIGHT = 830 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 30 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 30 # number of columns of icons
BOARDHEIGHT = 20 # number of rows of icons
#assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100) 
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (0, 0, 0)
BGCOLOR = (0, 154, 205)
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

def main():
    g = Grafo("Mi Grafo")
    g.inicializarGrafo()
    type = sys.stdin.readline().split()
    nodes = sys.stdin.readline().split()

    graph = []
    for a in range(BOARDHEIGHT*BOARDWIDTH):
        trans = sys.stdin.readline().split()
        graph.append(trans)

    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Mi juego')

    mainBoard = getRandomizedBoard()
    revealedBoxes =generateBoard(type)
    
    firstSelection = None # stores the (x, y) of the first box clicked.
    secondSelection = None
    
    DISPLAYSURF.fill(BGCOLOR)

    while True: # main game loop
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)
        
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                #print str(mousex)+","+str(mousey)
            elif event.type == MOUSEBUTTONUP:
                #print "CLick"
                mousex, mousey = event.pos
                mouseClicked = True
            
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            drawHighlightBox(boxx, boxy)
            if revealedBoxes[boxy][boxx]:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_s: #tecla S, pone el inicio
                        if firstSelection == None: 
                            revealedBoxes[boxy][boxx] = "inicio" 
                            firstSelection = (boxy, boxx)
                            print "inicio: " + (str(firstSelection[0]+1)+"_"+str(firstSelection[1]+1))
                    elif event.key == K_e: #telca E pone el fin
                        if secondSelection == None and firstSelection != None:
                            revealedBoxes[boxy][boxx] = "fin"
                            secondSelection = (boxy, boxx)
                            print "fin: " + (str(secondSelection[0]+1)+"_"+str(secondSelection[1]+1))
                    elif firstSelection != None and secondSelection != None and event.key == K_b:
                        print "Calculando BSF....."
                        g.bfs(str(firstSelection[0]+1)+"_"+str(firstSelection[1]+1))
                        drawWayBoard(revealedBoxes,firstSelection,secondSelection,g,None)
                    elif firstSelection != None and secondSelection != None and event.key == K_d:
                        print "Calculando DSF....."
                        g.dfs(str(firstSelection[0]+1)+"_"+str(firstSelection[1]+1))
                        drawWayBoard(revealedBoxes,firstSelection,secondSelection,g,None)
                    elif firstSelection != None and secondSelection != None and event.key == K_j:
                        print "Calculando Dijkstra....."
                        graphe = generateGraph(graph,nodes,1)
                        p=dijkstra(graphe,str(firstSelection[0]+1)+"_"+str(firstSelection[1]+1), str(secondSelection[0]+1)+"_"+str(secondSelection[1]+1))
                        drawWayBoard(revealedBoxes,firstSelection,secondSelection,g,p)
                    elif firstSelection != None and secondSelection != None and event.key == K_a:
                        print "Calculando A Estrella....."
                        graphe = generateGraph(graph,nodes,0)
                        p=dijkstra(graphe,str(firstSelection[0]+1)+"_"+str(firstSelection[1]+1), str(secondSelection[0]+1)+"_"+str(secondSelection[1]+1))
                        drawWayBoard(revealedBoxes,firstSelection,secondSelection,g,p)
                        #route = heuristicManhattan(str(firstSelection[0]+1)+"_"+str(firstSelection[1]+1), str(secondSelection[0]+1)+"_"+str(secondSelection[1]+1),revealedBoxes)
                        #drawWayBoard(revealedBoxes,firstSelection,secondSelection,g,route)
                    elif event.key == K_z:
                        print "Limpiando"
                        mainBoard = getRandomizedBoard()
                        firstSelection = None 
                        secondSelection = None
                        revealedBoxes = generateBoard(type)
                        drawBoard(mainBoard, revealedBoxes)
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def heuristicManhattan(s,e,board):
    route1 = deque()
    route2 = deque()
    start =  s.split('_')
    end = e.split('_')
    costRoute1 = 0
    costRoute2 = 0
    if int(start[0]) < int(end[0]) and int(start[1]) < int(end[1]):
        for x in range(int(start[0]),int(end[0])+1):
            if board[int(x)-1][int(start[1])-1] == "wall" or board[int(x)-1][int(start[1])-1] == 0:
                costRoute1 += 20
            elif board[int(x)-1][int(start[1])-1] == 1:
                costRoute1 +=10
            #print board[int(x)-1][int(start[1])-1], int(x), start[1]
            route1.append(str(x)+"_"+start[1])
        for y in range(int(start[1])+1,int(end[1])+1):
            if board[int(end[0])-1][int(y)-1] == "wall" or board[int(end[0])-1][int(y)-1] == 0:
                costRoute1 += 20
            elif board[int(end[0])-1][int(y)-1] == 1:
                costRoute1 +=10
            route1.append(end[0]+"_"+str(y))
            #print board[int(end[0])-1][int(y)-1],int(end[0])-1,int(y)-1
            
        for i in range(int(start[1]),int(end[1])+1):
            if board[int(start[0])-1][int(i)-1] == "wall" or board[int(start[0])-1][int(i)-1] == 0:
                costRoute2 += 20
            elif board[int(start[0])-1][int(i)-1] == 1:
                costRoute2 +=10
            #print board[int(start[0])-1][int(i)-1], int(start[0])-1, int(i)-1
            route2.append(start[0]+"_"+str(i))
        for j in range(int(start[0])+1,int(end[0])+1):
            if board[int(j)-1][int(end[1])-1] == "wall" or board[int(j)-1][int(end[1])-1] == 0:
                costRoute2 += 20
            elif board[int(j)-1][int(end[1])-1] == 1:
                costRoute2 +=10
            #print board[int(j)-1][int(end[1])-1], int(end[1])-1, int(j)-1
            route2.append(str(j)+"_"+end[1])
    print costRoute1+10, costRoute2
    if costRoute1+10 <= costRoute2:
        return route1
    else:
        return route2

def generateBoard(type):
    masterType = []
    count = 0
    for y in range(BOARDHEIGHT):
        new = []
        for x in range(BOARDWIDTH):
            if type[count] == "1":
                new.append(1)
            elif type[count] == "0":
                new.append(0)
            count += 1
        masterType.append(new)
    return masterType

def drawWayBoard(revealedBoxes,firstSelection,secondSelection,g,routeManhattan):
    route = routeManhattan
    if routeManhattan == None:
        route = deque()
        g.crearRuta(str(secondSelection[0]+1)+"_"+str(secondSelection[1]+1), route)
    cost = 0
    for e in route:
        boxWay= list(e)
        if len(boxWay) == 3:
            if revealedBoxes[int(boxWay[0])-1][int(boxWay[2])-1] == 0 or revealedBoxes[int(boxWay[0])-1][int(boxWay[2])-1] == "wall":
                revealedBoxes[int(boxWay[0])-1][int(boxWay[2])-1] = "wall"
                cost +=20
            else:
                revealedBoxes[int(boxWay[0])-1][int(boxWay[2])-1] = "draw"
                cost +=10
        elif len(boxWay) == 4:
            if boxWay[1] == "_": 
                if revealedBoxes[int(boxWay[0])-1][int(boxWay[2]+boxWay[3])-1] == 0 or revealedBoxes[int(boxWay[0])-1][int(boxWay[2]+boxWay[3])-1] == "wall": 
                    revealedBoxes[int(boxWay[0])-1][int(boxWay[2]+boxWay[3])-1] = "wall"
                    cost +=20
                else: 
                    revealedBoxes[int(boxWay[0])-1][int(boxWay[2]+boxWay[3])-1] = "draw"
                    cost +=10
            else:
                if revealedBoxes[int(boxWay[0]+boxWay[1])-1][int(boxWay[3])-1] == 0 or revealedBoxes[int(boxWay[0]+boxWay[1])-1][int(boxWay[3])-1] == "wall":
                    revealedBoxes[int(boxWay[0]+boxWay[1])-1][int(boxWay[3])-1] = "wall"
                    cost +=20
                else:
                    revealedBoxes[int(boxWay[0]+boxWay[1])-1][int(boxWay[3])-1] = "draw"
                    cost +=10
        elif len(boxWay) == 5:
            if revealedBoxes[int(boxWay[0]+boxWay[1])-1][int(boxWay[3]+boxWay[4])-1] == 0 or revealedBoxes[int(boxWay[0]+boxWay[1])-1][int(boxWay[3]+boxWay[4])-1] == "wall":
                revealedBoxes[int(boxWay[0]+boxWay[1])-1][int(boxWay[3]+boxWay[4])-1] = "wall"
                cost +=20
            else:
                revealedBoxes[int(boxWay[0]+boxWay[1])-1][int(boxWay[3]+boxWay[4])-1] = "draw"
                cost +=10
    if cost-10 > 0:
        print "Costo Total: "+ str(cost-10)
    else:
        print "No hay transicion"
    revealedBoxes[firstSelection[0]][firstSelection[1]] ="inicio"
    revealedBoxes[secondSelection[0]][secondSelection[1]] ="fin"
        
def generateRevealedBoxesData(val):
    revealedBoxes = []
    
    for i in range(len(val)):
        n = []
        if val[i] == "1":
            n.append(True)
        elif val[i] == "0":
            n.append(False)
        revealedBoxes.append(n)
    print "revealed "+str(revealedBoxes)
    return revealedBoxes

#inicializar tablero
def getRandomizedBoard():
    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        board.append(column)
    return board

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDHEIGHT):
        for boxy in range(BOARDWIDTH):
            left, top = leftTopCoordsOfBox(boxy, boxx)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxy, boxx)
    return (None, None)

def drawBoard(board, revealed):
    for boxx in range(BOARDHEIGHT):
        for boxy in range(BOARDWIDTH):
            left, top = leftTopCoordsOfBox(boxy, boxx)
            if revealed[boxx][boxy] == 1:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left,top, BOXSIZE, BOXSIZE))
            elif revealed[boxx][boxy] == 0:
                pygame.draw.rect(DISPLAYSURF, BLACK, (left,top, BOXSIZE, BOXSIZE))
            elif revealed[boxx][boxy] == "inicio":
                pygame.draw.rect(DISPLAYSURF, GREEN, (left,top, BOXSIZE, BOXSIZE))
            elif revealed[boxx][boxy] == "fin":
                pygame.draw.rect(DISPLAYSURF, RED, (left,top, BOXSIZE, BOXSIZE))
            elif revealed[boxx][boxy] == "draw":
                pygame.draw.rect(DISPLAYSURF, YELLOW, (left,top, BOXSIZE, BOXSIZE))
            elif revealed[boxx][boxy] == "wall":
                pygame.draw.rect(DISPLAYSURF, GRAY, (left,top, BOXSIZE, BOXSIZE))

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def generateGraph(graph,node,mode):
    graphe = {}
    nodes = tuple(node)
    
    keys = []
    for a in range((BOARDHEIGHT*BOARDWIDTH)):
        new = []
        countX = 0
        countY = 0
        for b in range((BOARDHEIGHT*BOARDWIDTH)):
            countY += 1
            if countY > BOARDWIDTH:
                countY = 1
                countX +=1
            if graph[a][b] != '-1':
                if graph[b][a] == '10' or graph[b][a] == '20':
                    aux = []
                    if graph[b][a] == '10':
                        aux.append(str(countX+1)+"_"+str(countY))
                        aux.append(10)
                        aux1 = tuple(aux)
                        new.append(aux1)
                    if mode == 0:
                        if graph[b][a] == '20':
                            aux.append(str(countX+1)+"_"+str(countY))
                            aux.append(20)
                            aux1 = tuple(aux)
                            new.append(aux1)
        keys.append(nodes[a])
        tuples = dict.fromkeys(keys, new)
        graphe.update(tuples)
        keys = []
    return graphe

def dijkstra(G, a, z):
    Inf = 0
    for u in G:
        for v, w in G[u]:
            Inf += w
    L = dict([(u, Inf) for u in G])
    L[a] = 0
    S = set([u for u in G])
    A = { }

    def W(v):
        return L[v]

    while z in S:
        u = min(S, key=W)
        S.discard(u)
        for v, w in G[u]:
            if v in S:
                if L[u] + w < L[v]:
                    L[v] = L[u] + w
                    A[v] = u
    P = []
    u = z
    while u != a:
        P.append(u)
        try:
            u = A[u]
        except KeyError: 
            print "No hay transicion"
            break
    route = deque()
    if len(P) > 1:
        P.append(a)
        P.reverse()
        for e in P:
            route.append(e)
        return route
    else:
        return route.clear()

if __name__ == '__main__':
    main()
    
    
    