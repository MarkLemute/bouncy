import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BALL_RADIUS = 10
BALL_SPEED = 5
SPEED_INCREASE = 1.05  # Ball speeds up a little on every paddle hit

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
ORANGE = (255, 150, 0)
RED = (255, 0, 0)

# FPS
FPS = 60

class BouncyGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Bouncy")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Game state
        self.reset_game()

    def reset_game(self):
        self.paddle = pygame.Rect((WINDOW_WIDTH - PADDLE_WIDTH) // 2, WINDOW_HEIGHT - 40,
                                  PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball_x = WINDOW_WIDTH / 2
        self.ball_y = WINDOW_HEIGHT / 3
        self.ball_dx = random.choice([-1, 1]) * BALL_SPEED
        self.ball_dy = BALL_SPEED
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            # ESC quits too (goes back to the games menu)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False

            # Reset game on SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game_over:
                self.reset_game()

        return True

    def update(self):
        if self.game_over:
            return

        # Move paddle with held arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            self.paddle.x += PADDLE_SPEED
        self.paddle.clamp_ip(self.screen.get_rect())

        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Bounce off walls and ceiling
        if self.ball_x - BALL_RADIUS <= 0 or self.ball_x + BALL_RADIUS >= WINDOW_WIDTH:
            self.ball_dx = -self.ball_dx
            self.ball_x = max(BALL_RADIUS, min(WINDOW_WIDTH - BALL_RADIUS, self.ball_x))
        if self.ball_y - BALL_RADIUS <= 0:
            self.ball_dy = abs(self.ball_dy)

        # Bounce off paddle (only when moving down)
        ball_rect = pygame.Rect(self.ball_x - BALL_RADIUS, self.ball_y - BALL_RADIUS,
                                BALL_RADIUS * 2, BALL_RADIUS * 2)
        if self.ball_dy > 0 and ball_rect.colliderect(self.paddle):
            # Angle depends on where the ball hits the paddle
            offset = (self.ball_x - self.paddle.centerx) / (PADDLE_WIDTH / 2)
            self.ball_dx += offset * 3
            self.ball_dy = -abs(self.ball_dy) * SPEED_INCREASE
            self.score += 1

        # Ball fell below the paddle
        if self.ball_y - BALL_RADIUS > WINDOW_HEIGHT:
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)

        # Draw paddle and ball
        pygame.draw.rect(self.screen, BLUE, self.paddle)
        pygame.draw.circle(self.screen, ORANGE, (int(self.ball_x), int(self.ball_y)), BALL_RADIUS)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press SPACE to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 20))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = BouncyGame()
    game.run()
