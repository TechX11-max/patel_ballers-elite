# sprites.py
import math
import pygame
from settings import *

# ball class( all classes need to be moved to a seperate file asap.)
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, r=BALL_RADIUS):
        super().__init__()
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
        
    def backboard_collision(self, backboard_rect):  #(will convert this code into a different class shortly(incase))
                                                    #if backboard_rect.collidepoint(self.pos.x + self.r, self.pos.y):
                                                    #self.pos.x=backboard_rect.left - self.r
                                                    #self.vel.x= -self.vel.x * REST

            
        
        nearest_x = max(backboard_rect.left, min(self.pos.x, backboard_rect.right)) # clamp x to backboard edges
        nearest_y = max(backboard_rect.top, min(self.pos.y, backboard_rect.bottom)) # clamp y to backboard edges
        nearest_point = pygame.Vector2(nearest_x, nearest_y)

        # Vector from the nearest point to ball center
        offset = self.pos - nearest_point
        dist = offset.length()

        # If ball overlaps the backboard rectangle
        if dist < self.r and dist != 0:
            n = offset.normalize()  # normal vector (direction away from wall)
            overlap = self.r - dist
            self.pos += n * overlap  # push ball out of backboard

            # Reflect velocity along normal
            v_dot = self.vel.dot(n)
            if v_dot < 0:
                self.vel -= (1 + REST) * v_dot * n



