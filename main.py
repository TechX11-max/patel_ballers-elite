# main.py
# used chat to format the code(files properly)
# used chatgpt for some debugging and tuple values
import sys
import pygame
from settings import *
from sprites import Ball
from utils import draw_hoop, rim_collision
from tilemap import load_level

pygame.init()  # initialize pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # sets the width and height 
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)  # default font

# Main loop
def main():  # main game loop which runs the game
    # Two players with different ball colors and positions
    player1 = Ball(140, HEIGHT - BALL_RADIUS - 1)  # ball for p 1 (why do we use -1? to prevent sticking to ground)
    player2 = Ball(300, HEIGHT - BALL_RADIUS - 1)  # ball for p 2 (height - radius -1 to start just above ground)
    player2.color = (0, 0, 139)  # light blue for player 2

    dragging = False
    drag_start = pygame.Vector2(0, 0)  # drag start pos
    current_player = player1  # Player 1 starts

    # Load rim / backboard position
    rim_pos = load_level()
    rim_center = pygame.Vector2(rim_pos)  # get rim position from load_level
    rim_radius = 40  # rim radius
    backboard_rect = pygame.Rect(rim_center.x + rim_radius - 5, rim_center.y - 70, 10, 140)  # backboard rectangle

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # delta time (/1000 to convert ms to seconds)

        # Event Handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Start dragging
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse = pygame.Vector2(e.pos)
                if (mouse - current_player.pos).length() <= current_player.r + 8:  # mouse-current player pos less than radius +8 pixels
                    dragging = True  # makes sure we are dragging
                    drag_start = mouse  # tells us where we start dragging

            # Release shot
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and dragging:
                mouse = pygame.Vector2(e.pos)  # e.pos is mouse position
                drag_vec = mouse - drag_start  # direction from click to release

                if drag_vec.length() > 0:  # only shoot if you actually dragged
                    speed = drag_vec.length() * 6.5  # launch speed
                    max_speed = 1500  # max speed cap
                    current_player.vel = drag_vec.normalize() * min(speed, max_speed)

                dragging = False  # stop dragging

                # Switch players after a shot
                current_player = player2 if current_player == player1 else player1

            # Reset both balls
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                player1.pos = pygame.Vector2(140, HEIGHT - BALL_RADIUS - 1)  # reset position (1 is to not stick to ground)
                player1.vel = pygame.Vector2(0, 0)  # reset velocity
                player2.pos = pygame.Vector2(300, HEIGHT - BALL_RADIUS - 1)  # 300 is x pos for player 2
                player2.vel = pygame.Vector2(0, 0)  # reset velocity for p2

        # Physics
        for ball in [player1, player2]:  # update both balls
            ball.update(dt)  # update method from sprites.py
            rim_collision(ball, rim_center, rim_radius)  # rim collision from utils.py
            ball.backboard_collision(backboard_rect)  # backboard collision method from sprites.py

        # Render
        screen.fill(BACKGROUND)  # clear background
        rim_center, rim_radius = draw_hoop(screen, rim_center, rim_radius)  # draw hoop once (and get updated rim values)
        pygame.draw.rect(screen, (180, 180, 180), backboard_rect)  # draw backboard (light grey color)

        player1.draw(screen)  # draw both players
        player2.draw(screen)  # draw both players

        # Draw drag line for aiming
        if dragging:
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            pygame.draw.line(screen, DRAG_LINE_COLOR, drag_start, mouse, 3)

        # Display current player text
        text = font.render(  # display which player's turn it is
            f"Current Player: {'Orange' if current_player == player1 else 'Blue'}",  # tells which player's turn it is
            True,
            (255, 255, 255)  # white color
        )
        screen.blit(text, (20, 20))  # draw text on screen at position 20,20

        pygame.display.flip()  # update display


if __name__ == '__main__':  # entry point
    main()






