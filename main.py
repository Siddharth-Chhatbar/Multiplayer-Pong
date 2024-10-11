import pygame
from network import Network
from game_objects import Paddle, Ball

WIDTH, HEIGHT = 1920, 1080
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 200
WINNING_SCORE = 12


def draw_waiting_screen(screen):
    screen.fill(BLACK)
    waiting_font = pygame.font.SysFont("Ubuntu Regular", 100)
    waiting_text = waiting_font.render("Waiting for another player...", 1, WHITE)
    screen.blit(
        waiting_text,
        (
            WIDTH // 2 - waiting_text.get_width() // 2,
            HEIGHT // 2 - waiting_text.get_height() // 2,
        ),
    )
    pygame.display.update()


def draw_countdown(screen, count):
    screen.fill(BLACK)
    countdown_font = pygame.font.SysFont("Ubuntu Regular", 200)
    countdown_text = countdown_font.render(str(count), 1, WHITE)
    screen.blit(
        countdown_text,
        (
            WIDTH // 2 - countdown_text.get_width() // 2,
            HEIGHT // 2 - countdown_text.get_height() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.wait(1000)  # Pause for 1 second


def draw(screen, paddle1, paddle2, ball, left_score, right_score):
    screen.fill(BLACK)

    # Score
    SCORE_FONT = pygame.font.SysFont("Ubuntu Regular", 150)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    screen.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    screen.blit(
        right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20)
    )

    paddle1.draw(screen)
    paddle2.draw(screen)

    ball.draw(screen)

    # MIDDLE LINE
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, 0, 10, HEIGHT))

    pygame.display.update()


def move_paddle(keys, paddle: Paddle):
    if keys[pygame.K_UP]:
        paddle.move(True)
    if keys[pygame.K_DOWN]:
        paddle.move(False)
    return


def handle_y_velocity(ball: Ball, paddle: Paddle):
    middle_y = paddle.y + paddle.height / 2
    difference_in_y = middle_y - ball.y
    reduction_factor = (paddle.height / 2) / ball.MAX_VELOCITY
    y_velocity = difference_in_y / reduction_factor
    ball.y_velocity = -1 * y_velocity
    return ball, paddle


def collide(ball: Ball, paddle: Paddle):
    if (
        paddle.y <= ball.y <= paddle.y + paddle.height
    ):  # Check if ball's y is within the paddle's height
        if (
            ball.x - ball.radius <= paddle.x + paddle.width and paddle.x < WIDTH // 2
        ):  # Left paddle collision
            ball.x_velocity *= -1
            ball, paddle = handle_y_velocity(ball, paddle)

        elif (
            ball.x + ball.radius >= paddle.x and paddle.x > WIDTH // 2
        ):  # Right paddle collision
            ball.x_velocity *= -1
            ball, paddle = handle_y_velocity(ball, paddle)

    return ball, paddle


def handle_collision(ball: Ball, paddle1: Paddle, paddle2: Paddle):
    if (
        ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0
    ):  # Ball hits top or bottom
        ball.y_velocity *= -1

    # Handle collision for both paddles
    ball, paddle1 = collide(ball, paddle1)  # Check collision with paddle1
    ball, paddle1 = collide(ball, paddle2)  # Check collision with paddle1

    return ball, paddle1, paddle2


def win_screen(screen, win_text):
    WIN_FONT = pygame.font.SysFont("Ubuntu Regular", 200)
    win_text_render = WIN_FONT.render(f"{win_text}", 1, WHITE)
    screen.fill(BLACK)
    screen.blit(
        win_text_render,
        (
            WIDTH // 2 - win_text_render.get_width() // 2,
            HEIGHT // 2 - win_text_render.get_height() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    active = True
    network = Network()
    game_obj = network.get_game_obj()
    score = [0, 0]
    paddle1, ball = None, None
    win = False
    win_text = ""
    if game_obj is not None:
        paddle1, ball, score, win = game_obj
    left_score, right_score = score[0], score[1]
    connected = False

    while active:
        clock.tick(FPS)
        paddle2 = None
        game_obj = network.send((paddle1, ball, [left_score, right_score], win))
        if game_obj is not None:
            try:
                paddle2, _, score, win = game_obj
                left_score, right_score = score[0], score[1]
                if not connected:
                    for i in range(3, 0, -1):
                        draw_countdown(screen, i)
                    draw_countdown(screen, "Start")
                    pygame.time.wait(300)  # Short delay after "Start"
                connected = True
            except:
                print("Error: ", game_obj)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False

        keys = pygame.key.get_pressed()
        if paddle1 is None or paddle2 is None or ball is None:
            continue
        move_paddle(keys, paddle1)

        handle_collision(ball, paddle1, paddle2)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            pygame.time.wait(1000)

        if ball.x > WIDTH:
            left_score += 1
            ball.reset()
            pygame.time.wait(1000)

        draw(screen, paddle1, paddle2, ball, left_score, right_score)

        game_obj = network.send((paddle1, ball, [left_score, right_score], win))
        if game_obj is not None:
            paddle2, ball, score, win = game_obj
            left_score, right_score = score[0], score[1]

        if left_score == WINNING_SCORE:
            win = True
            win_text = "Left Player Wins"
        if right_score == WINNING_SCORE:
            win = True
            win_text = "Right Player Wins"

        if win:
            win_screen(screen, win_text)
            ball.reset()
            paddle1.reset()
            paddle2.reset()
            left_score = 0
            right_score = 0
            win = False

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
