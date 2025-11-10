# main.py
# used chat to format the code(files properly)
import sys
import pygame
from settings import *
from sprites import Ball
from utils import draw_hoop, rim_collision
from tilemap import load_level

pygame.init()  # initialize pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)  # default font

# Main loop
def main():  # main game loop which runs the game
    ball = Ball(140, HEIGHT - BALL_RADIUS - 1)
    dragging = False
    drag_start = pygame.Vector2(0, 0)

    rim_pos = load_level()  # level loading placeholder
    # backboard rectangle for collision (only one backboard)
    backboard_rect = pygame.Rect(rim_pos[0] + 40, rim_pos[1] - 70, 10, 140)

    while True:  # proper game loop
        dt = clock.tick(FPS) / 1000.0  # delta time in seconds

        # Event handling
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
                mouse = pygame.Vector2(e.pos)  # get mouse position on release
                drag_vec = drag_start - mouse  # calculate drag vector
                ball.vel = drag_vec * 6.5  # set ball velocity based on drag vector
                dragging = False  # stop dragging

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:  # reset ball position on spacebar press
                ball.pos = pygame.Vector2(140, HEIGHT - BALL_RADIUS - 1)  # reset position
                ball.vel = pygame.Vector2(0, 0)  # reset velocity

        # Physics
        ball.update(dt)
        rim_center, rim_radius = draw_hoop(screen)
        rim_collision(ball, rim_center, rim_radius)
        ball.backboard_collision(backboard_rect)  # collision with backboard

        # Render
        screen.fill(BACKGROUND)  # fill background
        rim_center, rim_radius = draw_hoop(screen)
        rim_collision(ball, rim_center, rim_radius)
        pygame.draw.rect(screen, (180, 180, 180), backboard_rect)  # draw backboard (visual next to rim)
        ball.draw(screen)  # draw ball

        # Draw drag line
        if dragging:  # if dragging is true draw line
            mouse = pygame.Vector2(pygame.mouse.get_pos())  # get current mouse position
            pygame.draw.line(screen, DRAG_LINE_COLOR, drag_start, mouse, 3)  # draw line from drag_start to current mouse position

        pygame.display.flip()


if __name__ == '__main__':  # entry point
    main()



