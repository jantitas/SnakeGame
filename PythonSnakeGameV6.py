import pygame
import random
import os
import sys

# Initialize pygame
pygame.init()

# Create a Clock object for controlling frame rate
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the dimensions of the game window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Set the dimensions of the grid
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Set the speed of the snake
SNAKE_SPEED = 0.15

# Set the speed multiplier for the obstacle
OBSTACLE_SPEED_MULTIPLIER = 0.2
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, down, left, right

# Game Pause
STATE_PAUSED = 4

# Set the delay between frames (in milliseconds)
# This will be replaced with FPS
# DELAY = 85
FPS = 60

# Set the font for the score
FONT = pygame.font.SysFont(None, 30)
BIG_FONT = pygame.font.SysFont("Arial", 60)

# Set the maximum number of high scores to keep track of
MAX_HIGH_SCORES = 10

# Set the name of the file to save the high scores to
HIGH_SCORES_FILE = "high_scores.txt"

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Game state constants
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_HIGH_SCORES = 3


# [NEW] Added a function to handle game over
def game_over():
    global state
    state = STATE_GAME_OVER
    save_high_score(player_name, snake.score, HIGH_SCORES_FILE)


# [NEW] Added a function to load high scores from a file
def load_high_scores(filename):
    try:
        with open(filename, "r") as file:
            high_scores = [tuple(line.strip().split(",")) for line in file.readlines()]
            high_scores = [(name, int(score)) for name, score in high_scores]
            high_scores.sort(key=lambda x: x[1], reverse=True)
            return high_scores
    except FileNotFoundError:
        return []


# [NEW] Added a function to save a new high score to a file
def save_high_score(name, score, filename):
    high_scores = load_high_scores(filename)
    high_scores.append((name, score))
    high_scores.sort(key=lambda x: x[1], reverse=True)
    with open(filename, "w") as file:
        for name, score in high_scores[:MAX_HIGH_SCORES]:
            file.write(f"{name},{score}\n")


# [NEW] Added a function to render text
def render_text(text, font, color):
    return font.render(text, True, color)


# Pause draw screen
def draw_paused():
    paused_text = FONT.render("Paused", True, WHITE)
    press_p_text = FONT.render("Press P to resume", True, WHITE)

    window.blit(paused_text, (
        WINDOW_WIDTH // 2 - paused_text.get_width() // 2, WINDOW_HEIGHT // 2 - paused_text.get_height() // 2 - 30))
    window.blit(press_p_text, (
        WINDOW_WIDTH // 2 - press_p_text.get_width() // 2, WINDOW_HEIGHT // 2 - press_p_text.get_height() // 2 + 30))

    pygame.display.update()


# Idejau veikia pakeist pavadinima gal dar
def draw_menu():
    window.fill(BLACK)
    title_text = FONT.render("Snake Game", True, WHITE)
    start_text = FONT.render("1. Start Game", True, WHITE)
    high_scores_text = FONT.render("2. High Scores", True, WHITE)
    quit_text = FONT.render("3. Quit", True, WHITE)

    window.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 3))
    window.blit(start_text, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, WINDOW_HEIGHT // 2))
    window.blit(high_scores_text, (WINDOW_WIDTH // 2 - high_scores_text.get_width() // 2, WINDOW_HEIGHT // 2 + 30))
    window.blit(quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, WINDOW_HEIGHT // 2 + 60))

    pygame.display.update()


# input boxas kad geime nick isivesciau
def input_box(prompt):
    input_string = ""
    window.fill(BLACK)
    prompt_text = FONT.render(prompt, True, WHITE)
    window.blit(prompt_text, (WINDOW_WIDTH // 2 - prompt_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_string
                elif event.key == pygame.K_BACKSPACE:
                    input_string = input_string[:-1]
                else:
                    input_string += event.unicode

        input_text = FONT.render(input_string, True, WHITE)
        window.fill(BLACK)
        window.blit(prompt_text, (WINDOW_WIDTH // 2 - prompt_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
        window.blit(input_text, (WINDOW_WIDTH // 2 - input_text.get_width() // 2, WINDOW_HEIGHT // 2))
        pygame.display.update()
        clock.tick(FPS)


# Naujas fixas
def draw_game_over():
    global high_score

    if snake.score > high_score:
        high_score = snake.score
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))

    window.fill(BLACK)
    game_over_text = BIG_FONT.render("GAME OVER", True, WHITE)
    window.blit(game_over_text, (
        WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
        WINDOW_HEIGHT // 2 - game_over_text.get_height() // 2 - 50))

    score_text = FONT.render(f"Your Score: {snake.score}", True, WHITE)
    window.blit(score_text, (
        WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 - score_text.get_height() // 2 + 50))

    high_score_text = FONT.render(f"High Score: {high_score}", True, WHITE)
    window.blit(high_score_text, (
        WINDOW_WIDTH // 2 - high_score_text.get_width() // 2,
        WINDOW_HEIGHT // 2 - high_score_text.get_height() // 2 + 90))

    press_enter_text = FONT.render("Press ENTER to return to menu", True, WHITE)
    window.blit(press_enter_text, (WINDOW_WIDTH // 2 - press_enter_text.get_width() // 2, WINDOW_HEIGHT - 70))


# Define the Bait class
class Bait:
    def __init__(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
        self.rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

    def draw(self):
        pygame.draw.rect(window, RED, self.rect)


# Define the Snake class
class Snake:
    def __init__(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
        self.dx = SNAKE_SPEED
        self.dy = 0
        self.body = [(self.x, self.y)]
        self.length = 1
        self.score = 0
        self.head_rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0:
            self.x = GRID_WIDTH - 1
        elif self.x > GRID_WIDTH - 1:
            self.x = 0
        if self.y < 0:
            self.y = GRID_HEIGHT - 1
        elif self.y > GRID_HEIGHT - 1:
            self.y = 0
        self.body.insert(0, (self.x, self.y))
        if len(self.body) > self.length:
            self.body.pop()
        self.head_rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

    def draw(self):
        for x, y in self.body:
            pygame.draw.rect(window, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def handle_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.dx = -SNAKE_SPEED
            self.dy = 0
        elif keys[pygame.K_RIGHT]:
            self.dx = SNAKE_SPEED
            self.dy = 0
        elif keys[pygame.K_UP]:
            self.dx = 0
            self.dy = -SNAKE_SPEED
        elif keys[pygame.K_DOWN]:
            self.dx = 0
            self.dy = SNAKE_SPEED

    def check_collision(self):
        if self.body[0] in self.body[1:]:
            return True
        return False

    def eat(self):
        self.score += 10
        self.length += 5


# Define the Obstacle class
class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
                                GRID_SIZE, GRID_SIZE)
        self.direction = random.choice(DIRECTIONS)

    def move(self):
        dx, dy = self.direction
        new_x = self.rect.x + dx * GRID_SIZE * OBSTACLE_SPEED_MULTIPLIER
        new_y = self.rect.y + dy * GRID_SIZE * OBSTACLE_SPEED_MULTIPLIER

        if 0 <= new_x < WINDOW_WIDTH and 0 <= new_y < WINDOW_HEIGHT:
            self.rect.move_ip(dx * GRID_SIZE * OBSTACLE_SPEED_MULTIPLIER, dy * GRID_SIZE * OBSTACLE_SPEED_MULTIPLIER)
        else:
            self.direction = random.choice(DIRECTIONS)
            self.move()

    def draw(self):
        pygame.draw.rect(window, BLUE, self.rect)


# Create the Snake, Bait objects, and a list of Obstacle objects
snake = Snake()
bait = Bait()
obstacles = [Obstacle() for _ in range(3)]  # Create 3 obstacles

# Load the high score from a file
try:
    with open('high_score.txt', 'r') as file:
        high_score = int(file.read())
except FileNotFoundError:
    # If the file does not exist, create it with a default value of 0
    with open('high_score.txt', 'w') as file:
        file.write(str(high_score))

# [NEW] Added a player name variable and a game state variable
player_name = ""
state = STATE_MENU


# HighScore
def draw_high_scores():
    window.fill(BLACK)
    high_scores_title = FONT.render("High Scores", True, WHITE)
    press_enter_text = FONT.render("Press Enter to return to the menu", True, WHITE)

    window.blit(high_scores_title, (WINDOW_WIDTH // 2 - high_scores_title.get_width() // 2, 20))
    high_scores = load_high_scores(HIGH_SCORES_FILE)
    for i, (name, score) in enumerate(high_scores, start=1):
        score_text = FONT.render(f"{i}. {name}: {score}", True, WHITE)
        window.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 40 + 28 * i))

    window.blit(press_enter_text, (WINDOW_WIDTH // 2 - press_enter_text.get_width() // 2, WINDOW_HEIGHT - 70))

    pygame.display.update()
    clock.tick(FPS)


# Run the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input
    keys = pygame.key.get_pressed()

    if state == STATE_MENU:
        # [NEW] Added menu logic
        player_name = ""
        draw_menu()
        if keys[pygame.K_1]:
            state = STATE_PLAYING
            player_name = input_box("Enter your nickname:")
            snake = Snake()
        elif keys[pygame.K_2]:
            state = STATE_HIGH_SCORES
        elif keys[pygame.K_3]:
            running = False

    if state == STATE_PLAYING:
        # Handle key presses
        snake.handle_keys(keys)

        # Pause handle part
        if keys[pygame.K_p]:
            state = STATE_PAUSED

        # Move the snake
        snake.move()

        # Check for collisions with the snake's body
        if snake.check_collision():
            game_over()

        # Check for collisions with the obstacles
        for obstacle in obstacles:
            if snake.head_rect.colliderect(obstacle.rect):
                game_over()

        # Check for collisions with the bait
        if snake.head_rect.colliderect(bait.rect):
            snake.eat()
            bait = Bait()

        # Move the obstacles
        for obstacle in obstacles:
            obstacle.move()

        # Clear the window
        window.fill(BLACK)

        # Draw the snake, the obstacles, the bait, and the score
        snake.draw()
        for obstacle in obstacles:
            obstacle.draw()
        bait.draw()
        score_text = FONT.render(f"Score: {snake.score}", True, WHITE)
        high_score_text = FONT.render(f"High Score: {high_score}", True, WHITE)
        window.blit(score_text, (10, 10))
        window.blit(high_score_text, (WINDOW_WIDTH - 170, 10))

    elif state == STATE_PAUSED:
        draw_paused()
        if keys[pygame.K_p]:
            state = STATE_PLAYING


    elif state == STATE_GAME_OVER:
        # [NEW] Added game over logic
        draw_game_over()
        if keys[pygame.K_RETURN]:
            state = STATE_MENU

    elif state == STATE_HIGH_SCORES:
        # [NEW] Added high scores logic
        draw_high_scores()
        if keys[pygame.K_RETURN]:
            state = STATE_MENU

    # Update the display
    pygame.display.update()

    # Delay to control the speed of the game using the Clock object
    clock.tick(FPS)

# Quit pygame
pygame.quit()