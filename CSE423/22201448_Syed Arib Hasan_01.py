from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


### TASK 1 ###
w,g,b=1.0,171/255,240/255
d=.05
rain_angle = 0
angle_change = 2
def draw_points(x, y):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()


def iterate():
    glViewport(0, 0, 1920, 1080)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1920, 0.0, 1080, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def sky_ground():
    glutPostRedisplay()
    global w,g,b
    #sky
    glBegin(GL_TRIANGLES)
    glColor3f(w,w,w)
    glVertex2f(0, 720)
    glVertex2f(1920, 720)
    glColor3f(0.0, g, b)
    glVertex2f(0, 1080)
    
    glColor3f(w,w,w)
    glVertex2f(1920, 720)
    glColor3f(0.0, g, b)
    glVertex2f(1920, 1080)
    glVertex2f(0, 1080)
    #ground
    glColor3f(102/255, 51/255, 0/255)
    glVertex2f(0, 720)
    glVertex2f(0, 0)
    glVertex2f(1920, 0)
    
    glVertex2f(0, 720)
    glVertex2f(1920, 720)
    glVertex2f(1920, 0)
    glEnd()

def tree():
    glBegin(GL_TRIANGLES)
    x=0
    while x<1920:
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(x, 560)
        glColor3f(102/255, 51/255, 0/255)
        glVertex2f(x+50, 700)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(x+100, 560)
        x+=100
    glEnd()
def drawAxes(x1, y1, x2, y2):
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0, 1.0, 0.0)
    glVertex2f(0, 0)
    glEnd()
def house():
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 102/255,102/255)
    glVertex2f(640,580)
    glVertex2f(640,380)
    glVertex2f(800,380)
    glVertex2f(640,580)
    glVertex2f(800,580)
    glVertex2f(800,380)

    glColor3f(0.0, 153/255, 153/255)
    glVertex2f(800,580)
    glVertex2f(800,380)
    glVertex2f(1280,380)

    glVertex2f(800,580)
    glVertex2f(1280,580)
    glVertex2f(1280,380)

    #SMALL roof
    glColor3f(0/255, 51/255,102/255)
    glVertex2f(640,580)
    glVertex2f(720,750)
    glVertex2f(800,580)

    #big roof
    glColor3f(0.0, 102/255, 204/255)
    glVertex2f(720,750)
    glVertex2f(800,580)
    glVertex2f(1280,580)
    glVertex2f(720,750)
    glVertex2f(1200,750)
    glVertex2f(1280,580)

    #DOOR
    glColor3f(51/255, 0/255, 25/255)
    glVertex2f(670,380)
    glVertex2f(670,520)
    glVertex2f(770,380)

    glVertex2f(670,520)
    glVertex2f(770,520)
    glVertex2f(770,380)

    #knob
    glColor3f(0.0, 102/255, 204/255)
    glVertex2f(680, 450)
    glVertex2f(680, 440)
    glVertex2f(690, 440)

    glVertex2f(680, 450)
    glVertex2f(690, 450)
    glVertex2f(690, 440)

    #window1
    glColor3f(1,1,0)
    glVertex2f(870, 560)
    glVertex2f(870, 460)
    glVertex2f(970, 460)

    glVertex2f(870, 560)
    glVertex2f(970, 560)
    glVertex2f(970, 460)

    #window2
    glColor3f(1,1,0)
    glVertex2f(1130, 560)
    glVertex2f(1130, 460)
    glVertex2f(1230, 460)

    glVertex2f(1130, 560)
    glVertex2f(1230, 560)
    glVertex2f(1230, 460)
    glEnd()


    #window1 line
    drawAxes(920,460,920,560)
    drawAxes(1180,460,1180,560)
    drawAxes(870,510,970,510)
    drawAxes(1130,510,1230,510)
def rain():
    global rain_angle
    a=random.randint(0,100)
    glLineWidth(2)
    glBegin(GL_LINES)
    
    r,g,b=0,0,0
    if a%2==0:
        r,g,b=1,1,1
    else:
        r,g,b=0,0,1
    
    glColor3f(r,g,b) 
    
    for _ in range(50):
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        rain_length = random.randint(0,40) 
        x_prime = rain_length * (rain_angle / 45.0)
        
        glVertex2f(x, y)
        glVertex2f(x + x_prime, y - rain_length)
    
    glEnd()

def specialKeyListener(key, x, y):
    global rain_angle
    if key == GLUT_KEY_DOWN:
        rain_angle = max(rain_angle - angle_change, -45)
    elif key == GLUT_KEY_UP:
        rain_angle = min(rain_angle + angle_change, 45)

    
    glutPostRedisplay()
def keyboardListener(key, x, y):
    global w, g, b, d
    if key==b'w':
        w = max(0.0, w - d)  
        g = max(0.0, g - d) 
        b = max(0.0, b - d)  

    elif key==b's':
        w = min(1.0, w + d)
        g = min(171/255, g + d)
        b = min(240/255, b + d)
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1, 1, 1.0) #konokichur color set (RGB)
    #call the draw methods here
    sky_ground()
    tree()
    house()
    rain()
    glutSwapBuffers()


    

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1920, 1080) #window  
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)


glutMainLoop()



# ### TASK 2 ###

# import random
# class Dot():
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         r,g,b=random.uniform(0.01,1.0),random.uniform(0.01,1.0),random.uniform(0.01,1.0)
#         self.color=(r,g,b)
#         self.velocity=random.choice([(-1,1),(1,1),(-1,-1),(1,-1)])

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import time

# W_Width, W_Height = 800,500  
# points = []
# speed = 0.01
# freeze=False
# blinking = False  
# rectangle_visible = False 

# def draw_points(): 
#     glutPostRedisplay()
#     glPointSize(5) #pixel size. by default 1 thake
#     glBegin(GL_POINTS)
#     for p in points:
#         x,y=p.x,p.y
#         r,g,b=p.color
#         glColor3f(r,g,b) #konokichur color set (RGB)
#         glVertex2f(x,y) #jekhane show korbe pixel
#     glEnd()

# def draw_box():
#     glBegin(GL_LINES)
#     glColor3f(1.0, 1.0, 1.0)
#     glVertex2f(10, 10)
#     glVertex2f(10, 490)

#     glVertex2f(790, 10)
#     glVertex2f(790, 490)

#     glVertex2f(10, 10)
#     glVertex2f(790, 10)

#     glVertex2f(10, 490)
#     glVertex2f(790, 490)
#     glEnd()

# def draw_rectangle():
#     global rectangle_visible
#     if rectangle_visible:
#         glBegin(GL_TRIANGLES)
#         glColor3f(0.0, 0.0, 0.0)

#         glVertex2f(10, 10)    
#         glVertex2f(10, 489)   
#         glVertex2f(789, 10)  

#         glVertex2f(10, 489)   
#         glVertex2f(789, 10)  
#         glVertex2f(789, 489)  

#         glEnd()

# def convert_coordinate(x,y):
#     return x, W_Height - y



# def animate():
#     if freeze:
#         return
#     for p in points:
#         p.x+=p.velocity[0]*speed
#         p.y+=p.velocity[1]*speed
#         if p.x>=790 or p.x<=10:
#             p.velocity=(p.velocity[0]*-1,p.velocity[1])
#         if p.y>=490 or p.y<=10:
#             p.velocity=(p.velocity[0],p.velocity[1]*-1)

# def blinker(value):

#     global rectangle_visible, blinking
#     if blinking:
#         rectangle_visible = not rectangle_visible 
#         glutPostRedisplay()
#         glutTimerFunc(500, blinker, 0) 
# def iterate():
#     glViewport(0, 0, 800, 500)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 800, 0.0, 500, 0.0, 1.0)
#     glMatrixMode (GL_MODELVIEW)
#     glLoadIdentity()

# def specialKeyListener(key, x, y):
#     global speed
#     if key=='w':
#         print(1)
#     if key==GLUT_KEY_UP:
#         speed *= 2
#         print("Speed Increased")
#     if key== GLUT_KEY_DOWN:		#// up arrow key
#         speed /= 2
#         print("Speed Decreased")
#     glutPostRedisplay()

# def mouseListener(button, state, x, y):
#     global blinking
#     if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
#         if freeze:
#             return
#         print("Left button pressed at ", x, y)
#         x, y = convert_coordinate(x, y)
#         print("Converted: ", x, y)
#         p=Dot(x,y)
#         points.append(p)
#     if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#         blinking = not blinking
#         if blinking:
#             blinker(0)
#     glutPostRedisplay()

# def keyboardListener(key, x, y):
#     global freeze
#     if key==b' ':
#         freeze=not freeze
#     glutPostRedisplay()

# def showScreen():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()
#     glColor3f(1, 1, 1.0) #konokichur color set (RGB)
#     #call the draw methods here
#     draw_box()
#     draw_points()
#     draw_rectangle()
#     glutSwapBuffers()


    

# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(800, 500) #window  
# glutInitWindowPosition(0, 0)
# wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
# glutDisplayFunc(showScreen)
# glutIdleFunc(animate)
# glutMouseFunc(mouseListener)
# glutSpecialFunc(specialKeyListener)
# glutKeyboardFunc(keyboardListener)
# glutMainLoop()






