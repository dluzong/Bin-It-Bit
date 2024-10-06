import pygame
import sys
import time

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
        
        self.gameStateManager = GameStateManager('menu') #the app should start at the menu
        self.menu = Menu(self.screen, self.gameStateManager)
        self.cutscene = Cutscene(self.screen, self.gameStateManager)
        
        self.states = {'menu':self.menu, 'cutscene':self.cutscene}
        
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
        SCREEN = self.display
        background_3 = pygame.image.load("assets/doomsday-three-bkg.png")
        background_2 = pygame.image.load("assets/doomsday-two-bkg.png")
        background_1 = pygame.image.load("assets/doomsday-one-bkg.png")
        background_0 = pygame.image.load("assets/doomsday-zero-bkg.png")

        cutscene_manager = CutsceneManager()
        SCREEN.blit(background_3, (0, 0))
        cutscene_manager.add_scene(DialogueScene('It was an ordinary day in Union Square.\nOur protagonist, Jane Doe, is on a\nstroll when she looks up and notices...', 4))
        cutscene_manager.add_scene(DialogueScene('The doomsday clock was finally \ncounting down to...', 3))
        cutscene_manager.add_scene(DialogueScene('...', 2))
        cutscene_manager.add_scene(DialogueScene('...zero??', 2))
        cutscene_manager.add_scene(DialogueScene('The climate change apocalypse \nhas finally begun?!', 3))
        cutscene_manager.add_scene(DialogueScene('As a consequence of not taking \nenough precautions, Jane Doe and \nthe other inhabitants of Earth are \nforced to collect trash unless they \nwant to be buried under it forever!!', 5))
        cutscene_manager.start()

        while self.gameStateManager.get_state() == 'cutscene':
            if cutscene_manager.return_scene_index() == 1:
                SCREEN.blit(background_2, (0, 0))
            elif cutscene_manager.return_scene_index() == 2:
                SCREEN.blit(background_1, (0, 0))
            elif cutscene_manager.return_scene_index() == 3:
                SCREEN.blit(background_0, (0, 0))
            cutscene_manager.update()  # Continuously update the current cutscene
            cutscene_manager.draw(self.display)  # Draw the current cutscene on the screen
            pygame.display.update()  # Refresh display to show updated visuals

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if all scenes are finished and then change state
            if cutscene_manager.active_scene is None:
                self.gameStateManager.set_state('menu')  # CHANGE TO GAMEPLAY !!!!!!


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
                if self.INFO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("go to info")
                if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        
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