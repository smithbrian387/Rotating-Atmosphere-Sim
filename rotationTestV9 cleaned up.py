# import pygame module in this program
import pygame, pygame.freetype, sys
from pygame.locals import *
from random import randrange

# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# create the display surface object of specific dimension
win = pygame.display.set_mode((1000, 1000))

# set the pygame window name
pygame.display.set_caption("Rotation")

#Rotational Center coordinates
xCen = 500
yCen = 500

#How much the rotational planes pull on neighboring planes
frictionCoeff = 3

# Rate at which time moves in ms. Changing time step doesn't affect relative motion
timeStep = 10

#Sets the velocity of the base "planet"
baseVel = 2

#Sets the spacing between objects
spacing = 3

#Sets the number/size of objects
objNum = 0
objSize = 3

#Making a slider
redColor = pygame.Color(255,0,0)
blackColor = pygame.Color(0,0,0)

#Defining control sliders
sliderObjNum = objNum
sliderBaseVel = baseVel*100
sliderFrictionCoeff = frictionCoeff*100

#Slider labels
font = pygame.freetype.SysFont(pygame.font.get_default_font(), 24)

class rotatingObject:
    def __init__(self, rotationRadius, x, size, vel):
        self.rotationRadius = rotationRadius
        self.x = x
        self.y = 0
        self.size = size
        self.vel = vel
        self.aligned = False
        

#Making a list of classes
objectList = []

#Define the "planet" rotation
objectList.append(rotatingObject(100, xCen, 10, baseVel))

#initialze atmospheric layers
for i in range(objNum):
    objectList.append(rotatingObject(120 + spacing*(i+1), xCen, objSize, 0))


# Indicates pygame is running
run = True

# infinite loop
while run:
    # creates time delay of timeStep in ms
    pygame.time.delay(timeStep)
    
    # check for ESC key pressed, or pygame window closed, to quit
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    #Connect slider to object numbers
    button = pygame.mouse.get_pressed()
    clickX = 0
    clickY = 0
    if button[0] != 0:
        pos = pygame.mouse.get_pos()
        clickX = pos[0]
        clickY = pos[1]

    #objNum Slider, top slider in Y [0,100]
    if clickY >0 and clickY < 100:
        sliderObjNum = int(clickX/10)
        if sliderObjNum > objNum:
            for i in range(sliderObjNum-objNum):
                objectList.append(rotatingObject(120 + spacing*(objNum+i+1), xCen, objSize, 0))
        elif sliderObjNum < objNum:
            for i in range(objNum-sliderObjNum):
                objectList.pop()
        objNum = sliderObjNum

    #sliderBaseVel slider
    elif clickY > 100 and clickY < 200:
        sliderBaseVel = clickX - xCen
        baseVel = sliderBaseVel/100
        objectList[0].vel = baseVel

    #sliderFrictionCoeff slider
    elif clickY > 200 and clickY < 300:
        sliderFrictionCoeff = clickX
        frictionCoeff = sliderFrictionCoeff/100

    #Get list of angular velocities for calculating speed changes before updating anything
    curVel = []
    for i in range(len(objectList)):
        curVel.append(objectList[i].vel)

    #Updating position and velocity of the list of rotatingObjects
    for i in range(len(objectList)):     
        #Position adjustment
        dirToCen = [xCen-objectList[i].x ,yCen-objectList[i].y]
        dirVel = [dirToCen[1], -dirToCen[0]]
    
        objectList[i].x += (dirVel[0]/objectList[i].rotationRadius)*objectList[i].vel
        objectList[i].y += (dirVel[1]/objectList[i].rotationRadius)*objectList[i].vel

        #Adjust velocity by ANGULAR velocity difference to lower rotational plane
        if i > 0 and i < len(curVel)-1:
            lowerVelDiff = ((curVel[i-1]/objectList[i-1].rotationRadius)-(curVel[i]/objectList[i].rotationRadius))
            upperVelDiff = ((curVel[i+1]/objectList[i+1].rotationRadius)-(curVel[i]/objectList[i].rotationRadius))
            velUpdate = lowerVelDiff + upperVelDiff
            objectList[i].vel += velUpdate*(frictionCoeff)

        #Update outer object
        elif i == len(curVel)-1:
            lowerVelDiff = ((curVel[i-1]/objectList[i-1].rotationRadius)-(curVel[i]/objectList[i].rotationRadius))
            velUpdate = lowerVelDiff
            objectList[i].vel += velUpdate*(frictionCoeff)

    
        #This is the larger radius as a result of tangential movement
        newRad = ((xCen-objectList[i].x)**2+(yCen-objectList[i].y)**2)**0.5
        
        #new vector pointing toward rotational center
        #newDirToCen = [xCen-objectList[i].x,yCen-objectList[i].y]
        
        objectList[i].x = xCen + (objectList[i].x-xCen) / (newRad/objectList[i].rotationRadius)
        objectList[i].y = yCen + (objectList[i].y-yCen) / (newRad/objectList[i].rotationRadius)

    #Refresh the screen
    win.fill(blackColor)
    pygame.draw.circle(win, (27, 33, 219),(xCen, yCen),100+objectList[0].size+5)
    #Drawing objects on screen
    for obj in objectList:
        pygame.draw.circle(win, (27, 219, 149),(obj.x,obj.y),obj.size)
        pygame.draw.circle(win, (27, 219, 149),(obj.x-2*(obj.x-xCen),obj.y-2*(obj.y-yCen)),obj.size)

    #Slider Labels
    font.render_to(win, (840, 40), "Objects: " +str(objNum), redColor)
    font.render_to(win, (840, 140), "Velocity: " +str(sliderBaseVel), (213,34,102))
    font.render_to(win, (840, 240), "Friction: " +str(sliderFrictionCoeff), (108,200,5))

    
    #Update slider positions
    pygame.draw.rect(win,redColor,Rect(sliderObjNum*10,5,10,90))
    pygame.draw.rect(win,(213,34,102),Rect(sliderBaseVel+xCen,105,10,90))
    pygame.draw.rect(win,(108,200,5),Rect(sliderFrictionCoeff,205,10,90))
    
    #Refresh the window
    pygame.display.update()

# closes the pygame window
pygame.quit()
















