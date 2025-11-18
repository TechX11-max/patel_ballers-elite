# main.py
# used chat to format the code(files properly)
# used chatgpt for some debugging and tuple values
import sys
import pygame
from settings import *
from sprites import Ball
from utils import draw_hoop  # keep draw_hoop for visuals (we'll do rim physics here)
from tilemap import load_level
import math # import math for calculations

pygame.init()  # initialize pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # sets the width and height 
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)  # default font

def collide_with_segment(ball, p1, p2): # updated in utils.py for rim collision( wasn't realistic before( some help from gpt for debug/format effieciently))
    line = p2 - p1 # line vector( p2-p1 gives direction and length of line)
    line_len2 = line.dot(line)
    if line_len2 == 0: # prevent the division by zero( if did divide by 0 my screen would either glitch or crash)
        return
    t = (ball.pos - p1).dot(line) / line_len2 # project ball pos onto line ball.pos- p1 dot line/ line dot line
    t = max(0.0, min(1.0, t)) # clamp t to [0,1] to stay within segment and not extend beyond(fly off screen)
    nearest = p1 + line * t # nearest point on segment to ball( knockoff way of saying "projected point or closest point")
    offset = ball.pos - nearest # vector from nearest point to ball center( a vector is a direction with magnitude)
    dist = offset.length()                  
    if dist < ball.r and dist != 0: # if ball overlaps segment and dist not 0
        n = offset.normalize() # normal vector (direction away from segment)
        overlap = ball.r - dist # overlap amount
        ball.pos += n * overlap # Pushes the ball out of the segment( to prevent sticking to rim)
        v_dot = ball.vel.dot(n) # velocity along normal
        if v_dot < 0:
            ball.vel -= (1 + REST) * v_dot * n

def create_rim_segments(center, radius): # creates left and right rim segments for collision
    left_outer = pygame.Vector2(center.x - radius, center.y) # left outer point
    left_inner = pygame.Vector2(center.x - radius * 0.25, center.y) # left inner point
    right_inner = pygame.Vector2(center.x + radius * 0.25, center.y) # right inner point
    right_outer = pygame.Vector2(center.x + radius, center.y) # right outer point
    return left_outer, left_inner, right_inner, right_outer # return the four points. This is meant to return the values where the rim hits the ball

def main():
    player1 = Ball(140, HEIGHT - BALL_RADIUS - 1)  # ball for p 1 (why do we use -1? to prevent sticking to ground)
    player2 = Ball(300, HEIGHT - BALL_RADIUS - 1)  # ball for p 2 (height - radius -1 to start just above ground)
    player2.color = (0, 0, 139)  # light blue for player 2

    dragging = False
    drag_start = pygame.Vector2(0, 0)  # drag start pos
    current_player = player1  # Player 1 starts

    rim_pos = load_level()
    rim_center = pygame.Vector2(rim_pos)  # get rim position from load_level
    rim_radius = 40  # rim radius
    backboard_rect = pygame.Rect(rim_center.x + rim_radius - 5, rim_center.y - 70, 10, 140)  # backboard rectangle

    score_p1 = 0
    score_p2 = 0

    ball_state = {
        player1: {"entered": False, "prev_y": player1.pos.y},
        player2: {"entered": False, "prev_y": player2.pos.y},
    }

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # delta time (/1000 to convert ms to seconds)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse = pygame.Vector2(e.pos)
                if (mouse - current_player.pos).length() <= current_player.r + 8:  # mouse-current player pos less than radius +8 pixels
                    dragging = True  # makes sure we are dragging
                    drag_start = mouse  # tells us where we start dragging
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and dragging:
                mouse = pygame.Vector2(e.pos)  # e.pos is mouse position
                drag_vec = mouse - drag_start  # direction from click to release
                if drag_vec.length() > 0:  # only shoot if you actually dragged
                    speed = drag_vec.length() * 6.5  # launch speed
                    max_speed = 1500  # max speed cap
                    current_player.vel = drag_vec.normalize() * min(speed, max_speed)
                dragging = False  # stop dragging
                current_player = player2 if current_player == player1 else player1
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                player1.pos = pygame.Vector2(140, HEIGHT - BALL_RADIUS - 1)
                player1.vel = pygame.Vector2(0, 0)
                player2.pos = pygame.Vector2(300, HEIGHT - BALL_RADIUS - 1)
                player2.vel = pygame.Vector2(0, 0)
                ball_state[player1]["entered"] = False
                ball_state[player2]["entered"] = False
                ball_state[player1]["prev_y"] = player1.pos.y
                ball_state[player2]["prev_y"] = player2.pos.y
                score_p1 = 0
                score_p2 = 0

        for ball in [player1, player2]:
            ball.update(dt)
            left_p1, left_p2, right_p1, right_p2 = create_rim_segments(rim_center, rim_radius)
            collide_with_segment(ball, left_p1, left_p2)
            collide_with_segment(ball, right_p1, right_p2)
            ball.backboard_collision(backboard_rect)

        net_w = rim_radius * 1.0
        net_h = rim_radius * 1.5
        net_rect = pygame.Rect(rim_center.x - net_w / 2, rim_center.y, net_w, net_h)

        for ball in [player1, player2]:
            state = ball_state[ball]
            prev_y = state["prev_y"]
            cur_y = ball.pos.y
            if not state["entered"]:
                if prev_y < rim_center.y and net_rect.collidepoint(ball.pos.x, ball.pos.y):
                    state["entered"] = True
            if state["entered"]:
                if cur_y > rim_center.y + rim_radius * 0.5:
                    if ball is player1:
                        score_p1 += 1
                    elif ball is player2:
                        score_p2 += 1
                    state["entered"] = False
            state["prev_y"] = cur_y

        screen.fill(BACKGROUND)
        rim_center, rim_radius = draw_hoop(screen, rim_center, rim_radius)
        pygame.draw.rect(screen, (180, 180, 180), backboard_rect)
        left_p1, left_p2, right_p1, right_p2 = create_rim_segments(rim_center, rim_radius)
        pygame.draw.line(screen, HOOP_COLOR, left_p1, left_p2, 6)
        pygame.draw.line(screen, HOOP_COLOR, right_p1, right_p2, 6)
        player1.draw(screen)
        player2.draw(screen)

        if dragging:
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            pygame.draw.line(screen, DRAG_LINE_COLOR, drag_start, mouse, 3)

        text = font.render(
            f"Current Player: {'Orange' if current_player == player1 else 'Blue'}",
            True,
            (255, 255, 255)
        )
        screen.blit(text, (20, 20))

        score_text = font.render(f"P1: {score_p1}   P2: {score_p2}", True, (255, 255, 255))
        screen.blit(score_text, (20, 44))

        pygame.display.flip()

if __name__ == '__main__':
    main()








