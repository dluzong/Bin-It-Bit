import pygame
import sys

from cutscenes import *
from button import Button

SCREENWIDTH, SCREENHEIGHT = 500,700
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Bin-It-Bit Game")
        self.clock = pygame.time.Clock()
        
        self.gameStateManager = GameStateManager('menu')
        self.menu = Menu(self.screen, self.gameStateManager)
        self.cutscene = Cutscene(self.screen, self.gameStateManager)
        self.index = Index(self.screen, self.gameStateManager)
        
        self.states = {'menu':self.menu, 'cutscene':self.cutscene, 'index':self.index}
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.states[self.gameStateManager.get_state()].run() # all classes MUST have the run function to work
                    
            pygame.display.update()
            self.clock.tick(FPS)

class Cutscene:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        cutscene_manager = CutsceneManager()
        cutscene_manager.add_scene(DialogueScene('It was a dark and stormy night...', 5))
        cutscene_manager.add_scene(DialogueScene('Suddenly, a shot rang out!', 4))
        cutscene_manager.add_scene(DialogueScene('The maid screamed.', 3))
        cutscene_manager.add_scene(DialogueScene('And all was silent...', 5))
        cutscene_manager.start()

class Menu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.BG = pygame.image.load("assets/bright-sky.png")
        # FONT
        self.myfont = pygame.font.Font('fonts/ARCADECLASSIC.TTF', 40)
        
        #resize button
        img = pygame.image.load("assets/button.png")
        DFLT_IMG_SZ = (187, 71)

        self.START_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(125, 500), text_input="START", font=self.myfont, base_color="#80493A", hovering_color="#A77B5B")
        self.INDEX_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(375, 500), text_input="INDEX", font=self.myfont, base_color="#80493A", hovering_color="#A77B5B")
        self.INFO_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(125, 620), text_input="INFO", font=self.myfont, base_color="#80493A", hovering_color="#A77B5B")
        self.QUIT_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(375, 620), text_input="QUIT", font=self.myfont, base_color="#80493A", hovering_color="#A77B5B")
    
    def run(self):
        SCREEN = self.display
        pygame.display.set_caption("Menu")
        
        SCREEN.blit(self.BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = self.myfont.render("BIN IT BIT", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(250, 100))
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [self.START_BUTTON, self.INDEX_BUTTON, self.INFO_BUTTON, self.QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("go to cutscene")
                    self.gameStateManager.set_state('cutscene')
                if self.INDEX_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("go to index state")
                    self.gameStateManager.set_state('index')
                if self.INFO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("go to info")
                if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

class Index:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.BG = pygame.transform.scale(pygame.image.load("assets/index-board.png"), (SCREEN_WIDTH,SCREEN_HEIGHT))

        # FONT
        self.myfont = pygame.font.Font('fonts/ARCADECLASSIC.TTF', 20)

        self.BACK_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/back-arrow.png"), (95,75)), pos=(55, 40), text_input="MENU", font=self.myfont, base_color="#292D34", hovering_color="#4A5059")

    def run(self):
        SCREEN = self.display
        pygame.display.set_caption("Index")

        bottom_rect = pygame.Rect(0, SCREENHEIGHT // 2, SCREENWIDTH, SCREENHEIGHT // 2)
        show_bottom_rect = False

        bottle_img = pygame.transform.scale(pygame.image.load("assets/bottle.png"), (40,75))
        bottle_loc = (180,160)
        bottle_rect = bottle_img.get_rect(center=bottle_loc)
        cereal_img = pygame.transform.scale(pygame.image.load("assets/cereal.png"), (60,75))
        cereal_loc = (320,160)
        cereal_rect = cereal_img.get_rect(center=cereal_loc)
        chips_img = pygame.transform.scale(pygame.image.load("assets/chips.png"), (60,75))
        chips_loc = (180, 300)
        chips_rect = chips_img.get_rect(center=chips_loc)
        apple_img = pygame.transform.scale(pygame.image.load("assets/apple.png"), (60,75))
        apple_loc = (320, 300)
        apple_rect = apple_img.get_rect(center=apple_loc)
        highlight_img = pygame.transform.scale(pygame.image.load("assets/highlight.png"), (80,100))

        def is_button_clicked(button_rect):
            mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
            mouse_clicked = pygame.mouse.get_pressed()[0]  # Check if left mouse button is clicked
            if button_rect.collidepoint(mouse_pos) and mouse_clicked:
                show_bottom_rect = True
                return True
            return False
 
        SCREEN.blit(self.BG, (0, 0))
        SCREEN.blit(bottle_img, bottle_rect)
        SCREEN.blit(cereal_img, cereal_rect)
        SCREEN.blit(chips_img, chips_rect)
        SCREEN.blit(apple_img, apple_rect)

        INDEX_MOUSE_POS = pygame.mouse.get_pos()

        self.BACK_BUTTON.changeColor(INDEX_MOUSE_POS)
        self.BACK_BUTTON.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.BACK_BUTTON.checkForInput(INDEX_MOUSE_POS):
                    print("go to menu state")
                    self.gameStateManager.set_state('menu')
        for rect in [bottle_rect, cereal_rect, chips_rect, apple_rect]:
            if is_button_clicked(rect):
                if show_bottom_rect:
                    # Draw the bottom half rect
                    pygame.draw.rect(SCREEN, (200, 200, 200), bottom_rect)
                
                    # Render text and display it
                    text_surface = self.myfont.render("This is some information!", True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=bottom_rect.center)
                    SCREEN.blit(text_surface, text_rect)
                if rect==bottle_rect:
                    highlight_rect = highlight_img.get_rect(center=bottle_loc)
                    SCREEN.blit(highlight_img, highlight_rect)
                if rect==cereal_rect:
                    highlight_rect = highlight_img.get_rect(center=cereal_loc)
                    SCREEN.blit(highlight_img, highlight_rect)
                if rect==chips_rect:
                    highlight_rect = highlight_img.get_rect(center=chips_loc)
                    SCREEN.blit(highlight_img, highlight_rect)
                if rect==apple_rect:
                    highlight_rect = highlight_img.get_rect(center=apple_loc)
                    SCREEN.blit(highlight_img, highlight_rect)

#CHANGES STATE
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state
    
if __name__ == '__main__':
    game = Game()
    game.run()