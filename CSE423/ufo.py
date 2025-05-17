from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random, time, math

# Window and world constants
WINDOW_W, WINDOW_H = 1000, 800
WORLD_W, WORLD_H, WORLD_D = 800.0, 600.0, 800.0   
SCROLL_S = 50.0  
SCROLL_SPEEDS = {
    "stars":  SCROLL_S * 0.1,
    "planets": SCROLL_S * 0.3,
    "asteroids": SCROLL_S * 0.5,
    "ships": SCROLL_S * 0.75,
    "obstacles": SCROLL_S,
}

# Object counts
N_STARS, N_PLANETS, N_ASTEROIDS, N_SHIPS, N_OBSTACLES = 400, 7, 30, 3, 30
if N_OBSTACLES ==0:
    N_OBSTACLES = 30

# Colors
Planet_colour = [random.uniform(0.15, 0.55), random.uniform(0.05, 0.75)]
BG_TOP = (0.18, 0.38, 0.92)
BG_BOT = (0.01, 0.05, 0.25)

# Game objects
stars, planets, asteroids, ships, obstacles = [], [], [], [], []
projectiles = []

# Game state
last_time = 0.0
ufo_pos_x = -150.0
ufo_pos_y = 0
ufo_pos_z = 0.0
ufo_rotation_angle = 0.0
ufo_rotation_speed = 0.8
gun_rotation_angle = 0.0  # New variable to track gun rotation
is_firing = False
is_first_person = False  # Toggle for camera view
score = 0
lives = 3
bullets = []
bullet_speed = 2
health=90

class Obstacle:
    def __init__(self, z_offset=0.0):
        self.x = WORLD_W / 2 + z_offset
        self.y = random.uniform(-100.0, 100.0)
        self.z = random.uniform(-20.0, 20.0)
        self.rotation = random.uniform(0, 360)
        self.type = random.choice(['A', 'B', 'C'])
        
        if self.type == 'A':
            self.size = 5.0
            self.rotation_speed = random.uniform(0.5, 1.0)
        elif self.type == 'B':
            self.size = 15.0
            self.rotation_speed = random.uniform(0.1, 0.3)
        elif self.type == 'C':
            self.size = 8.0
            self.rotation_speed = random.uniform(1, 2)

    def move(self, dt):
        self.x -= SCROLL_S * 1.5 * dt
        if self.x < -WORLD_W / 2:
            self.x += WORLD_W + 300.0
            self.y = random.uniform(-100.0, 100.0)
            self.z = random.uniform(-50.0, 50.0)
            self.type = random.choice(['A', 'B', 'C'])
        self.rotation += self.rotation_speed

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        if self.type == 'A':
            glColor3f(0.2, 0.25, 0.15)
            glScalef(2, 2, 2)
            glRotatef(self.rotation, 0.3, 1.0, 0.7)
            glutSolidSphere(6, 20, 20)
        elif self.type == 'B':
            glColor3f(0.25, 0.0, 0.2)
            glScalef(15, 25, 10)
            glRotatef(self.rotation, 0.3, 1.0, 0.7)
            glutSolidTetrahedron()
        elif self.type == 'C':
            glColor3f(0.05, 0.2, 0.2)
            glScalef(7, 7, 7)  # Or adjust as needed
            glRotatef(self.rotation, 0.3, 1.0, 0.7)
            glutSolidIcosahedron()
        glPopMatrix()

class Bullet:
    def __init__(self, x, y, z, angle):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.speed = bullet_speed
        
    def move(self):
        # Fixed bullet movement calculation
        rad = math.radians(-self.angle)
        self.x += self.speed * math.cos(rad)
        self.z += self.speed * math.sin(rad)
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 1, 0)
        glColor3f(1, 0.5, 0)
        glScalef(2, 3, 2)
        glutSolidSphere(1.0, 8, 8)  # Parameters: radius, slices, stack
        glPopMatrix()
        
    def is_offscreen(self):
        return abs(self.x) > WORLD_W/2 or abs(self.y) > WORLD_H/2

def shoot_bullet():
    global bullets, ufo_pos_y, ufo_pos_z, ufo_pos_x,ufo_rotation_angle
    
    # Calculate bullet starting position based on gun angle
    rad = math.radians(-gun_rotation_angle)  # Negative because of coordinate system
    gun_length = 30.0  # Length of the gun barrel
    bullet_x = ufo_pos_x
    bullet_z = ufo_pos_z
    bullet_y = ufo_pos_y  # Same Y as the UFO
    
    bullet = Bullet(bullet_x, bullet_y, bullet_z, ufo_rotation_angle)
    bullets.append(bullet)

def animate_bullet():
    global bullets
    
    # Move each bullet
    for bullet in bullets:
        bullet.move()
    
    # Remove bullets that are off-screen
    bullets[:] = [b for b in bullets if not b.is_offscreen()]

def rand_pos(depth_scale=1.0):
    """Generate a random position in world space"""
    return [
        random.uniform(-WORLD_W / 2, WORLD_W / 2),
        random.uniform(-WORLD_H / 2, WORLD_H / 2),
        random.uniform(-WORLD_D / 4, WORLD_D / 4) * depth_scale,
    ]


def populate_scene():
    """Initialize all game objects"""
    stars[:] = [rand_pos() for _ in range(N_STARS)]
    planets[:] = [[rand_pos(0.6), random.uniform(15.0, 35.0)] for _ in range(N_PLANETS)]
    asteroids[:] = [[rand_pos(), random.uniform(4.0, 9.0)] for _ in range(N_ASTEROIDS)]
    ships[:] = [rand_pos() for _ in range(N_SHIPS)]
    
    spacing = 100.0
    for i in range(N_OBSTACLES):
        obstacles.append(Obstacle(z_offset=i * spacing))


def draw_ufo(pos_x=0, pos_y=0, pos_z=0, scale=1.0):
    """Draw the UFO at the specified position and scale"""
    glPushMatrix()
    glTranslatef(pos_x, pos_y, pos_z)
    glRotatef(ufo_rotation_angle, 0, 1, 0)  # Rotate UFO around Y-axis
    glScalef(scale, scale, scale)

    # UFO body
    glColor3f(0.7, 0.7, 0.7)
    glPushMatrix()
    glScalef(1.0, 0.25, 1.0)
    quadric = gluNewQuadric()
    gluSphere(quadric, 60.0, 32, 32)
    glPopMatrix()

    # Cockpit
    glColor3f(0.2, 0.5, 0.8)
    glPushMatrix()
    glTranslatef(0.0, 15.0, 0.0)
    glScalef(0.5, 0.3, 0.5)
    gluSphere(gluNewQuadric(), 60.0, 32, 16)
    glPopMatrix()

    # Bottom section
    glColor3f(0.4, 0.4, 0.4)
    glPushMatrix()
    glTranslatef(0.0, -10.0, 0.0)
    glScalef(0.7, 0.15, 0.7)
    gluSphere(gluNewQuadric(), 60.0, 32, 16)
    glPopMatrix()
    #gun
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(60, 0, 0.0)
    glRotatef(90, 0, 1, 0)  # Rotate to align with X-axis
    gluCylinder(gluNewQuadric(), 2.0, 1.5, 30.0, 12, 4)  #radius, top radius, height, slices, stacks
    glPopMatrix()
    


    # Legs
    glColor3f(0.3, 0.3, 0.3)
    for i in range(3):
        angle = i * 120
        x = 40 * math.cos(math.radians(angle))
        z = 40 * math.sin(math.radians(angle))
        glPushMatrix()
        glTranslatef(x, -15.0, z)
        glRotatef(60, -z, 0, x)
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 5.0, 5.0, 30.0, 8, 8)
        glPopMatrix()
        glTranslatef(0.0, -30.0, 0.0)
        glColor3f(0.2, 0.2, 0.2)
        glutSolidSphere(8.0, 8, 8)
        glPopMatrix()
    

    glPopMatrix()
    
def health_bar():

    global health,lives,is_first_person
    glPushMatrix()
    glTranslatef(100, 160, 0)
    if lives==3:
        glColor3f(0, 1, 0)
    elif lives==2:
        glColor3f(1, 1, 0)
    elif lives==1:
        glColor3f(1, 0, 0)
    if not is_first_person:
        glBegin(GL_QUADS)
        glVertex2f(-30, 0)
        glVertex2f(health, 0)
        glVertex2f(health, 5)
        glVertex2f(-30, 5)
        glEnd()
    elif is_first_person:
        glRotatef(90, 0, 1, 0)  
        glBegin(GL_QUADS)
        glVertex2f(-30, 0)
        glVertex2f(health, 0)
        glVertex2f(health, 5)
        glVertex2f(-30, 5)
        glEnd()

    glPopMatrix()



def init():
    """Initialize OpenGL settings"""
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_pos = (500.0, 600.0, 800.0, 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.35, 1.0))
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    populate_scene()


def reshape(w, h):
    """Handle window resize"""
    glViewport(0, 0, max(1, w), max(1, h))


def set_camera():
    """Set up the camera view based on current mode"""
    global is_first_person
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if is_first_person:
        # Use a wider field of view for cockpit perspective
        gluPerspective(75.0, WINDOW_W / WINDOW_H, 1.0, 2000.0)
    else:
        gluPerspective(60.0, WINDOW_W / WINDOW_H, 1.0, 2000.0)
        
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if is_first_person:
        # Position camera in the cockpit of the UFO, slightly elevated
        # This will naturally show part of the UFO's front without adding objects
        gluLookAt(-160, ufo_pos_y+20, 0,   # Eye position in cockpit
                  0, ufo_pos_y, 0,           # Looking forward
                  0.0, 1.0, 0.0)             # Up vector
    else:
        # Default third-person view
        gluLookAt(0.0, 0.0, 300.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


def draw_gradient_background():
    """Draw the sky gradient background"""
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1, 0, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glBegin(GL_QUADS)
    glColor3f(*BG_TOP); glVertex2f(0, 1); glVertex2f(1, 1)
    glColor3f(*BG_BOT); glVertex2f(1, 0); glVertex2f(0, 0)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)


def draw_starfield():
    """Draw the stars in the background"""
    glDisable(GL_LIGHTING)
    glPointSize(2.5)
    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)
    for x, y, z in stars:
        glVertex3f(x, y, z)
    glEnd()
    glEnable(GL_LIGHTING)


def draw_planets():
    """Draw the planets"""
    for (x, y, z), r in planets:
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(Planet_colour[0], Planet_colour[1], 1.0)
        glutSolidSphere(r, 50, 50)
        glPopMatrix()


def draw_asteroids():
    """Draw the asteroids"""
    glColor3f(0.55, 0.55, 0.55)
    for (x, y, z), r in asteroids:
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef((x + y) * 3.5 % 360, 1, 1, 0)
        glutSolidSphere(r, 18, 18)
        glPopMatrix()


def draw_ships():
    """Draw the enemy ships"""
    glColor3f(0.8, 0.25, 0.25)
    for x, y, z in ships:
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef((x + z) * 11 % 360, 0, 1, 0)
        glutSolidCube(12)
        glPopMatrix()


def draw_obstacles():
    """Draw all obstacles"""
    for obs in obstacles:
        obs.draw()


def draw_bullets():
    """Draw all active bullets"""
    for bullet in bullets:
        bullet.draw()

def check_collisions():
    global bullets, obstacles, score, lives,ufo_pos_x, ufo_pos_y, ufo_pos_z,health
    ufo_pos=[ufo_pos_x, ufo_pos_y, ufo_pos_z]
    projectile_radius = 2.0
    ufo_radius = 25.0  # Approximate based on your draw scale
    for obs in obstacles[:]:
        # Obstacle position
        obs_pos = [obs.x, obs.y, obs.z]
        obstacle_radius = obs.size

        # --- Bullet vs Obstacle ---
        for bullet in bullets[:]:
            if bullet.is_offscreen():
                continue
            bullet_pos = [bullet.x, bullet.y, bullet.z]
            dist_proj = math.sqrt(sum((a - b)**2 for a, b in zip(bullet_pos, obs_pos)))
            if dist_proj < projectile_radius + obstacle_radius:
                obstacles.remove(obs)
                bullets.remove(bullet)
                score += 1
                print(f"Score: {score}")
                break  # Only one projectile should count per obstacle

        # --- UFO vs Obstacle ---
        dist_ufo = math.sqrt(sum((a - b)**2 for a, b in zip(ufo_pos, obs_pos)))
        if dist_ufo < ufo_radius + obstacle_radius:
            obstacles.remove(obs)
            lives -= 1
            health -= 40
            print(f"UFO Hit! Lives remaining: {lives} Score: {score}")
            if lives <= 0 and health <= 0:
                print("GAME OVER")
                # Optionally trigger end-game logic here
            break  # Only one obstacle hit per frame

        
def scroll_list(lst, pair=False, dt=0.016, speed=SCROLL_S):
    """Scroll objects from right to left"""
    if pair:
        for item in lst:
            item[0][0] -= speed * dt
            if item[0][0] < -WORLD_W / 2:
                item[0][0] += WORLD_W
    else:
        for pos in lst:
            pos[0] -= speed * dt
            if pos[0] < -WORLD_W / 2:
                pos[0] += WORLD_W


def idle():
    """Handle animation and game updates"""
    global last_time, ufo_rotation_angle

    now = time.time()
    if last_time == 0.0:
        last_time = now
    dt = now - last_time
    last_time = now

    # Scroll background elements
    scroll_list(stars, dt=dt, speed=SCROLL_SPEEDS["stars"])
    scroll_list(planets, pair=True, dt=dt, speed=SCROLL_SPEEDS["planets"])
    scroll_list(asteroids, pair=True, dt=dt, speed=SCROLL_SPEEDS["asteroids"])
    scroll_list(ships, dt=dt, speed=SCROLL_SPEEDS["ships"])

    # Move obstacles
    for obs in obstacles:
        obs.move(dt)

    # Move projectiles and remove dead ones
    animate_bullet()
    check_collisions()


    glutPostRedisplay()


def display():
    """Main display function"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_gradient_background()
    set_camera()
    health_bar()
    draw_starfield()
    draw_planets()
    draw_asteroids()
    draw_ships()
    draw_obstacles()


    # Draw all bullets
    draw_bullets()

    # Always draw the UFO - in first-person mode the camera position will
    # naturally make only parts of it visible
    draw_ufo(pos_x=ufo_pos_x, pos_y=ufo_pos_y, pos_z=ufo_pos_z, scale=0.4)
    #draw_gun()
    
    glutSwapBuffers()


def key_pressed(key, x, y):
    """Handle special key presses (arrow keys)"""
    global ufo_pos_y, gun_rotation_angle, ufo_rotation_angle, ufo_rotation_speed
    offset = 10.0
    rotation_speed = 5.0  # Degrees to rotate per key press

    if key == GLUT_KEY_UP:  # Move UFO up
        ufo_pos_y += 5
        ufo_pos_y = min(ufo_pos_y, (WORLD_H-280) / 2 - offset)

    elif key == GLUT_KEY_DOWN:  # Move UFO down
        ufo_pos_y -= 5
        ufo_pos_y = max(ufo_pos_y, (-WORLD_H+295) / 2 + offset)
        
    elif key == GLUT_KEY_RIGHT:  # Rotate gun to the left
        ufo_rotation_angle -= ufo_rotation_speed
        if ufo_rotation_angle <= 360.0:
            ufo_rotation_angle += 360.0
            
    elif key == GLUT_KEY_LEFT:  # Rotate gun to the right
        ufo_rotation_angle += ufo_rotation_speed
        if ufo_rotation_angle >= 360.0:
            ufo_rotation_angle -= 360.0


def keyboard(key, x, y):
    """Handle regular key presses"""
    global is_firing, is_first_person
    
    if key == b' ':
        # Fire weapon
        shoot_bullet()
        is_firing = True
    
    elif key == b'f' or key == b'F': 
        # Toggle first-person view
        is_first_person = not is_first_person
        
    elif key == b'q' or key == b'\x1b':  # ESC or q to quit
        glutLeaveMainLoop()


def main():
    """Main function to initialize and run the game"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutCreateWindow(b"Flappy Space")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(key_pressed)
    glutMainLoop()


if __name__ == "__main__":
    main()