#!/usr/bin/env python2

"""The game of tetris"""
from header import * 

os_supports_music=False


    
class Cell(object):
    """The representation of the smallest part of the tetris, can even be called a box or a brick"""
    def __init__(self, pos=(0,0), color=0):
        self.__pos=pos
        if color==0:
            self.__renderPic=Image.Green
        elif color==1:
            self.__renderPic=Image.Blue
        else:
            self.__renderPic=Image.Red
        self.__color=color
        
    def __str__(self):
        r="Cell object, positioned at (%s,%s)"%(self.__pos)
        return r
    
    def getPos(self):
        return self.__pos

    def getRenderPic(self):
        return self.__renderPic
    
    def setPos(self,pos):
        self.__pos=(pos[0],pos[1])


class Score(object):
    
    def incr(self,lines=0):
        if(lines == 1):
            self.__score+=10
        elif(lines==2):
            self.__score+=30
        elif (lines==3):
            self.__score+=45
        elif (lines==4):
            self.__score+=90

        self.__blitImage=self.__font.render(str(self.__score),True,Color('green'),Color('blue'))
        self.__blitImage=pygame.transform.scale(self.__blitImage,(self.__size,self.__size))

    def __init__(self):
        #create a render pic of the score
        #get a random rectangle
        self.__font=pygame.font.SysFont("Verdana",25,False,False)

        self.__score=0
        self.__blitImage=0

        x=30
        y=30
        self.__size=100
        self.__rect=pygame.Rect(x,y,self.__size,self.__size)

        self.incr(0)
    def reset(self):
        self.__score=0

    def getRenderImage(self):
        return self.__blitImage

    def getRect(self):
        return self.__rect
    
    
class Music(object):
    __sources={"lineComplete":"lineComplete.wav","gameOver":"gameOver.wav"}
    __musicFiles={"music":"music.mid","sound":{}}
    
    def __init__(self):
        if(os_supports_music): 
            Music.__enabled=True
        else:
            Music.__enabled=False

        if Music.__enabled: pygame.mixer.music.load(Music.__musicFiles['music'])

        for kw in Music.__sources:
            source= Music.__sources[kw]
            
            if Music.__enabled:
                Music.__musicFiles['sound'][kw]=pygame.mixer.Sound(source)
            
    def ready(self):
        return True

    def play(self):
        if Music.__enabled: pygame.mixer.music.play()

    def playSound(self,sType='lineComplete'):
        if not Music.__enabled: return;
        try:
            Music.__musicFiles['sound'][sType].play()
        except:
            print ("error")
class Image(object):
    __imageFiles={"red":"red.jpg",
                  "blue":"blue.jpg",
                  "green":"green.jpg",
                  "empty":"empty.jpg"
                  }
    Red=0
    Blue=0
    Green=0
    def __init__(self):
        Image.Red=pygame.image.load(Image.__imageFiles['red'])
        Image.Blue=pygame.image.load(Image.__imageFiles['blue'])
        Image.Green=pygame.image.load(Image.__imageFiles['green'])
        Image.Empty=pygame.image.load(Image.__imageFiles['empty'])
        
    def resizeCells(self,size):
        Image.Red=pygame.transform.scale(Image.Red,(size,size))
        Image.Blue=pygame.transform.scale(Image.Blue,(size,size))
        Image.Green=pygame.transform.scale(Image.Green,(size,size))
        Image.Empty=pygame.transform.scale(Image.Empty,(size,size))
        

class FallingObject(object):
    alreadyPresent=False
    __Objects=[
                [[(0,0),(0,1),(1,0),(1,1)]],
                
                [[(0,0),(0,1),(1,1),(1,2)],
                 [(0,1),(1,0),(1,1),(2,0)]],

                [[(0,0),(1,0),(1,1),(2,1)],
                 [(0,1),(0,2),(1,0),(1,1)]],

                [[(0,0),(1,0),(2,0),(3,0)],
                 [(0,0),(0,1),(0,2),(0,3)]],

                [[(0,0),(1,0),(2,0),(2,1)],
                 [(0,0),(0,1),(0,2),(1,0)],
                 [(0,0),(0,1),(1,1),(2,1)],
                 [(0,2),(1,0),(1,1),(1,2)]],

                [[(0,1),(1,1),(2,0),(2,1)],
                 [(0,0),(1,0),(1,1),(1,2)],
                 [(0,0),(0,1),(1,0),(2,0)],
                 [(0,0),(0,1),(0,2),(1,2)]],

                [[(0,1),(1,0),(1,1),(1,2)],
                 [(0,0),(1,0),(1,1),(2,0)],
                 [(0,0),(0,1),(0,2),(1,1)],
                 [(0,1),(1,0),(1,1),(2,1)]]
            ]
    
    def CreateNew(self,init=-1):

        #get the centre position of the width of the main board
        #get a random cell from objects[]
        #add the centre position to all of the cells
        #create object from the new list
        ctr=int(self.__onBoard.width/2)-1

        self.__itemX=self.__nextItemX
        
        self.__nextItemX=random.randint(0,len(FallingObject.__Objects)-1)
        temp=FallingObject.__Objects[self.__nextItemX]
        
        self.__itemY=self.__nextItemY

        self.__nextItemY=random.randint(0,len(temp)-1)
        newObj=copy.deepcopy(temp[self.__nextItemY])
        
        del temp
        
        for i in range(0, len(newObj)):
            newObj[i]=(newObj[i][0],newObj[i][1]+ctr)

        color=random.randint(0,2)
        
        newFallObj=[]
        for i in list(newObj):
            z=Cell(i,color)
            newFallObj.append(z)
            
        if(init>0):
            self.nextFallObject=newFallObj
        else:
            self.fallObject=self.nextFallObject
            self.nextFallObject=newFallObj
        
    def __init__(self,board,stack, structure=1):
        self.__onBoard=board
        self.__onStack=stack

        self.__itemX=0
        self.__itemY=0
        self.__nextItemX=0
        self.__nextItemY=0
        
        if(FallingObject.alreadyPresent):
            print("Sorry, I am already present")
        else:
            FallingObject.alreadyPresent=True
            self.fallObject=[]
            self.nextFallObject=[]
            self.CreateNew()

        
    def init(self):
        self.CreateNew()
        
    def moveToBottom(self):
        z=self.moveDown()
        while z>0:
            z=self.moveDown()
        
    def rotate(self):        
        xIncr,yIncr=[0,0]
        pos=copy.deepcopy(self.fallObject[0].getPos())
        theory=FallingObject.__Objects[self.__itemX][self.__itemY][0]

        xIncr=pos[0]-theory[0]
        yIncr=pos[1]-theory[1]

        newItemY=self.__itemY+1
        if(newItemY >= len(FallingObject.__Objects[self.__itemX])):
            newItemY=0
        
        newType=copy.deepcopy(FallingObject.__Objects[self.__itemX][newItemY])
        
        newCells=[]
        for i in range(len(newType)):
            newCells.append((newType[i][0]+xIncr,newType[i][1]+yIncr))

        for i in list(newCells):
            if i[0]<0 or i[0]>self.__onBoard.height-1:
                return False
            if i[1]<0 or i[1]>self.__onBoard.width-1:
                return False

        if(doOverlap(self.__onStack,newCells)):
            return False
        
        for i in range(len(self.fallObject)):
            self.fallObject[i].setPos((newCells[i]))

        self.__itemY=newItemY
        
        return True
    
    def moveDown(self):
        newPos=[]
        a=1
        for i in range(0, len(self.fallObject)):
            z=self.fallObject[i].getPos()
            newPos.append((z[0]+1,z[1]))
            if (newPos[i][0]>=self.__onBoard.height or newPos[i][1]>=self.__onBoard.width):
                self.__onStack.addToStack(self.fallObject)
                self.CreateNew()
                return -1

        if doOverlap(self.__onStack,newPos):
            self.__onStack.addToStack(self.fallObject)
            self.CreateNew()
            return -2
        
        for i in range(0,len(self.fallObject)):
            self.fallObject[i].setPos(newPos[i])

        return 1
    
    def moveTowards(self, direct=-1):
        #create a new position of the current cell
        #if out of bound, return False
        #if merges with mainStack, return false
        #set the new position as the position of the block

        newPos=[]
        for i in range(len(self.fallObject)):
            pos=self.fallObject[i].getPos()
            newPos.append((pos[0],pos[1]+direct))

        for i in list(newPos):
            if i[1]<0 or i[1]>=self.__onBoard.width:
                return False
        if (doOverlap(self.__onStack,newPos)):
            return False

        for z in range(len(self.fallObject)):
            self.fallObject[z].setPos(newPos[z])
            
        return True
    

    def getCells(self):
        return FallingObject.fallObject
    
class MainStack(object):
    __Cells=[]
    def __init__(self,onBoard):
        self.__board=onBoard
		
    def addToStack(self,block):
        #add the points from the block to the cells
        for i in list(block):
            MainStack.__Cells.append(i)
            z=i.getPos()
            if z[0] <= 0:
                self.__board.GameOverInterface()
            
        rows=[]
        for i in range(self.__board.height):
            rows.append(0)

        for i in list(MainStack.__Cells):
            z=i.getPos()
            rows[z[0]] += 1


        totalLineRemoved=0

        i=self.__board.height-1
        while i>=0:
            if rows[i]==self.__board.width:
                totalLineRemoved += 1
                #i th row is filled
                #for each cell, get its xPos
                #if xPos=i, remove from mainstack,
                #if xPos>i, leave it
                #if xPos<i, reduce 1 from it
                #for rows[]. remove the current index,
                #add 0 at the front of rows[]
                #increment the totalLineRemoved

                for x in list(MainStack.__Cells):
                    z=x.getPos()
                    if z[0]==i:
                        MainStack.__Cells.remove(x)

                for x in list(MainStack.__Cells):
                    z=x.getPos()
                    if z[0]<i:
                        x.setPos((z[0]+1,z[1]))
                rows.reverse()
                rows.remove(self.__board.width)
                rows.append(0)
                rows.reverse()
                
            else:
                i-=1
                
        if totalLineRemoved >0:
            self.__board.score.incr(totalLineRemoved)
            Tetris.music.playSound('lineComplete')
        
    def getCells(self):
        return MainStack.__Cells
    
class Tetris(object):
    """The game of tetris"""

    __preConfigured=False
    __loadedMusic=False
    music=0
    
    def __init__(self, height=20, width=10, gameSize=600):

        self.height=height
        self.width=width
        self.__gameSize=gameSize

        self.__gameOver=False
        self.__fps=30
        self.__movesPerSecond=2
        
        self.score=0
        
        self.__pieceStack=[]            #the stack of all the items
        self.__fallingPiece=0           #the list to keep a falling piece
        
        self.mainStack=0
        self.block=0            #the falling block representation
        
        self.__gameScreen=0
        self.__clock=pygame.time.Clock()
        self.__upMargin=10
        self.__cellMargin=1
        self.__leftMargin=0     #will be initialised later
        self.__cellSize=0
        
    def GameOverInterface(self):
        Tetris.music.playSound('gameOver')
        print("Game Over")
        time.sleep(3)
        self.__exitGame()
    def __preConfigure(self):
        if(not Tetris.__preConfigured):
            Tetris.preConfigured=True
            pygame.init()
            pygame.key.set_repeat(400,60)
            pygame.display.set_caption("Tetris")
            pygame.font.init()
        return 1

    def __config(self):
        self.score=Score()
        self.score.reset()
        
        #generate the cell size
        gameHeight=self.__gameSize-2*self.__upMargin
        gameHeight -= (self.height-1) *( self.__cellMargin)

        self.cellSize=int(gameHeight/self.height)

        #create the left margin
        self.__leftMargin=int((self.__gameSize - (self.__cellMargin * (self.width-1)) - (self.width * self.cellSize))/2)


        #create a music instance
        Tetris.music=Music()

        #create a picture instance
        Tetris.image=Image()

        return 1

    def __loadVideo(self):
        self.__gameScreen=pygame.display.set_mode((self.__gameSize,self.__gameSize))
        return 1

    def __initMainStackAndBlock(self):
        self.mainStack=MainStack(self)

        self.block=FallingObject(self,self.mainStack)
        self.block.init()

        return 1
    
    def gameReady(self):
        #initialise everything
        print("pre configuring")
        if(Tetris().__preConfigure()<0):
            return -1

        #rest stuffs, such as create a falling object, an empty stack, etc
        print("Initialising game components")
        if(self.__config()<0):
            return -2
        
        #initialise music and sound
        print("loading music and sounds")
        if(not Tetris.__loadedMusic):
            Tetris.__loadedMusic=True
            Tetris.music.ready()
        
        #initialise graphics
        print("loading graphics")
        Tetris.image.resizeCells(self.cellSize)
                                      
        #initialise video
        print("loading video")
        if(self.__loadVideo()<0):
            return -3
        #initialise the main stack and block
        print("Initialising main stack and block")
        if(self.__initMainStackAndBlock()<0):
            return -4
        return 1

    def __getMove(self):
        for i in pygame.event.get():
            if i.type==QUIT:
                self.__exitGame()
            if i.type==KEYDOWN:
                if i.key==K_ESCAPE:
                    self.__exitGame()
                elif i.key==K_UP:
                    self.block.rotate()
                elif i.key==K_DOWN:
                    self.block.moveDown()
                elif i.key==K_SPACE:
                    self.block.moveToBottom()
                elif i.key==K_LEFT or i.key==K_RIGHT:
                    if i.key==K_LEFT:
                        direct=-1
                    else:
                        direct=1
                    self.block.moveTowards(direct)
                    return None
                
    def __exitGame(self):
        pygame.quit()
        print("Good bye")
        sys.exit()

    def __render(self):
        self.__gameScreen.fill(Color('white'))

        #get the position of the (0,0) cell
        xPos=self.__leftMargin
        yPos=self.__upMargin

        cellsToDrawFromFall=self.block.fallObject
        cellsToDrawFromStack=self.mainStack.getCells()
        cellsToDrawForNext=self.block.nextFallObject

        #blit the next appearing object
        for i in list(cellsToDrawForNext):
            z=i.getPos()
            top=z[0]*self.cellSize + 200
            left=z[1]*self.cellSize + 350
            rect=pygame.Rect(left,top,self.cellSize,self.cellSize)
            self.__gameScreen.blit(i.getRenderPic(),rect)
    
        printArray=[]
        for i in range(0, self.height):
            printArray.append([])
            for j in range(0,self.width):
                printArray[i].append(Image.Empty)

        for x in list(cellsToDrawFromFall):
            pos=x.getPos()
            pic=x.getRenderPic()
            printArray[pos[0]][pos[1]]=pic

        for x in list(cellsToDrawFromStack):
            pos=x.getPos()
            pic=x.getRenderPic()
            printArray[pos[0]][pos[1]]=pic
            
        for i in range(0, self.height):
            top=self.__upMargin + i* self.__cellMargin + (i)* self.cellSize
            for j in range(0, self.width):
                left=self.__leftMargin + j* self.__cellMargin + (j)*self.cellSize
                rect=pygame.Rect(left,top,self.cellSize,self.cellSize)
                self.__gameScreen.blit(printArray[i][j],rect)
        
        self.__gameScreen.blit(self.score.getRenderImage(),self.score.getRect())
        
        pygame.display.update()
        return True
    
    def startGame(self):
        z=self.gameReady()
        Tetris.music.play()
        if(z<0):
            print("Could not load the game. %s error"%(-z))
        else:
            move=0
            while True:
                move+=1
                self.__getMove()
                self.__render()

                if(move>=int(self.__fps/self.__movesPerSecond)):
                    move=0
                    self.block.moveDown()
                self.__clock.tick(self.__fps)


def doOverlap(stack,blockCells):
    c1=stack.getCells()
    for x in list(c1):
        pos1=x.getPos()
        for y in list(blockCells):
            if(pos1[0]==y[0] and pos1[1]==y[1]):
                return True
    return False

def PrintCellArray(array):
    for i in list(array):
        print(i)
        
Game=Tetris()
Game.startGame()
