from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
last_time = time.time()
diamond_speed = 100
bucket_speed = 100
bucket_x0=190
bucket_x1=310
diamond_x=random.randint(20,470)
diamond_y=500
game_paused = False
game_over= False
br,bg,bb=1.0,1.0,1.0
dr,dg,db=random.uniform(0.01,1.0),random.uniform(0.01,1.0),random.uniform(0.01,1.0)
score=0
def findzone(x,y,x1,y1):
    dx = x1 - x
    dy = y1 - y
    if dx == 0: 
        if dy > 0:
            return 1  
        else:
            return 5 
    if abs(dx)>=abs(dy):
        if dx>0 and dy>0:
            return 0
        elif dx<0 and dy>0:
            return 3
        elif dx<0 and dy<0:
            return 4
        else:
            return 7
    else:
        if dx>0 and dy>0:
            return 1
        elif dx<0 and dy>0:
            return 2
        elif dx<0 and dy<0:
            return 5
        else:
            return 6
        
def convert_zone0(x,y,n):
    if n==0:
        return x,y
    elif n==1:
        return y,x
    elif n==2:
        return y,-x
    elif n==3:
        return -x,y
    elif n==4:
        return -x,-y
    elif n==5:
        return -y,-x
    elif n==6:
        return -y,x
    else:
        return x,-y
def convert_from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    else:  
        return x, -y
def draw_points(x, y, x1, y1):
    glPointSize(2)
    glBegin(GL_POINTS)
    z = findzone(x, y, x1, y1)
    x0, y0 = convert_zone0(x, y, z)
    xi, yi = convert_zone0(x1, y1, z)
    if x0 > xi:
        x0, y0, xi, yi = xi, yi, x0, y0
    dx = xi - x0
    dy = yi - y0
    d = 2 * dy - dx
    de = 2 * dy
    dne = 2 * (dy - dx)
    x, y = x0, y0
    X, Y = convert_from_zone0(x, y, z)
    glVertex2i(int(round(X)), int(round(Y)))
    while x < xi:
        if d < 0:
            x += 1
            d += de
        else:
            x += 1
            y += 1
            d += dne
        X, Y = convert_from_zone0(x, y, z)
        glVertex2i(int(round(X)), int(round(Y)))
    glEnd()


def draw_back():
    glColor3f(0.0, 1.0, 1.0)
    draw_points(10,560,50,560)
    draw_points(10,560,30,575)
    draw_points(10,560,30,545)

def draw_pause():
    glColor3f(1.0,1.0,0.0)
    draw_points(245,545,245,575)
    draw_points(255,545,255,575)

def draw_play():

    glColor3f(1.0, 0.75, 0.0)  
    draw_points(245,545,245,575)
    draw_points(245,575,260,560)
    draw_points(245,545, 260,560)

def draw_cross():
    glColor3f(1.0, 0.0, 0.0)
    draw_points(450,545,480,575)
    draw_points(450,575,480,545)

def draw_bucket(x0,x1):
    global br,bg,bb
    glColor3f(br,bg,bb)
    draw_points(x0,5,x1,5)
    draw_points(x0-20,25,x1+20,25)
    draw_points(x0-20,25,x0,5)
    draw_points(x1+20,25,x1,5)

def draw_diamond(x, y):
    global dr,dg,db
    glColor3f(dr,dg,db)
    width = 20
    height = 30
    draw_points(x,y, x + (width*.5), y + (height*.5))
    draw_points(x, y, x + width*.5, y - height*.5)
    draw_points(x + width*.5, y - height*.5, x+width, y)
    draw_points(x + width*.5, y + height*.5, x+width, y)


def specialKeyListener(key, x, y):
    global bucket_x0, bucket_x1,game_paused, game_over
    if game_paused or game_over:
        return
    if key==GLUT_KEY_RIGHT:
        if bucket_x1+25<500:
            bucket_x0+=10
            bucket_x1+=10


    elif key==GLUT_KEY_LEFT:
        if bucket_x0-25>0:
            bucket_x0-=10
            bucket_x1-=10



    glutPostRedisplay()
    
def mouseListener(button, state, x, y):
    global game_paused,score, diamond_x, diamond_y, br, bg, bb, game_over, bucket_x0, bucket_x1, dr, dg, db, diamond_speed, last_time
    y = 600 - y 

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 240 <= x <= 260 and 545 <= y <= 575 and not game_over:
            game_paused = not game_paused
        elif 10 <= x <= 50 and 545 <= y <= 575:
            print("Starting Over!")   
            score = 0
            dr, dg, db = random.uniform(0.01, 1.0), random.uniform(0.01, 1.0), random.uniform(0.01, 1.0)
            diamond_x = random.randint(60, 470)
            diamond_y = 500
            br, bg, bb = 1.0, 1.0, 1.0
            game_paused = False
            game_over = False
            diamond_speed = 100
            last_time = time.time()
            bucket_x0 = 190
            bucket_x1 = 310
        elif 450 <= x <= 480 and 545 <= y <= 575:
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()
        

    glutPostRedisplay()


def iterate():
    glViewport(0, 0, 500, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 600, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1, 1, 1.0) #konokichur color set (RGB)
    #call the draw methods here
    draw_back()
    if game_paused:
        draw_play()
    else:
        draw_pause()
    draw_cross()
    draw_bucket(bucket_x0,bucket_x1)
    draw_diamond(diamond_x,diamond_y)
    glutSwapBuffers()

def animate():
    global diamond_y, diamond_x, score, game_paused, bucket_x0, bucket_x1, game_over, br, bg, bb, dr, dg, db, last_time, diamond_speed
    if game_over:
        return
    current_time = time.time()
    if game_paused:
        last_time = current_time 
        glutPostRedisplay()
        return
    delta_time = current_time - last_time
    last_time = current_time
    diamond_y -= diamond_speed * delta_time



    if diamond_y-15<= 25 and diamond_y > 0:
        if (diamond_x >= (bucket_x0-20)) and (diamond_x+10 <= (bucket_x1+20)):
            score += 1
            print("Score:", score)
            dr,dg,db=random.uniform(0.01,1.0),random.uniform(0.01,1.0),random.uniform(0.01,1.0)
            diamond_y = 500
            diamond_x = random.randint(0, 470)
            diamond_speed += 20
    if diamond_y <= -20:
        game_over = True
        br, bg, bb = 1.0, 0.0, 0.0       
        print("Game Over! Final Score:", score)
                
    glutPostRedisplay()

    

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 600) #window  
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutIdleFunc(animate)
glutMainLoop()