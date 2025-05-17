from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import random

ufo_pos_x = 0.0
ufo_pos_y = 100.0
ufo_pos_z = 0.0
ufo_rotation_x = 0.0
ufo_rotation_y = 0.0
ufo_rotation_z = 0.0
ufo_scale = 1.0


game_score = 0
life=5
missed=0

fovY = 120  
GRID_LENGTH = 600  

player_angle = 0
player_x, player_y= 0, 0  
dead=False

bullets = []
bullet_speed = 15

camera_radius = 500
camera_angle = 0  
camera_height = 500
cam_mode= 1  # 0 for first person, 1 for third person

x = camera_radius * math.sin(math.radians(camera_angle))
y = camera_radius * math.cos(math.radians(camera_angle))
z = camera_height
camera_pos = (x, y, z)
enemy=[]
enemy_head_radius = 50
enemy_body_radius = 100


cheat_mode = False
last_fire_time = 0 

frame_counter = 0
fire_interval = 100


class Bullet:
    def __init__(self, x, y, z, angle):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.speed = bullet_speed
        
        
    def move(self):
       
        rad = math.radians(-self.angle)
        self.x -= self.speed * math.sin(rad)
        self.y -= self.speed * math.cos(rad)
     
        
    def draw(self):
        glTranslatef(0,0,0)
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 0, 1)
        
        
        glColor3f(1, 0.5, 0)  
        glPushMatrix()
        glScalef(5, 30, 5)  
        glutSolidCube(1)
        glPopMatrix()
        
        glPopMatrix()
        
    def is_offscreen(self):
        
        return abs(self.x) > 600 or abs(self.y) > 600

class Enemy:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.body_radius = enemy_body_radius
        self.head_radius = enemy_head_radius
        self.shrink = True
        self.speed =  .5 

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(1, 0, 0)
        gluSphere(gluNewQuadric(), self.body_radius, 20, 20)  # main body

        # Head on top
        glTranslatef(0, 0, 150)  
        glColor3f(0, 0, 0)
        gluSphere(gluNewQuadric(), self.head_radius, 20, 20)
        glPopMatrix()
    
    def move_enemy(self, player_x, player_y):

        dir_x = player_x - self.x
        dir_y = player_y - self.y
        

        distance = math.sqrt(dir_x**2 + dir_y**2)
        

        if distance > 0:
            dir_x /= distance
            dir_y /= distance

        self.x += dir_x * self.speed
        self.y += dir_y * self.speed

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_shapes():

    glPushMatrix()  # Save the current matrix state
    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 0)  
    glutSolidCube(60) # Take cube size as the parameter
    glTranslatef(0, 0, 100) 
    glColor3f(0, 1, 0)
    glutSolidCube(60) 

    glColor3f(1, 1, 0)
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glTranslatef(100, 0, 100) 
    glRotatef(45, 0, 1, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    glColor3f(0, 1, 1)
    glTranslatef(300, 0, 100) 
    gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks

    glPopMatrix()  # Restore the previous matrix state

def draw_arena():
   
    c = 0
    glBegin(GL_QUADS)
    for i in range(600, -600, -60):
        for j in range(600, -600, -60):
            if c % 2 == 0:
                glColor3f(1, 1, 1)  
            else:
                glColor3f(0.7, 0.5, 0.95)  
            glVertex3f(i, j, 0)
            glVertex3f(i-60, j, 0)
            glVertex3f(i-60, j-60, 0)
            glVertex3f(i, j-60, 0)
            
            c = c + 1
        c = c + 1
    glColor3f(0,0,1)
    #blue waall
    glVertex3f(600, 600, 0)
    glVertex3f(600, -600, 0)
    glVertex3f(600, -600, 200)
    glVertex3f(600, 600, 200)

    #cyaan wall
    glColor3f(0,1,1)
    glVertex3f(600, -600, 0)
    glVertex3f(-600, -600, 0)
    glVertex3f(-600, -600, 200)
    glVertex3f(600, -600, 200)

    #green wall
    glColor3f(0,1,0)
    glVertex3f(-600, -600, 0)
    glVertex3f(-600, 600, 0)
    glVertex3f(-600, 600, 200)
    glVertex3f(-600, -600, 200)
    
    #red wall
    glColor3f(1,0,0)
    glVertex3f(-600, 600, 0)
    glVertex3f(600, 600, 0)
    glVertex3f(600, 600, 200)
    glVertex3f(-600, 600, 200)

    glEnd()
        
def draw_player():
    global player_angle, player_x, player_y,dead,enemy

    glPushMatrix()
   
    glTranslatef(player_x, player_y, 0)
    glRotatef(player_angle, 0, 0, 1)
    if dead:
        glRotatef(-90, 1, 0, 0)
    # Legs
    glColor3f(1, 1, 0)
    # Left leg
    glPushMatrix()
    glTranslatef(-15, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 20, 65, 10, 10)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(15, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 20, 65, 10, 10)
    glPopMatrix()

    # Body
    glPushMatrix()
    glTranslatef(0, 0, 95)
    glColor3f(0, 1, 0)
    glScalef(1.5, 1, 1.2)
    glutSolidCube(60)
    glPopMatrix()

    # Left Arm
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(50, 0, 105)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 20, 10, 65, 10, 10)
    glPopMatrix()

    # Right Arm
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(-50, 0, 105)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 20, 10, 65, 10, 10)
    glPopMatrix()

    # Gun 
    glPushMatrix()
    glColor3f(0, 1, 1)
    glTranslatef(0, 0, 105)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 20, 10, 95, 10, 10)
    glPopMatrix()


    # Head
    glPushMatrix()
    glTranslatef(0, 0, 155)  
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 25, 20, 20)
    glPopMatrix()
    glPopMatrix()
def draw_ufo(pos_x=0, pos_y=0, pos_z=0, 
             scale=1.0, rotate_x=0, rotate_y=0, rotate_z=0):
    """
    Draw the complete UFO with animation parameters
    
    Parameters:
    - time: Current time value for animations
    - beam_active: Boolean to toggle the beam
    - pos_x, pos_y, pos_z: Position of the UFO in 3D space
    - scale: Size scale factor
    - rotate_x, rotate_y, rotate_z: Rotation angles in degrees
    """
    glPushMatrix()
    
    # Apply position, scale and rotation transformations
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(rotate_x, 1, 0, 0)
    glRotatef(rotate_y, 0, 1, 0)
    glRotatef(rotate_z, 0, 0, 1)
    glScalef(scale, scale, scale)
    
    # Add a gentle hovering motion

    
    # --- UFO BODY (MAIN DISC) ---
    glColor3f(0.7, 0.7, 0.7)  # Silver color for the body
    glPushMatrix()
    glScalef(1.0, 0.25, 1.0)  # Flatten the sphere to make it disc-like
    gluSphere(gluNewQuadric(), 60.0, 32, 32)  # Main body
    glPopMatrix()
    
    # --- COCKPIT (DOME) ---
    glColor3f(0.2, 0.5, 0.8)  # Blue-tinted glass
    glPushMatrix()
    glTranslatef(0.0, 15.0, 0.0)  # Position on top of the body
    glScalef(0.5, 0.3, 0.5)  # Scale to create dome shape
    gluSphere(gluNewQuadric(), 60.0, 32, 16)  # Dome
    glPopMatrix()
    
    # --- BOTTOM SECTION ---
    glColor3f(0.4, 0.4, 0.4)  # Darker gray for bottom
    glPushMatrix()
    glTranslatef(0.0, -10.0, 0.0)  # Position under the body
    glScalef(0.7, 0.15, 0.7)  # Scale to create the shape
    gluSphere(gluNewQuadric(), 60.0, 32, 16)  # Bottom section
    glPopMatrix()
    
    # --- LANDING LEGS ---
    glColor3f(0.3, 0.3, 0.3)  # Dark gray for legs
    for i in range(3):
        angle = i * 120  # 120 degrees apart
        x = 40 * math.cos(math.radians(angle))
        z = 40 * math.sin(math.radians(angle))
        
        glPushMatrix()
        glTranslatef(x, -15.0, z)  # Position around the bottom
        glRotatef(60, -z, 0, x)  # Angle the leg outward
        
        # Leg
        glPushMatrix()
        glRotatef(90, 1, 0, 0)  # Rotate to point downward
        quadric = gluNewQuadric()
        gluCylinder(quadric, 5.0, 5.0, 30.0, 8, 8)  # Parameters: quadric, base radius, top radius, height, slices, stacks
        glPopMatrix()
        
        # Foot
        glTranslatef(0.0, -30.0, 0.0)
        glColor3f(0.5, 0.5, 0.5)
        glutSolidSphere(8.0, 8, 8)  # Parameters: radius, slices, stacks
        glPopMatrix()
    
    # --- LIGHTS ---

    # --- BEAM ---

    
    glPopMatrix()
def draw_enemy():
    global dead
    if not dead:
        for i in range(0, 5):
            if len(enemy) >= 5:
                break
            x=random.randint(-550, 550)
            y=random.randint(-550, 550)
            z=50
            enemy.append(Enemy(x, y, z))
        for e in enemy:
            e.draw()


def update_enemy_pos():
    global enemy, player_x, player_y
    for e in enemy:
        e.move_enemy(player_x, player_y)

def hit():
    global bullets, enemy,missed,game_score

    new_enemies = []
    for e in enemy:
        hit = False
        for b in bullets:
            dx = b.x - e.x
            dy = b.y - e.y
            dz = b.z - e.z
            distance = math.sqrt(dx**2 + dy**2 + dz**2)
            if distance < e.body_radius:
                hit = True
                break
        if hit:
            game_score += 1
            print("Player Bullet Fired!")
            new_enemies.append(Enemy(random.randint(-550, 550), random.randint(-550, 550), 50))
            bullets = [b for b in bullets if math.sqrt((b.x - e.x)**2 + (b.y - e.y)**2 + (b.z - e.z)**2) >= e.body_radius]
        else:
   
            new_enemies.append(e)

    enemy = new_enemies

def catch():
    global missed, game_score, life,enemy,player_x, player_y,life,dead
    if dead:
        return
    for e in enemy:
        dx = player_x - e.x
        dy = player_y - e.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance<= 50:
            life -= 1
            print("Remaining Player Life: ", life)
            if life==0:
                dead= True
            e.x = random.randint(-550, 550)
            e.y = random.randint(-550, 550)
            break

def check_line_of_sight(enemy_x, enemy_y):
    """Check if an enemy is in line of sight of the player's gun."""
    rad = math.radians(-player_angle)
    dir_x = -math.sin(rad)
    dir_y = -math.cos(rad)
    

    to_enemy_x = enemy_x - player_x
    to_enemy_y = enemy_y - player_y
    

    distance = math.sqrt(to_enemy_x**2 + to_enemy_y**2)
    

    if distance > 0:
        to_enemy_x /= distance
        to_enemy_y /= distance
    

    dot_product = dir_x * to_enemy_x + dir_y * to_enemy_y
    

    return dot_product > 0.9 and distance < 500 



def keyboardListener(key, X, Y):
    global player_angle, player_x, player_y, missed, game_score, life, cam_mode, enemy, camera_angle, camera_height, x, y, z, camera_radius,dead,cheat_mode

    step = 10  
    rot_step = 5  
    


    if key == b'c' or key == b'C':
        cheat_mode = not cheat_mode

    step = 10 
    rot_step = 5 
    if not dead:
        if key == b'a': 
            player_angle += rot_step

        if key == b'd': 
            player_angle -= rot_step

        if key == b's': 
            rad = math.radians(-player_angle)
            new_x = player_x + step * math.sin(rad)
            new_y = player_y + step * math.cos(rad)
            if -600 < new_x < 600 and -600 < new_y < 600:
                player_x, player_y = new_x, new_y

        if key == b'w': 
        
            rad = math.radians(-player_angle)
            new_x = player_x - step * math.sin(rad)
            new_y = player_y - step * math.cos(rad)
            if -600 < new_x < 600 and -600 < new_y < 600:
                player_x, player_y = new_x, new_y
                
    if key == b'r':  
    
        missed = 0
        game_score = 0
        life = 5
        
       
        player_angle = 0
        player_x, player_y = 0, 0
        
        camera_radius = 500
        camera_angle = 0
        camera_height = 500

        dead = False  
        
        global x, y, z  
        x = camera_radius * math.sin(math.radians(camera_angle))
        y = camera_radius * math.cos(math.radians(camera_angle))
        z = camera_height
        
        
        cam_mode = 1
        
        
        bullets.clear()
        enemy.clear()
        
     
        for i in range(5):
            enemy_x = random.randint(-550, 550)
            enemy_y = random.randint(-550, 550)
            enemy.append(Enemy(enemy_x, enemy_y, 50))

    glutPostRedisplay()


def specialKeyListener(key, X, Y):
    global camera_angle, camera_height,x,y,z, camera_radius

    if key == GLUT_KEY_LEFT:
        camera_angle += 2  
    elif key == GLUT_KEY_RIGHT:
        camera_angle -= 2  
    elif key == GLUT_KEY_UP:
        camera_height += 10 
    elif key == GLUT_KEY_DOWN:
        camera_height -= 10 

    


    x = camera_radius * math.sin(math.radians(camera_angle))
    y = camera_radius * math.cos(math.radians(camera_angle))
    z = camera_height


    glutPostRedisplay()


def shoot_bullet():
    global bullets, player_angle, player_x, player_y,cam_mode,dead

    rad = math.radians(-player_angle)
    gun_length = -100  

   
    bullet_x = player_x + gun_length * math.sin(rad)
    bullet_y = player_y + gun_length * math.cos(rad)
    bullet_z = 105  

    bullet = Bullet(bullet_x, bullet_y, bullet_z, player_angle)
    bullets.append(bullet)

def mouseListener(button, state, x, y):
    global bullets, player_angle, player_x, player_y,cam_mode,dead

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not dead:
        shoot_bullet()

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if cam_mode == 0:
            cam_mode = 1
        else:
            cam_mode = 0

def enemy_shrinking():
    for e in enemy:
        if e.shrink:
            e.body_radius -= 0.1
            e.head_radius -= 0.1
            if e.body_radius <= 50 or e.head_radius <= 25:
                e.shrink= False
        else:
            e.body_radius += 0.1
            e.head_radius += 0.1
            if e.body_radius >= 100 or e.head_radius >= 50:
                e.shrink= True

def animate_bullet():
    global bullets, missed,dead
    
    for bullet in bullets:
        bullet.move()
    
    
    old_len = len(bullets)
    bullets[:] = [b for b in bullets if not b.is_offscreen()]
    missed_bullets = old_len - len(bullets)
    missed += missed_bullets
    if missed_bullets > 0:
        print("Bullet Missed: ", missed)
    if missed==10:
        dead= True


def cheat():
    global player_angle, player_x, player_y, cheat_mode, bullets, enemy, frame_counter, fire_interval, dead
    
    if cheat_mode and not dead:
        # Rotate player gun automatically
        player_angle += 1
        if player_angle >= 360:
            player_angle -= 360
            
        
        frame_counter += 1
        if frame_counter >= fire_interval:
            for e in enemy:
                if check_line_of_sight(e.x, e.y):
                    shoot_bullet()
                    frame_counter = 0  
                    break  



def setupCamera():
    global cam_mode, player_x, player_y, player_angle, x, y, z

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if cam_mode == 0:  
        eye_x = player_x
        eye_y = player_y
        eye_z = 155+50 

        rad = math.radians(-player_angle)
        look_x = eye_x - 100 * math.sin(rad)
        look_y = eye_y - 100 * math.cos(rad)
        look_z = eye_z

        gluLookAt(eye_x, eye_y, eye_z,  
                  look_x, look_y, look_z, 
                  0, 0, 1) 

    elif cam_mode == 1:  
        gluLookAt(x, y, z,
                  0, 0, 0,  
                  0, 0, 1)  

def idle():
    global player_angle, bullets, last_fire_time
    
    # Existing code
    animate_bullet()
    enemy_shrinking()
    update_enemy_pos()
    hit()
    catch()
    cheat()
    

    
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
    draw_arena()
    draw_player()
    draw_enemy()
    draw_ufo(
        pos_x=ufo_pos_x,
        pos_y=ufo_pos_y,
        pos_z=ufo_pos_z,
        scale=ufo_scale,
        rotate_x=ufo_rotation_x,
        rotate_y=ufo_rotation_y,
        rotate_z=ufo_rotation_z
    )

    
    for bullet in bullets:
        bullet.draw()
    if dead:
        draw_text(10, 770, f"Game is Over. Your Score is: {game_score}")
        draw_text(10, 740, f"Press 'R' to Restart")
    else:
    # Display game info text at a fixed screen position
        draw_text(10, 770, f"Player Life Remaining: {life}")
        draw_text(10, 740, f"Game Scoore: {game_score}")
        draw_text(10, 710, f"Player Bullet Missed: {missed}")



    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window



    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()