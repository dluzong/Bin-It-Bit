import pygame 
  
pygame.init() 

#FONT
myfont = pygame.font.SysFont("monospace", 18, bold=True)    

#x, y coords for the moveable bin  
x = 100
y = 400

#bin options
bins = ["assets/black-bin.png", "assets/brown-bin.png", "assets/blue-bin.png", "assets/green-bin.png"]

  
# CREATING CANVAS 
canvas = pygame.display.set_mode((500,700)) 
  
# TITLE OF CANVAS 
pygame.display.set_caption("Bin-It-Bit Game") 
  
#load the bin item
image = pygame.image.load(bins[0]) 
exit = False
  
while not exit: 
    canvas.fill( (255,255,255) ) #white background
    position = (x,y)

    #controls text and background
    pygame.draw.rect(canvas, (255, 236, 161), pygame.Rect(35, 570, 360, 100))

    black_label = myfont.render("1 = garbage bin (black)", 1, (0,0,0))
    brown_label = myfont.render("2 = composte bin (brown)", 1, (0,0,0))
    blue_label = myfont.render("3 = plastic/metal bin (blue)", 1, (0,0,0))
    green_label = myfont.render("4 = paper bin (green)", 1, (0,0,0))

    canvas.blit(black_label, (50, 580))
    canvas.blit(brown_label, (50, 600))
    canvas.blit(blue_label, (50, 620))
    canvas.blit(green_label, (50, 640))

    #while the keys are pressed, go left/right or switch bins
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT]:
        if x > 0:
            x -= 0.5
    if keys[pygame.K_RIGHT]:
        if x < (500-122-10):
            x += 0.5

    if keys[pygame.K_1]:
        image = pygame.image.load(bins[0]) 
    if keys[pygame.K_2]:
        image = pygame.image.load(bins[1]) 
    if keys[pygame.K_3]:
        image = pygame.image.load(bins[2]) 
    if keys[pygame.K_4]:
        image = pygame.image.load(bins[3]) 


    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True


    canvas.blit(image, dest = position) 
    pygame.display.update() 