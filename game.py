import pygame 
  
pygame.init() 

#FONT
myfont = pygame.font.SysFont("monospace", 18, bold=True)    

#x, y coords for the moveable bin  
bin_x = 100
bin_y = 400

#bin options
bins = ["assets/black-bin.png", "assets/brown-bin.png", "assets/blue-bin.png", "assets/green-bin.png"]

  
# CREATING CANVAS 
canvas = pygame.display.set_mode((500,700)) 
  
# TITLE OF CANVAS 
pygame.display.set_caption("Bin-It-Bit Game") 
  
#load the bin item
bin_sprite = pygame.image.load(bins[0]) 
exit = False
  
while not exit: 
    canvas.fill( (255,255,255) ) #white background
    bin_position = (bin_x, bin_y)

    #controls text and background
    pygame.draw.rect(canvas, (255, 236, 161), pygame.Rect(35, 570, 360, 100))

    black_label = myfont.render("1 = garbage bin (black)", 1, (0,0,0))
    brown_label = myfont.render("2 = composte bin (brown)", 1, (77, 65, 61))
    blue_label = myfont.render("3 = plastic/metal bin (blue)", 1, (27, 23, 127))
    green_label = myfont.render("4 = paper bin (green)", 1, (41, 95, 20))

    canvas.blit(black_label, (50, 580))
    canvas.blit(brown_label, (50, 600))
    canvas.blit(blue_label, (50, 620))
    canvas.blit(green_label, (50, 640))

    #while the keys are pressed, go left/right or switch bins
    keys = pygame.key.get_pressed() 

    if keys[pygame.K_LEFT]:
        if bin_x > 0:
            bin_x -= 0.5
    if keys[pygame.K_RIGHT]:
        if bin_x < (500-122-10):
            bin_x += 0.5

    if keys[pygame.K_1]:
        bin_sprite = pygame.image.load(bins[0]) 
    if keys[pygame.K_2]:
        bin_sprite = pygame.image.load(bins[1]) 
    if keys[pygame.K_3]:
        bin_sprite = pygame.image.load(bins[2]) 
    if keys[pygame.K_4]:
        bin_sprite = pygame.image.load(bins[3]) 


    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True

    canvas.blit(bin_sprite, dest = bin_position) 
    pygame.display.update() 