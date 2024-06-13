import pygame
import random
import sys

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 10
FPS = 60
WINNING_SCORE = 10

pygame.init()
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

class Paddle:
    COLOR = WHITE
    VEL = 5

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up=True):
        if up:
            self.rect.y -= self.VEL
        else:
            self.rect.y += self.VEL

    def reset(self, y):
        self.rect.y = y

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)

class Ball:
    COLOR = WHITE
    MAX_VEL = 5

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.x_vel = random.choice([-self.MAX_VEL, self.MAX_VEL])
        self.y_vel = random.choice([-self.MAX_VEL, self.MAX_VEL])
    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def bounce(self):
        self.y_vel *= -1

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.x_vel = random.choice([-self.MAX_VEL, self.MAX_VEL])
        self.y_vel = random.choice([-self.MAX_VEL, self.MAX_VEL])

    def draw(self, win):
        pygame.draw.ellipse(win, self.COLOR, self.rect)

def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * 3 // 4 - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 0:
            pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)
    pygame.display.update()
def handle_collision(ball, left_paddle, right_paddle):
    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball.bounce()

    if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
        ball.x_vel *= -1

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.rect.top > 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.rect.bottom < HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.rect.top > 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.rect.bottom < HEIGHT:
        right_paddle.move(up=False)

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

    left_score = 0 
    right_score = 0 

    run = True
    while run:
        clock.tick(FPS)
        draw(win, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.rect.left <= 0:
            right_score += 1
            ball.reset(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

        elif ball.rect.right >= WIDTH:
            left_score += 1
            ball.reset(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

        if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
            win_text = "Left Player Won!" if left_score >= WINNING_SCORE else "Right Player Won!"
            text = SCORE_FONT.render(win_text, 1, WHITE)
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)

            ball.reset(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)
            left_paddle.reset(HEIGHT // 2 - PADDLE_HEIGHT // 2)
            right_paddle.reset(HEIGHT // 2 - PADDLE_HEIGHT // 2)
            left_score = 0
            right_score = 0

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
