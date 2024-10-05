import pygame
from random import randint

class Trash:
    def __init__(self, image, bin_type):
        self.image = image
        self.rect = image.get_rect(center=(randint(25, 475), randint(-1000, -100)))
        self.bin_type = bin_type

    def move(self):
        self.rect.y += 2

    def draw(self):
        WIN.blit(self.image, self.rect)

class Bin:
    def __init__(self, image, bin_type, bin_x, bin_y):
        self.bin_x = bin_x
        self.bin_y = bin_y
        self.image = image
        self.rect = self.image.get_rect(midbottom = (self.bin_x, self.bin_y))
        self.bin_type = bin_type

    def update_coords(self, new_x, new_y):
        self.bin_x = new_x
        self.bin_y = new_y
        self.rect = self.image.get_rect(midbottom = (self.bin_x, self.bin_y))

    def draw(self):
        WIN.blit(self.image, self.rect)


# OBSTACLE MOVEMENT FUNCTION
def obstacle_movement(obstacle_list, score):
    if obstacle_list:
        obstacles_to_remove = []  # Keep track of obstacles to remove
        for obstacle in obstacle_list:
            obstacle.move()
            obstacle.draw()

            # Check if the obstacle hits the ground (i.e., obstacle goes beyond screen height)
            if obstacle.rect.y >= HEIGHT:
                score -= 1  # Deduct one point
                obstacles_to_remove.append(obstacle)  # Mark obstacle for removal

            # Check if obstacle collides with the corresponding bin
            # Write code here...

        # Remove obstacles that hit the ground or collided with a bin
        for obstacle in obstacles_to_remove:
            obstacle_list.remove(obstacle)

    return obstacle_list, score

def draw_bin_key():
    #controls text and background
    pygame.draw.rect(WIN, (255, 236, 161), pygame.Rect(35, 570, 360, 100))

    black_label = myfont.render("1 = garbage bin (black)", 1, (0,0,0))
    brown_label = myfont.render("2 = composte bin (brown)", 1, (77, 65, 61))
    blue_label = myfont.render("3 = plastic/metal bin (blue)", 1, (27, 23, 127))
    green_label = myfont.render("4 = paper bin (green)", 1, (41, 95, 20))

    WIN.blit(black_label, (50, 580))
    WIN.blit(brown_label, (50, 600))
    WIN.blit(blue_label, (50, 620))
    WIN.blit(green_label, (50, 640))

def draw_score():
    score_label = myfont.render(f"Score: {score}", True, 'Black')
    score_rect = score_label.get_rect(center = (250, 20))
    pygame.draw.rect(WIN, (255, 236, 161), score_rect, 10)
    WIN.blit(score_label, score_rect)

def mouse_coords():
    mouse_pos = pygame.mouse.get_pos()
    print(mouse_pos)
    pygame.draw.circle(WIN, 'red', mouse_pos, 10)

pygame.init() 

# FONT
myfont = pygame.font.SysFont("monospace", 18, bold=True)

# WINDOW
WIDTH = 500
HEIGHT = 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bin-It-Bit Game") 

# PLAYER / BINS 
bin_x = 250 # x coord for bin
bin_y = 550 # y coord for bin

bins = [
    Bin(pygame.image.load("assets/black-bin.png"), "black", bin_x, bin_y),
    Bin(pygame.image.load("assets/brown-bin.png"), "brown", bin_x, bin_y),
    Bin(pygame.image.load("assets/blue-bin.png"), "blue", bin_x, bin_y),
    Bin(pygame.image.load("assets/green-bin.png"), "green", bin_x, bin_y)
]
current_bin_index = 0

# OBSTACLES / TRASH
plastic_bottle = pygame.transform.smoothscale(pygame.image.load("assets/bottle.png").convert_alpha(), (50, 50)) # green
cereal_box = pygame.transform.smoothscale(pygame.image.load("assets/cereal.png").convert_alpha(), (50, 50)) # green
apple_core = pygame.transform.smoothscale(pygame.image.load("assets/apple.png").convert_alpha(), (50, 50)) # brown
chip_bag = pygame.transform.smoothscale(pygame.image.load("assets/chips.png").convert_alpha(), (50, 50)) # black

trash = [
    Trash(plastic_bottle, 'blue'),
    Trash(cereal_box, 'green'),
    Trash(apple_core, 'brown'),
    Trash(chip_bag, 'black')
]

obstacle_list = []

# SCORE COUNTER
score = 0

# CLOCK
clock = pygame.time.Clock() # fps

# RUN BOOLEAN
run = True

# MAIN GAME BOOLEAN -- FOR NAVIGATION TO END GAME SCREEN
game_active = True

# TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 4000) # trigger obstacle event every 4000 ms
# EMILYYYYYYY ^^^^^^^^^

# GAME LOOP
while run:
    # check if game ends
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == obstacle_timer and game_active:
            trash_item = trash[randint(0, 3)]
            obstacle_list.append(Trash(trash_item.image, trash_item.bin_type))
    
    # BACKGROUND
    WIN.fill('white')

    # BIN KEY
    draw_bin_key()

    # BIN MOVEMENT

    # while the keys are pressed, go left/right or switch bins
    keys = pygame.key.get_pressed() 

    if keys[pygame.K_LEFT]:
        if bin_x > current_bin.rect.width/2:
            bin_x -= 5
    if keys[pygame.K_RIGHT]:
        if bin_x < (WIDTH - current_bin.rect.width/2):
            bin_x += 5

    # DRAW BIN
    if keys[pygame.K_1]:
        current_bin_index = 0
    if keys[pygame.K_2]:
        current_bin_index = 1
    if keys[pygame.K_3]:
        current_bin_index = 2 
    if keys[pygame.K_4]:
        current_bin_index = 3
    
    current_bin = bins[current_bin_index]
    current_bin.update_coords(bin_x, bin_y)
    current_bin.draw()
    pygame.draw.rect(WIN, (255, 0, 0), current_bin, 2 )

    # MOUSE CORD
    mouse_coords()

    # DISPLAY SCORE
    draw_score()

    # TRASH MOVEMENT
    obstacle_list, score = obstacle_movement(obstacle_list, score)

    # UPDATE DISPLAY AT 60 FPS
    pygame.display.update()
    clock.tick(60)

# QUIT GAME
pygame.quit()