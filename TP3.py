#part of the sidescrolling code comes from the course website:
#https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#this code imports cmu112 graphics:
#https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *
from tkinter import *
import random

class GameMode(Mode):
    def appStarted(mode):
        url="https://tinyurl.com/t6aj4zx"
        mode.background1=mode.loadImage(url)
        mode.background=mode.scaleImage(mode.background1, 2.7)
        mode.message="Attempt 1"
        #The player starts from the very left
        #the top left corner of the square
        mode.topX=0
        mode.squareSize=40
        mode.topY=mode.height*2//3-mode.squareSize
        #Set the platform to 1/3 of the height
        mode.platform=mode.height*2//3
        mode.scrollX = 0
        mode.score=0
        mode.dy=20
        mode.atCenter=False
        mode.dots = [(random.randrange(mode.width),
                      random.randrange(60, mode.height)) for _ in range(50)]
        mode.selectionList=["Triangle", "Puddle", "Rectangle"]
        mode.obstacleList=[]
        mode.bonusList=[]
        mode.newBonusList=[]
        mode.obstacleCounter=0
        mode.isJumping=False
        mode.gameOver=False
        mode.goingUp = False

    def keyPressed(mode, event):
        if (event.key == "Up") or (event.key=="Space"): 
            mode.isJumping=True 
        elif (event.key=="r"):
            mode.appStarted() 

    def mousePressed(mode, event):
        mode.isJumping=True
        

    def mouseDragged(mode, event):
        mode.longJump
        pass

    def timerFired(mode):
        #check if game over due to collision with obstacles
        mode.checkTriangleCollision()
        mode.checkPuddleCollision()
        mode.checkRectangleCollision()
        if mode.gameOver==True:
            return
        else:
            #increment the score every milisecond
            mode.score+=1
            mode.message=f'score: {mode.score}'
            #if the dot hasn't scroll to a certain distance
            if not mode.atCenter:
                #change the x value of the topLeft
                mode.topX=mode.topX+10
                #the square stops scrolling here
                if mode.topX==100:
                    mode.atCenter=True
            if mode.atCenter==True:
                mode.scrollX+=20
            #short jump when key/mouse pressed
            if mode.isJumping==True:
                mode.shortJump()
            mode.obstacleCounter+=1
            #randomly select one of the three obstacles
            mode.shape=random.choice(mode.selectionList)
            #add the obstacles to the list every five seconds
            if mode.obstacleCounter%(5000/mode.timerDelay)==0:
                if mode.shape=="Triangle":
                    triangle=Triangle(mode.width+mode.scrollX, mode.platform)
                    mode.obstacleList.append(triangle)
                    if triangle.x+mode.squareSize<=0:
                        mode.obstacleList.remove(triangle)
                elif mode.shape=="Puddle":
                    puddle=Puddle(mode.width+mode.scrollX, mode.platform)
                    mode.obstacleList.append(puddle)
                    if puddle.topX+puddle.width<=0:
                        mode.obstacleList.remove(puddle)
                elif mode.shape=="Rectangle":
                    rectangle=Rectangle(mode.width+mode.scrollX, mode.platform)
                    mode.obstacleList.append(rectangle)
                    if rectangle.botX-mode.scrollX+rectangle.width<=0:
                        mode.obstacleList.remove(rectangle)
            #remove the obstacles after they finish scrolling to the left of canvas
            for obstacle in mode.obstacleList:
                if type(obstacle)==Triangle:
                    if obstacle.x-mode.scrollX+mode.squareSize<=0:
                        mode.obstacleList.remove(obstacle)
                elif type(obstacle)==Puddle:
                    if obstacle.topX-mode.scrollX+obstacle.width<=0:
                        mode.obstacleList.remove(obstacle)
                elif type(obstacle)==Rectangle:           
                    if obstacle.botX-mode.scrollX+obstacle.width<=0:
                        mode.obstacleList.remove(obstacle)
            #add the bonus stars every 3 seconds
            if mode.obstacleCounter%(3000/mode.timerDelay)==0:
                mode.bonusList.append(BonusStar(mode.width+mode.scrollX, \
                    mode.platform - 2*mode.squareSize))
            if mode.checkBonusCollision()==True:
                mode.score+=100 
            
    
    def shortJump(mode):
        #jump over when the obstacle is a triangle or a puddle
        if len(mode.obstacleList)>0:
            shape=mode.obstacleList[0]
            if type(shape)==Triangle or type(shape)==Puddle:
                mode.topY-=mode.dy
                #start going down after reaching a certain height
                if mode.topY <= mode.platform - 3*mode.squareSize:
                    mode.dy = -abs(mode.dy)
                #stop moving after reaching the bottom
                elif mode.topY>= mode.platform-mode.squareSize:
                    mode.topY=mode.height*2//3-40
                    mode.isJumping=False
                    mode.dy = abs(mode.dy)
            if type(shape)==Rectangle:
                mode.topY-=mode.dy
                #stop moving after reaching the bottom, jump on top of the rectangle
                if mode.topX+mode.squareSize>shape.botX-mode.scrollX and \
                    mode.topX<shape.botX+shape.width-mode.scrollX:
                    if mode.topY>= mode.platform-2*mode.squareSize:
                        mode.topY=mode.platform-2*mode.squareSize 
                        mode.dy = abs(mode.dy)
                        #mode.topY-=mode.dy
                    if mode.topY <= mode.platform - 4*mode.squareSize:
                        mode.dy = -abs(mode.dy)
                        
                        #mode.isJumping=False
                    elif mode.topY>= mode.platform-2*mode.squareSize:
                        mode.topY=mode.platform-2*mode.squareSize
                        mode.isJumping=False
                
                #start going down after reaching a certain height
                elif mode.topY <= mode.platform - 3*mode.squareSize:
                    mode.dy = -abs(mode.dy)
                
                        
                #reaches the end of the rectangle
                elif mode.topX>=shape.botX+shape.width-mode.scrollX:
                    mode.topY-=mode.dy
                    if mode.topY>= mode.height*2//3-40:
                        mode.topY=mode.height*2//3-40
                        mode.isJumping=False
                        mode.dy = abs(mode.dy)
                elif mode.topX+mode.squareSize<=shape.botX-mode.scrollX:
                    if mode.topY>=mode.platform-mode.squareSize:
                        mode.topY=mode.platform-mode.squareSize
                        mode.isJumping=False
                        mode.dy = abs(mode.dy)
        else:
            #only change the dy value since it's already sidescrolling
            mode.topY-=mode.dy
            #start going down after reaching a certain height
            if mode.topY <= mode.platform - 3*mode.squareSize:
                mode.dy = -abs(mode.dy)
            #stop moving after reaching the bottom
            elif mode.topY>= mode.platform-mode.squareSize:
                mode.topY=mode.platform-mode.squareSize
                mode.isJumping=False
                mode.dy = abs(mode.dy)

    
    def longJump(mode):
        pass
    
    #check whether two lines intersect
    @staticmethod
    def checkIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
        if x1==x2:
            m2=(y4-y3)/(x4-x3)
            b2=y3-m2*x3
            x=x1
            y=x*m2+b2
        elif x3==x4:
            m1=(y2-y1)/(x2-x1)
            b1=y1-m1*x1
            x=x3
            y=x*m1+b1
        else:
            m1=(y2-y1)/(x2-x1)
            m2=(y4-y3)/(x4-x3)
            b1=y1-m1*x1
            b2=y3-m2*x3
            x=(b2-b1)/(m1-m2)
            y=x*m1+b1
        if x<=max(x1, x2) and x>=min(x1, x2) \
            and x<=max(x3, x4) and x>=min(x3, x4):
            if y<=max(y1, y2) and y>=min(y1, y2) \
                and y<=max(y3, y4) and y>=min(y3, y4):
                return True   
                 
    #check if the sqaure collides with the triangle by checking side intersections
    def checkTriangleCollision(mode):
        topLeftX=mode.topX
        topLeftY=mode.topY
        topRightX=mode.topX+mode.squareSize
        topRightY=mode.topY
        botLeftX=mode.topX
        botLeftY=mode.topY+mode.squareSize
        botRightX=mode.topX+mode.squareSize
        botRightY=mode.topY+mode.squareSize
        for obstacle in mode.obstacleList:
            if isinstance(obstacle, Triangle):
                triTopX=obstacle.x-mode.scrollX+mode.squareSize*0.5
                triTopY=mode.platform - 0.5*mode.squareSize*(3**0.5)
                triLeftX=obstacle.x-mode.scrollX
                triLeftY=mode.platform
                triRightX=triLeftX+mode.squareSize
                triRightY=mode.platform
                #right of square and left of triangle
                if GameMode.checkIntersection(topRightX, topRightY,
                    botRightX, botRightY, triTopX, triTopY, triLeftX, triLeftY)==True:
                    mode.gameOver=True
                #right of square and right of triangle
                if GameMode.checkIntersection(topRightX, topRightY, 
                    botRightX, botRightY, triTopX, triTopY, triRightX, triRightY)==True:
                    mode.gameOver=True
                #left of square and left of triangle
                if GameMode.checkIntersection(topLeftX, topLeftY,
                    botLeftX, botLeftY, triTopX, triTopY, triLeftX, triLeftY)==True:
                    mode.gameOver=True
                #left of square and right of triangle
                if GameMode.checkIntersection(topLeftX, topLeftY, 
                    botLeftX, botLeftY, triTopX, triTopY, triRightX, triRightY)==True:
                    mode.gameOver=True
                #bottom of square and left of triangle
                if GameMode.checkIntersection(botLeftX, botLeftY,
                    botRightX, botRightY, triTopX, triTopY, triLeftX, triLeftY)==True:
                    mode.gameOver=True
                #bottom of square and right of triangle
                if GameMode.checkIntersection(botLeftX, botLeftY, 
                    botRightX, botRightY, triTopX, triTopY, triRightX, triRightY)==True:
                    mode.gameOver=True
    
    #check if the square collides with the puddle by checking if the square
    #gets in between the puddle edges   
    def checkPuddleCollision(mode):
        botLeftX=mode.topX
        botLeftY=mode.topY+mode.squareSize
        botRightX=mode.topX+mode.squareSize
        botRightY=mode.topY+mode.squareSize
        for obstacle in mode.obstacleList:
            if isinstance(obstacle, Puddle):
                pudLeftX=obstacle.topX-mode.scrollX
                pudRightX=pudLeftX+obstacle.width
                if botLeftY==mode.platform:
                    if (botLeftX<=pudRightX and botLeftX>=pudLeftX) or \
                        (botRightX<=pudRightX and botRightX>=pudLeftX):
                        mode.gameOver=True
    
    #check if the square run into the rectangle
    def checkRectangleCollision(mode):
        botRightX=mode.topX+mode.squareSize
        botRightY=mode.topY+mode.squareSize
        for obstacle in mode.obstacleList:
            if isinstance(obstacle, Rectangle):
                RecLeftX=obstacle.botX-mode.scrollX
                RecLeftY=obstacle.botY-obstacle.height
                if botRightX==RecLeftX:
                    if (botRightY<=mode.platform and botRightY>=RecLeftY):
                        mode.gameOver=True

    #check if the player reaches the star and gets bonus points
    def checkBonusCollision(mode):
        for i in range(len(mode.bonusList)-1, -1, -1):
            star=mode.bonusList[i]
            if mode.topX+mode.squareSize>star.cx-mode.scrollX+star.r \
                and mode.topX<star.cx-mode.scrollX-star.r and \
                    mode.topY<star.cy-star.r:
                mode.bonusList.pop(i)
                return True

    def rotateSquare(mode):
        #the square rotates while jumping
        pass

    #adapted from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def drawGameOver(mode, canvas):
        if (mode.gameOver==True):
            canvas.create_image(300, 300, image=ImageTk.PhotoImage(mode.background))
            canvas.create_text(mode.width/2, mode.height/2-40, text='Game over!',
                            font='Arial 25 bold')
            canvas.create_text(mode.width/2, mode.height/2,
                            text=f'Your Final Score is: {mode.score}',
                            font='Arial 25 bold')
            canvas.create_text(mode.width/2, mode.height/2+40,
                            text='Press r to restart!',
                            font='Arial 25 bold')

    def redrawAll(mode, canvas):
        #draw the background
        canvas.create_image(300, 300, image=ImageTk.PhotoImage(mode.background))
       
        #draw the obstacles
        for obstacle in mode.obstacleList:
            if type(obstacle)==Triangle:
                obstacle.drawTriangle(obstacle.x-mode.scrollX, 
                    obstacle.y, canvas)
            elif type(obstacle)==Rectangle:
                obstacle.drawRectangle(obstacle.botX-mode.scrollX, 
                    obstacle.botY, canvas)
            elif type(obstacle)==Puddle:
                obstacle.drawPuddle(obstacle.topX-mode.scrollX, 
                    obstacle.topY, canvas)
            else:
                obstacle.drawBoth(obstacle.botX-mode.scrollX, obstacle.botY, 
                obstacle.triX-mode.scrollX, obstacle.triY, canvas)
        #draw bonus stars
        
        for star in mode.bonusList:
            star.drawBonusStar(star.cx-mode.scrollX, 
                    star.cy, canvas)
         # draw the player fixed to the left half of the scrolled canvas
        canvas.create_rectangle(mode.topX, mode.topY,\
        mode.topX + mode.squareSize, mode.topY + mode.squareSize,fill="yellow")
        r=10
        for (cx, cy) in mode.dots:
            canvas.create_oval(cx-r-mode.scrollX, cy-r, cx+r-mode.scrollX, \
                cy+r, fill='lightGreen')

        # draw the platform
        canvas.create_line(0, mode.platform, mode.width, mode.platform)
        # draw score
        canvas.create_text(50, 30, text=mode.message, fill="white")
        #draw gameOver
        mode.drawGameOver(canvas)

#the class for all the triangle objects
class Triangle(object):
    def __init__(self, x, y):
        #bottomLeft cordinate of the triangle
        self.x=x
        self.y=y
        self.size=40
        self.topY = self.y - (self.size**2 - (self.size/2)**2)**0.5

    def drawTriangle(self, x, y, canvas):
        canvas.create_polygon(x, self.y, x+self.size/2, \
            self.topY, x+self.size, self.y, fill="purple")

#the class for all the rectangle objects
class Rectangle(object):
    def __init__(self, botX, botY):
        #the bottomLeft corner of the rectangle
        self.botX=botX
        self.botY=botY
        self.width=350
        self.height=40

    def drawRectangle(self, botX, botY, canvas):
        canvas.create_rectangle(botX, self.botY-self.height, \
            botX+self.width, self.botY, fill="purple")

class Both(Rectangle):
    #an object with a triangle on top of the rectangle
    def __init__(self, botX, botY):
        super().__init__(botX, botY)
        self.size=40
        self.triX=self.botX+170
        self.triY=self.botY-self.height
        self.triTopY=self.triY - (self.size**2 - (self.size/2)**2)**0.5

    def drawBoth(self, botX, botY, triX, triY, canvas):
        canvas.create_rectangle(self.botX, self.botY-self.height, \
            self.botX+self.width, self.botY, fill="purple")
        canvas.create_polygon(self.triX, self.triY, self.triX+self.size/2, \
            self.triTopY, self.triX+self.size, self.triY, fill="purple")

#the class for all the puddle objects
class Puddle(object):
    def __init__(self, topX, topY):
        self.topX=topX
        self.topY=topY
        self.width=60
        self.height=10
    
    def drawPuddle(self, topX, topY, canvas):
        canvas.create_rectangle(topX, self.topY, \
            topX+self.width, self.topY+self.height, fill="red")

#the class for all the bonus stars
class BonusStar(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        colors = ['red', 'orange', 'yellow', 'green']
        self.fill = random.choice(colors)
        self.r = random.randint(5, 10)

    def drawBonusStar(self, cx, cy, canvas):
        canvas.create_oval(cx-self.r, cy-self.r,
                           cx+self.r, cy+self.r,
                           fill=self.fill)
        

class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.setActiveMode(app.gameMode)

app = MyModalApp(width=600, height=600)
