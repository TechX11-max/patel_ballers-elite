# utils.py
# used chat to format the code(files properly)
import math
import pygame
from settings import *
from tilemap import load_level

# defines the rim collision mechanic(hoop tbd)
def rim_collision(ball, rim_center, rim_radius):  # rim collision detection and response
    offset = ball.pos - rim_center
    dist = offset.length()
    min_dist = rim_radius + ball.r - 3

    if dist < min_dist and dist != 0:  # collision detected != 0 to avoid division by zero
        n = offset.normalize()  # normal vector
        overlap = min_dist - dist
        ball.pos += n * overlap
        v_dot = ball.vel.dot(n)
        if v_dot < 0:  # vdot is negative when moving towards the rim
            ball.vel -= (1 + REST) * v_dot * n  # velocity reflection

# draws the hoop function
def draw_hoop(surf, rim_center=None, rim_radius=None):  # surf=surface*
    if rim_center is None:
        rim_center = pygame.Vector2(load_level())  # default rim position
    if rim_radius is None:
        rim_radius = 40  # default radius

    # rim only (backboard removed here to keep only one in main.py)
    rim_rect = pygame.Rect(rim_center.x - rim_radius, rim_center.y - rim_radius, rim_radius * 2, rim_radius * 2)
    start_ang, end_ang = math.radians(210), math.radians(330)
    pygame.draw.arc(surf, HOOP_COLOR, rim_rect, start_ang, end_ang, 6)

    # inner depth arc
    inner_rect = rim_rect.inflate(-8, -8)
    pygame.draw.arc(surf, (180, 180, 180), inner_rect, start_ang, end_ang, 2)

    # small rope detail
    pygame.draw.line(surf, (240, 240, 240),  # light grey rope detail
                     (rim_center.x - rim_radius + 6, rim_center.y + 6),  # start point
                     (rim_center.x - rim_radius + 20, rim_center.y + 30), 1)  # end point

    return rim_center, rim_radius


