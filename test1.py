import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BLOCK_SIZE = 60
WALL_COLOR = (128, 128, 128)
EXIT_COLOR = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Escape the Grid")

player_sprite = pygame.image.load('Yannis Walking.png')
player_sprite = pygame.transform.scale(player_sprite, (BLOCK_SIZE, int(1.5 * BLOCK_SIZE)))  # Stretch upwards

wall_image = pygame.image.load('Grass block2.png')
wall_image = pygame.transform.scale(wall_image, (BLOCK_SIZE, BLOCK_SIZE))

background_image = pygame.image.load('Backround.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

grid_size_x = 8
grid_size_y = 6
grid = [['' for _ in range(grid_size_x)] for _ in range(grid_size_y)]

player_position = [grid_size_y - 1, grid_size_x - 1]
end_position = [0, 0]

movement_speed = 1

dragging_block = None
drag_offset_x = 0
drag_offset_y = 0

level = 1

def generate_walls(level):
    global grid
    grid = [['' for _ in range(grid_size_x)] for _ in range(grid_size_y)]
    
    wall_chance = 0.4 + (level * 0.1)
    
    for row in range(grid_size_y):
        for col in range(grid_size_x):
            if (row, col) != tuple(player_position) and (row, col) != tuple(end_position):
                if random.random() < wall_chance:
                    wall_size = random.choice([(1, 1), (2, 1), (1, 2)])
                    
                    if row + wall_size[0] <= grid_size_y and col + wall_size[1] <= grid_size_x:
                        collision = False
                        for r in range(wall_size[0]):
                            for c in range(wall_size[1]):
                                if grid[row + r][col + c] != '' or (row + r, col + c) == tuple(player_position):
                                    collision = True
                                    break
                            if collision:
                                break
                        
                        if not collision:
                            for r in range(wall_size[0]):
                                for c in range(wall_size[1]):
                                    grid[row + r][col + c] = 'wall'

def draw_grid():
    grid_top_left_x = (SCREEN_WIDTH - (grid_size_x * BLOCK_SIZE)) // 2
    grid_top_left_y = (SCREEN_HEIGHT - (grid_size_y * BLOCK_SIZE)) // 2
    
    for row in range(grid_size_y):
        for col in range(grid_size_x):
            rect = pygame.Rect(grid_top_left_x + col * BLOCK_SIZE, grid_top_left_y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if (row, col) == tuple(end_position):
                pygame.draw.rect(screen, EXIT_COLOR, rect)
            elif grid[row][col] == 'wall':
                screen.blit(wall_image, (grid_top_left_x + col * BLOCK_SIZE, grid_top_left_y + row * BLOCK_SIZE))

def draw_player():
    grid_top_left_x = (SCREEN_WIDTH - (grid_size_x * BLOCK_SIZE)) // 2
    grid_top_left_y = (SCREEN_HEIGHT - (grid_size_y * BLOCK_SIZE)) // 2
    
    player_rect = pygame.Rect(
        grid_top_left_x + player_position[1] * BLOCK_SIZE,
        grid_top_left_y + player_position[0] * BLOCK_SIZE + (BLOCK_SIZE - int(1.5 * BLOCK_SIZE)) // 2,  # Center vertically
        BLOCK_SIZE,
        int(1.5 * BLOCK_SIZE)  # Stretched height
    )
    
    screen.blit(player_sprite, player_rect)

def move_player():
    global player_position

    keys = pygame.key.get_pressed()

    new_x = player_position[1]
    new_y = player_position[0]

    if keys[pygame.K_UP] and new_y > 0 and grid[new_y - 1][new_x] != 'wall':
        new_y -= 1

    if keys[pygame.K_DOWN] and new_y < grid_size_y - 1 and grid[new_y + 1][new_x] != 'wall':
        new_y += 1

    if keys[pygame.K_LEFT] and new_x > 0 and grid[new_y][new_x - 1] != 'wall':
        new_x -= 1

    if keys[pygame.K_RIGHT] and new_x < grid_size_x - 1 and grid[new_y][new_x + 1] != 'wall':
        new_x += 1

    player_position = [new_y, new_x]

def handle_dragging(mouse_x, mouse_y):
    global dragging_block, drag_offset_x, drag_offset_y
    
    if dragging_block:
        new_x = (mouse_x - drag_offset_x) // BLOCK_SIZE
        new_y = (mouse_y - drag_offset_y) // BLOCK_SIZE
        
        if grid[new_y][new_x] == '':
            grid[dragging_block[0]][dragging_block[1]] = ''
            grid[new_y][new_x] = 'wall'
            dragging_block = (new_y, new_x)

def show_game_over(level):
    font = pygame.font.SysFont(None, 48)
    
    if level == 1:
        game_over_text = font.render("Congratulations! You've beaten the first level.", True, (255, 255, 255))
        next_level_text = font.render("Now onto the next level!", True, (255, 255, 255))
    else:
        game_over_text = font.render("Congratulations! You've beaten the game!", True, (255, 255, 255))
        next_level_text = font.render("", True, (255, 255, 255))
    
    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(next_level_text, (SCREEN_WIDTH // 2 - next_level_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.time.wait(1000)

def game_loop():
    global player_position, dragging_block, drag_offset_x, drag_offset_y, level, end_position
    running = True
    
    pygame.key.set_repeat(200, 100)
    
    generate_walls(level)
    
    end_position = [0, 0]

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        draw_grid()
        draw_player()
        move_player()
        
        if player_position == end_position:
            show_game_over(level)
            level += 1
            player_position = [grid_size_y - 1, grid_size_x - 1]
            end_position = [0, 0]
            generate_walls(level)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x = (mouse_x - (SCREEN_WIDTH - (grid_size_x * BLOCK_SIZE)) // 2) // BLOCK_SIZE
                grid_y = (mouse_y - (SCREEN_HEIGHT - (grid_size_y * BLOCK_SIZE)) // 2) // BLOCK_SIZE
                
                if grid[grid_y][grid_x] == 'wall':
                    dragging_block = (grid_y, grid_x)
                    drag_offset_x = mouse_x - grid_x * BLOCK_SIZE
                    drag_offset_y = mouse_y - grid_y * BLOCK_SIZE
            
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_block = None
            
            elif event.type == pygame.MOUSEMOTION:
                if dragging_block:
                    handle_dragging(event.pos[0], event.pos[1])

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    game_loop()
    pygame.quit()
