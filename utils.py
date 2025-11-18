# utils.py
# used chat to format the code(files properly), used to make rim a bit more realistic
import math
import pygame
from settings import *

# draws the hoop function (visual only)
def draw_hoop(surf, center=None, rim_radius=None):  # surf=surface*
    if center is None:
        center = pygame.Vector2(WIDTH - 200, HEIGHT // 3)  # hoop position
    if rim_radius is None:
        rim_radius = 40  # rim radius

    # rim only (backboard removed here to keep only one in main.py)
    rim_rect = pygame.Rect(center.x - rim_radius, center.y - rim_radius, rim_radius * 2, rim_radius * 2)
    start_ang, end_ang = math.radians(210), math.radians(330)
    pygame.draw.arc(surf, HOOP_COLOR, rim_rect, start_ang, end_ang, 6)

    # inner depth arc
    inner_rect = rim_rect.inflate(-8, -8) # slightly smaller rect for inner arc(more realistic for wk # 5 sub)
    pygame.draw.arc(surf, (180, 180, 180), inner_rect, start_ang, end_ang, 2) # lighter grey inner arc

    # small rope detail
    pygame.draw.line(surf, (240, 240, 240), # light grey rope detail( a rope detail is added to make it look more realistic)
                     (center.x - rim_radius + 6, center.y + 6), # starting point of rope detail +6 to position it better on rim
                     (center.x - rim_radius + 20, center.y + 30), 1) # end point of rope detail # you subtract center.x-rim radius to position it on left side of rim

    return center, rim_radius



