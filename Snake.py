import pygame
import random
import heapq  # Import the heapq module for efficient priority queue
from collections import deque

GRID_SIZE = 15
CELL_SIZE = 30
FPS = 60
DELAY = 60

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
clock = pygame.time.Clock()

# Define the Snake class
class Snake:
    def __init__(self):
        # Initialize the snake with length 1, starting position in the middle of the grid, and a random initial direction
        self.length = 1
        self.positions = [((GRID_SIZE // 2), (GRID_SIZE // 2))]
        self.direction = random.choice(["up", "down", "left", "right"])

    def draw(self, surface):
        # Draw the snake on the game surface
        for p in self.positions:
            pygame.draw.rect(surface, (0, 255, 0), (p[0] * CELL_SIZE, p[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move(self, food):
        # Move the snake based on the A* algorithm
        head_x, head_y = self.positions[0]
        food_x, food_y = food.x // CELL_SIZE, food.y // CELL_SIZE

        # Use A* algorithm for pathfinding
        path = self.find_path_to_food(food)
        if path:
            next_position = path[0]
            x, y = next_position
            # Update the direction based on the next position
            if x < head_x:
                self.direction = "left"
            elif x > head_x:
                self.direction = "right"
            elif y < head_y:
                self.direction = "up"
            elif y > head_y:
                self.direction = "down"

        # Calculate the new head position based on the current direction
        x, y = self.positions[0]
        new = self.get_next_position((x, y), self.direction)

        # Handle collisions and choose a different direction if necessary
        if not (0 <= new[0] < GRID_SIZE and 0 <= new[1] < GRID_SIZE) or new in self.positions[1:]:
            directions = ["up", "down", "left", "right"]
            directions.remove(self.direction)
            for direction in directions:
                next_position = self.get_next_position((x, y), direction)
                if 0 <= next_position[0] < GRID_SIZE and 0 <= next_position[1] < GRID_SIZE and next_position not in self.positions:
                    self.direction = direction
                    new = next_position
                    break

        # Check for collisions again after updating the direction
        if not (0 <= new[0] < GRID_SIZE and 0 <= new[1] < GRID_SIZE) or new in self.positions[1:]:
            print("Snake length:", self.length)
            pygame.quit()
            quit()

        # Insert the new head position at the beginning of the snake's positions
        self.positions.insert(0, new)

        # Check if the snake has eaten the food
        if self.positions[0][0] == food_x and self.positions[0][1] == food_y:
            # Increase the length of the snake, and move the food to a random position
            self.length += 1
            food.x = random.randint(0, GRID_SIZE - 1) * CELL_SIZE
            food.y = random.randint(0, GRID_SIZE - 1) * CELL_SIZE
        else:
            # If the snake hasn't eaten the food, remove the last position to maintain the snake's length
            if len(self.positions) > self.length:
                self.positions.pop()

    def find_path_to_food(self, food):
        # Find the path from the snake's head to the food using the A* algorithm
        start = self.positions[0]
        goal = (food.x // CELL_SIZE, food.y // CELL_SIZE)

        # Implement A* algorithm with priority queue
        visited = set()
        heap = [(0, start, [])]

        while heap:
            current_cost, current, path = heapq.heappop(heap)

            if current == goal:
                return path

            if current in visited:
                continue

            visited.add(current)

            for next_direction in ["up", "down", "left", "right"]:
                next_node = self.get_next_position(current, next_direction)

                if not (0 <= next_node[0] < GRID_SIZE and 0 <= next_node[1] < GRID_SIZE) or next_node in visited:
                    continue

                new_path = path + [next_node]
                new_cost = len(new_path) + heuristic(next_node, goal)
                heapq.heappush(heap, (new_cost, next_node, new_path))

        return None

    def get_next_position(self, current, direction):
        # Calculate the next position based on the current position and direction
        x, y = current
        if direction == "up":
            return x, y - 1
        elif direction == "down":
            return x, y + 1
        elif direction == "left":
            return x - 1, y
        elif direction == "right":
            return x + 1, y

# Heuristic function for A* algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Draw the grid on the game surface
def draw_grid(surface):
    for i in range(0, GRID_SIZE):
        for j in range(0, GRID_SIZE):
            pygame.draw.rect(surface, (255, 255, 255), (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Create an instance of the Snake class
snake = Snake()

# Create the initial food position
food = pygame.Rect(random.randint(0, GRID_SIZE - 1) * CELL_SIZE, random.randint(0, GRID_SIZE - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a black background
    screen.fill((0, 0, 0))

    draw_grid(screen)

    snake.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), food)

    snake.move(food)

    pygame.display.flip()

    pygame.time.delay(DELAY)
    clock.tick(FPS)

pygame.quit()