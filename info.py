import pygame
from button import *

SCREEN_WIDTH, SCREEN_HEIGHT = 500,700

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/ARCADECLASSIC.TTF", size)

body = ["Although NYS has very reliable sorting systems,",
        "preventing the mix of non-recyclable items",
        "in recycling collection is the best way to",
        "ensure your trash actually gets recycled.",
        "",
        "Some common items that are mistaken for ",
        "recyclable items include:",
        "   - Receipts",
        "   - Plastic Bags/Wrappers",
        "   - Plastic Pouches",
        "",
        "Generally speaking, only rigid plastics should",
        "be recycled. Flexible, smaller plastic items ",
        "have the potential to clog machinery."
        "",
        "",
        "Recycling guidelines depend on processes set by",
        "local sanitation departments. For specific",
        "instructions, check the guidelines provided by",
        "your county."
        ]

class Info:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.BG = pygame.transform.smoothscale(pygame.image.load("assets/bright-sky.png"), (500, 700))
        self.font = pygame.font.SysFont("monospace", 16, bold=True)

        
        #resize button
        img = pygame.image.load("assets/button.png")
        DFLT_IMG_SZ = (187, 71)

        self.MENU_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(250, 650), text_input="MENU", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
    
    def run(self):
        SCREEN = self.display
        pygame.display.set_caption("Menu")
        
        SCREEN.blit(self.BG, (0, 0))

        offset = 0
        for line in body:
            text_label = self.font.render(line, 1, (0,0,0))
            SCREEN.blit(text_label, (15, 30+offset))
            offset += 30

        MOUSE_POS = pygame.mouse.get_pos()
        
        for button in [self.MENU_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.MENU_BUTTON.checkForInput(MOUSE_POS):
                    print("go to menu")
                    self.gameStateManager.set_state('menu')