import pygame
from pygame import mixer
from random import randint

class Trash:
    def __init__(self, WIN, image, bin_type):
        self.WIN = WIN
        self.image = image
        self.rect = image.get_rect(center=(randint(25, 475), randint(-1000, -100)))
        self.bin_type = bin_type

    def move(self):
        self.rect.y += 2

    def draw(self):
        self.WIN.blit(self.image, self.rect)

class Bin:
    def __init__(self, WIN, image, bin_type, bin_x, bin_y):
        self.WIN = WIN
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
        self.WIN.blit(self.image, self.rect)

class Game:
    def __init__(self, WIN, WIDTH, HEIGHT, gameStateManager):
        # INITIALIZATION
        pygame.init()
        mixer.init()

        # SET TRACK VOLUME
        mixer.music.set_volume(0.25)

        # LOAD SOUNDS
        self.catch_sound = pygame.mixer.Sound("assets/sfx/coin-3.wav")
        self.miss_sound = pygame.mixer.Sound("assets/sfx/bonk-3.wav")

        self.gameStateManager = gameStateManager

        self.WIN = WIN
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.BG = pygame.transform.smoothscale(pygame.image.load("assets/doomsday-opacity.png"), (self.WIDTH, self.HEIGHT))
        self.myfont = pygame.font.SysFont("monospace", 18, bold=True)
        self.bin_x = 250 # x coord for bin
        self.bin_y = 550 # y coord for bin
        self.current_bin_index = 0
        self.bins = [
            Bin(self.WIN, pygame.image.load("assets/black-bin.png"), "black", self.bin_x, self.bin_y),
            Bin(self.WIN, pygame.image.load("assets/brown-bin.png"), "brown", self.bin_x, self.bin_y),
            Bin(self.WIN, pygame.image.load("assets/blue-bin.png"), "blue", self.bin_x, self.bin_y),
            Bin(self.WIN, pygame.image.load("assets/green-bin.png"), "green", self.bin_x, self.bin_y)
        ]

        # OBSTACLES / TRASH
        self.plastic_bottle = pygame.transform.smoothscale(pygame.image.load("assets/bottle.png").convert_alpha(), (40, 50)) # green
        self.cereal_box = pygame.transform.smoothscale(pygame.image.load("assets/cereal.png").convert_alpha(), (40, 50)) # green
        self.apple_core = pygame.transform.smoothscale(pygame.image.load("assets/apple.png").convert_alpha(), (40, 50)) # brown
        self.chip_bag = pygame.transform.smoothscale(pygame.image.load("assets/chips.png").convert_alpha(), (40, 50)) # black
        self.trash = [
            Trash(self.WIN, self.plastic_bottle, 'blue'),
            Trash(self.WIN, self.cereal_box, 'green'),
            Trash(self.WIN, self.apple_core, 'brown'),
            Trash(self.WIN, self.chip_bag, 'black')
        ]

        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 4000) # trigger obstacle event every 4000 ms

        # OBSTACLES IN PLAY
        self.obstacle_list = []

        # SCORE COUNTER
        self.score = 0

        # CLOCK
        self.clock = pygame.time.Clock() # fps

        # RUN BOOLEAN
        self.running = True

    def get_score(self):
        return self.score
    
    # OBSTACLE MOVEMENT FUNCTION
    def obstacle_movement(self, obstacle_list, score, current_bin):
        if obstacle_list:
            obstacles_to_remove = []  # keep track of obstacles to remove
            for obstacle in obstacle_list:
                obstacle.move()
                obstacle.draw()

                # UPDATE SCORE
                # check if the obstacle hits the ground
                if obstacle.rect.y >= self.HEIGHT:
                    pygame.mixer.Sound.play(self.miss_sound)
                    score -= 1
                    obstacles_to_remove.append(obstacle)

                # check if obstacle collides with the corresponding bin
                if obstacle.rect.colliderect(current_bin.rect):
                    if obstacle.bin_type == current_bin.bin_type:
                        pygame.mixer.Sound.play(self.catch_sound)
                        score += 1
                    else:
                        pygame.mixer.Sound.play(self.miss_sound)
                        score -= 1
                    
                    obstacles_to_remove.append(obstacle)

            # Remove obstacles that hit the ground or collided with a bin
            for obstacle in obstacles_to_remove:
                obstacle_list.remove(obstacle)

        return obstacle_list, score

    def draw_bin_key(self):
        #controls text and background
        pygame.draw.rect(self.WIN, (255, 236, 161), pygame.Rect(35, 570, 360, 100))

        black_label = self.myfont.render("1 = garbage bin (black)", 1, (0,0,0))
        brown_label = self.myfont.render("2 = composte bin (brown)", 1, (77, 65, 61))
        blue_label = self.myfont.render("3 = plastic/metal bin (blue)", 1, (27, 23, 127))
        green_label = self.myfont.render("4 = paper bin (green)", 1, (41, 95, 20))

        self.WIN.blit(black_label, (50, 580))
        self.WIN.blit(brown_label, (50, 600))
        self.WIN.blit(blue_label, (50, 620))
        self.WIN.blit(green_label, (50, 640))

    def draw_score(self):
        score_label = self.myfont.render(f"Score: {self.score}", True, 'Black')
        score_rect = score_label.get_rect(center = (250, 20))
        pygame.draw.rect(self.WIN, (255, 236, 161), score_rect, 10)
        self.WIN.blit(score_label, score_rect)

    def run(self):
        # LOADING TRACK
        mixer.music.load("assets/tracks/AWorthyChallenge.wav")
        
        pygame.display.set_caption("Bin-It-Bit Game")
        
        # PLAY TRACK
        mixer.music.play(-1) # -1 means play infinitely

        while self.running:
            # check if game ends
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == self.obstacle_timer:
                    trash_item = self.trash[randint(0, 3)]
                    self.obstacle_list.append(Trash(self.WIN, trash_item.image, trash_item.bin_type))

            # BACKGROUND
            self.WIN.blit(self.BG, (0,0))

            # MOUSE CORD
            # mouse_coords()

            # BIN KEY
            self.draw_bin_key()

            # BIN MOVEMENT

            ## UPDATE BIN COORDS
            keys = pygame.key.get_pressed() 

            if keys[pygame.K_LEFT]:
                if self.bin_x > current_bin.rect.width/2:
                    self.bin_x -= 5
            if keys[pygame.K_RIGHT]:
                if self.bin_x < (self.WIDTH - current_bin.rect.width/2):
                    self.bin_x += 5

            ## SWITCH BINS
            if keys[pygame.K_1]:
                self.current_bin_index = 0
            if keys[pygame.K_2]:
                self.current_bin_index = 1
            if keys[pygame.K_3]:
                self.current_bin_index = 2 
            if keys[pygame.K_4]:
                self.current_bin_index = 3

            current_bin = self.bins[self.current_bin_index]
            current_bin.update_coords(self.bin_x, self.bin_y)
            current_bin.draw()

            # DISPLAY SCORE
            self.draw_score()

            # TRASH MOVEMENT
            self.obstacle_list, self.score = self.obstacle_movement(self.obstacle_list, self.score, current_bin)

            # UPDATE DISPLAY AT 60 FPS
            pygame.display.update()
            self.clock.tick(60)

        mixer.music.stop()
        # QUIT GAME
        pygame.quit()


# def mouse_coords():
#     mouse_pos = pygame.mouse.get_pos()
#     print(mouse_pos)
#     pygame.draw.circle(WIN, 'red', mouse_pos, 10)
