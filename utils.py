# utils.py
# used chat to format the code(files properly)
import math
import pygame
from settings import *

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
