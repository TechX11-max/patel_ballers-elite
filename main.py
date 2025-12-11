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

def start_screen(): # most proud of
    waiting = True
    while waiting: # start screen loop
        screen.fill((0, 0, 0))  # Black background

        title_text = font.render("BALLERS ELITE", True, (255, 255, 255)) # white title text
        start_text = font.render("Press SPACE", True, (200, 200, 200)) # light grey start text

        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 60)) # center title //2 is to center text-60 to position it higher
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 10)) # center start text +10 to position it lower

        for event in pygame.event.get(): # event loop for start screen
            if event.type == pygame.QUIT: # quit event
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN: # whole thing is if you press scacebar it goes to main game
                if event.key == pygame.K_SPACE:
                    waiting = False # quit waiting loop

        pygame.display.update() # update display 
        clock.tick(60) # 60 fps for start screen

start_screen() # call to start screen function

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

def create_rim_segments(center, radius):
   
    # How long each rim piece is (short enough to leave a wide gap)
    seg_len = radius * 0.1 # makes the rim bigger

    # lrs
    left_p1 = pygame.Vector2(center.x - radius, center.y) # leftmost point of rim
    left_p2 = pygame.Vector2(center.x - radius + seg_len, center.y) # point seg_len to the right of leftmost point

    # rrs
    right_p1 = pygame.Vector2(center.x + radius - seg_len, center.y) # point seg_len to the left of rightmost point
    right_p2 = pygame.Vector2(center.x + radius, center.y) # rightmost point of rim

    return left_p1, left_p2, right_p1, right_p2 # returns the four points defining the rim segments

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
                current_player = player2 if current_player == player1 else player1 # switch players
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE: # reset game when space is pressed(very useful for physics which kinda suck)
                player1.pos = pygame.Vector2(140, HEIGHT - BALL_RADIUS - 1) # reset player 1 position
                player1.vel = pygame.Vector2(0, 0) # reset player 1 velocity
                player2.pos = pygame.Vector2(300, HEIGHT - BALL_RADIUS - 1) #RESET P2 POS
                player2.vel = pygame.Vector2(0, 0) # P2 Velo reset
                ball_state[player1]["entered"] = False # scrore reset
                ball_state[player2]["entered"] = False # score reset
                ball_state[player1]["prev_y"] = player1.pos.y # reset previous y pos
                ball_state[player2]["prev_y"] = player2.pos.y # reset previous y pos
                score_p1 = 0 # scoring system reset
                score_p2 = 0

        for ball in [player1, player2]: # update both balls
            ball.update(dt) # update ball position and velocity
            left_p1, left_p2, right_p1, right_p2 = create_rim_segments(rim_center, rim_radius)
            collide_with_segment(ball, left_p1, left_p2) # rim collision
            collide_with_segment(ball, right_p1, right_p2) # rim collision
            ball.backboard_collision(backboard_rect) # backboard collision

        net_w = rim_radius * 1.7 # net width
        net_h = rim_radius * 1.5  # net height
        net_rect = pygame.Rect(rim_center.x - net_w / 2, rim_center.y, net_w, net_h) # net rectangle /2 to center it on rim - y to position below rim rim_center.y for top of net at rim center

        for ball in [player1, player2]: # this section handles scoring and collision with net
            state = ball_state[ball] # this  gets the state for the current ball( entered flag and previous y pos)
            prev_y = state["prev_y"] # previous y pos
            cur_y = ball.pos.y
            if not state["entered"]:
                if prev_y < rim_center.y and net_rect.collidepoint(ball.pos.x, ball.pos.y): # if ball was above rim and is now inside net rect
                    state["entered"] = True # mark as entered
            if state["entered"]: # if ball has entered net
                if cur_y > rim_center.y + rim_radius * 0.25: # if ball has dropped below a certain point (rim_center.y + rim_radius * 0.25)
                    if ball is player1:
                        score_p1 += 1# increment player 1 score
                    elif ball is player2: # increment player 2 score
                        score_p2 += 1
                    state["entered"] = False
            state["prev_y"] = cur_y

        screen.fill(BACKGROUND) # fill background color
        rim_center, rim_radius = draw_hoop(screen, rim_center, rim_radius)
        pygame.draw.rect(screen, (180, 180, 180), backboard_rect) # draw backboard
        left_p1, left_p2, right_p1, right_p2 = create_rim_segments(rim_center, rim_radius)
        pygame.draw.line(screen, HOOP_COLOR, left_p1, left_p2, 6) # draw rim segments
        pygame.draw.line(screen, HOOP_COLOR, right_p1, right_p2, 6) # draw rim segments
        player1.draw(screen)
        player2.draw(screen)

        if dragging: # creates the shooting line when dragging( visual aid for shooting)
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            pygame.draw.line(screen, DRAG_LINE_COLOR, drag_start, mouse, 3)

        text = font.render(
            f"Current Player: {'Orange' if current_player == player1 else 'Blue'}",
            True,
            (255, 255, 255)
        )
        screen.blit(text, (20, 20))

        score_text = font.render(f"P1: {score_p1}   P2: {score_p2}", True, (255, 255, 255)) # score display(on top of screen)(255,255,255 is white).
        screen.blit(score_text, (20, 44))

        pygame.display.flip()

if __name__ == '__main__':
    main()








