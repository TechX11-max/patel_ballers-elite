import sys
import math
import pygame

# settings.py (tbd into a new file)
WIDTH, HEIGHT = 900, 600
FPS = 60 # frames
GRAVITY = 1500 # pixels per second squared
REST = 0.65  # bounce energy
GROUND_FRICTION = 0.995
AIR_DRAG = 0.999
MIN_BOUNCE_VEL = 60

BALL_RADIUS = 14 # defining balls features with tuple values
BALL_COLOR = (244, 127, 36)
BACKGROUND = (30, 30, 30)
HOOP_COLOR = (200, 200, 200)
DRAG_LINE_COLOR = (100, 220, 255)

pygame.init() # initialize pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20) # default font



class Ball: # ball class( all classes need to be moved to a seperate file asap.)
    def __init__(self, x, y, r=BALL_RADIUS):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.r = r
        self.color = BALL_COLOR
        self.on_ground = False

    def apply_gravity(self, dt): # gravity application method(dt =delta time which is time between frames)
        self.vel.y += GRAVITY * dt

    def update(self, dt): # ball update method which updates ball position and velocity
        self.apply_gravity(dt)
        self.vel *= AIR_DRAG
        self.pos += self.vel * dt

        # ground collision
        if self.pos.y + self.r > HEIGHT:
            self.pos.y = HEIGHT - self.r

            if abs(self.vel.y) > MIN_BOUNCE_VEL: # bounce check(physics implementation)
                self.vel.y = -self.vel.y * REST
            else: # stop bouncing
                self.vel.y = 0
                self.on_ground = True

            self.vel.x *= GROUND_FRICTION
            if abs(self.vel.x) < 8:
                self.vel.x = 0
        else: # not on ground
            self.on_ground = False # reset on_ground flag

        # wall collisions
        if self.pos.x - self.r < 0: # left wall
            self.pos.x = self.r # left wall collision
            self.vel.x = -self.vel.x * REST # left wall
        elif self.pos.x + self.r > WIDTH: # right wall
            self.pos.x = WIDTH - self.r
            self.vel.x = -self.vel.x * REST

    def draw(self, surf): # ball drawing method
        pygame.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), self.r) # main ball
        # seam details
        pygame.draw.arc(surf, (220, 100, 20), #tuple values which define the color of the seam
                        (self.pos.x - self.r, self.pos.y - self.r, self.r * 2, self.r * 2),
                        math.radians(30), math.radians(150), 2) # first arc
        pygame.draw.arc(surf, (220, 100, 20), # second arc
                        (self.pos.x - self.r, self.pos.y - self.r // 2, self.r * 2, self.r), # seam position
                        math.radians(210), math.radians(330), 2) # second arc


# defines the rim collision mechanic(hoop tbd)
def rim_collision(ball, rim_center, rim_radius): # rim collision detection and response
    offset = ball.pos - rim_center
    dist = offset.length()
    min_dist = rim_radius + ball.r - 3

    if dist < min_dist and dist != 0: # collision detected != 0 to avoid division by zero which can crash the program
        n = offset.normalize() # normal vector
        overlap = min_dist - dist
        ball.pos += n * overlap
        v_dot = ball.vel.dot(n)
        if v_dot < 0: # vdot is negative when moving towards the rim( defined earlier as rim collision detection and response)
            ball.vel -= (1 + REST) * v_dot * n # velocity reflection

# draws the hoop function 
def draw_hoop(surf): # surf=surface*
    center = pygame.Vector2(WIDTH - 200, HEIGHT // 3) # hoop position
    rim_radius = 40 # rim radius

    # backboard
    backboard = pygame.Rect(center.x + rim_radius - 5, center.y - 70, 10, 140) # backboard dimensions
    pygame.draw.rect(surf, HOOP_COLOR, backboard) # draw backboard

    # rim
    rim_rect = pygame.Rect(center.x - rim_radius, center.y - rim_radius, rim_radius * 2, rim_radius * 2) # rim rectangle
    start_ang, end_ang = math.radians(210), math.radians(330) # rim arc angles
    pygame.draw.arc(surf, HOOP_COLOR, rim_rect, start_ang, end_ang, 6) # draw rim arc

    # inner depth arc
    inner_rect = rim_rect.inflate(-8, -8)
    pygame.draw.arc(surf, (180, 180, 180), inner_rect, start_ang, end_ang, 2)

    # small rope detail which adds realism to the game/hoop
    pygame.draw.line(surf, (240, 240, 240),
                     (center.x - rim_radius + 6, center.y + 6), # +6 and 1 to adjust position
                     (center.x - rim_radius + 20, center.y + 30), 1)

    return center, rim_radius


#Main loop
def main(): # main game loop which runs the game
    ball = Ball(140, HEIGHT - BALL_RADIUS - 1)
    dragging = False
    drag_start = pygame.Vector2(0, 0)

    while True:
        dt = clock.tick(FPS) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse = pygame.Vector2(e.pos)
                if (mouse - ball.pos).length() <= ball.r + 8:
                    dragging = True
                    drag_start = mouse

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and dragging:
                mouse = pygame.Vector2(e.pos) # get mouse position on release
                drag_vec = drag_start - mouse # calculate drag vector
                ball.vel = drag_vec * 6.5 # set ball velocity based on drag vector
                dragging = False # stop dragging

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE: # reset ball position on spacebar press
                ball.pos = pygame.Vector2(140, HEIGHT - BALL_RADIUS - 1) # reset position
                ball.vel = pygame.Vector2(0, 0) # reset velocity

        # physics
        ball.update(dt)
        rim_center, rim_radius = draw_hoop(screen)
        rim_collision(ball, rim_center, rim_radius)

        # render
        screen.fill(BACKGROUND) # fill background
        rim_center, rim_radius = draw_hoop(screen)
        rim_collision(ball, rim_center, rim_radius)
        ball.draw(screen)

        # draw drag line
        if dragging: # if dragging is true draw line
            mouse = pygame.Vector2(pygame.mouse.get_pos()) # get current mouse position
            pygame.draw.line(screen, DRAG_LINE_COLOR, drag_start, mouse, 3) # draw line from drag_start to current mouse position

        pygame.display.flip()


if __name__ == '__main__': # entry point
    main()

