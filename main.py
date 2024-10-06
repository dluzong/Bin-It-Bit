import pygame
import sys

from cutscenes import *
from button import Button

from game import Game

SCREENWIDTH, SCREENHEIGHT = 500,700
FPS = 60

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/ARCADECLASSIC.TTF", size)

class Manager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Bin-It-Bit Game")
        self.clock = pygame.time.Clock()
        
        self.gameStateManager = GameStateManager('menu')
        self.menu = Menu(self.screen, self.gameStateManager)
        self.cutscene = Cutscene(self.screen, self.gameStateManager)
        self.game = Game(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.gameStateManager)
        self.ending = Ending(self.screen, self.gameStateManager)
        self.gameOver = GameOver(self.screen, self.gameStateManager)
        
        self.states = {'menu':self.menu, 'cutscene':self.cutscene, 'game':self.game, 'ending':self.ending, 'gameOver':self.gameOver}
        
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
        self.BG = pygame.transform.smoothscale(pygame.image.load("assets/bright-sky.png"), (500, 700))
        
        #resize button
        img = pygame.image.load("assets/button.png")
        DFLT_IMG_SZ = (187, 71)

        self.START_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(125, 500), text_input="START", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
        self.INDEX_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(375, 500), text_input="INDEX", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
        self.INFO_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(125, 620), text_input="INFO", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
        self.QUIT_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(375, 620), text_input="QUIT", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
    
    def run(self):
        SCREEN = self.display
        pygame.display.set_caption("Menu")
        
        SCREEN.blit(self.BG, (0, 0))

        logo = pygame.image.load("assets/game-logo.png")

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = pygame.transform.scale(logo, (500,500))
        MENU_RECT = MENU_TEXT.get_rect(center=(255, 250))
        
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

class Ending:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.BG = pygame.transform.smoothscale(pygame.image.load("assets/bright-sky.png"), (500, 700))
        
        #resize button
        img = pygame.image.load("assets/button.png")
        DFLT_IMG_SZ = (187, 71)

        self.PLAY_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(125, 550), text_input="TRY AGAIN", font=get_font(30), base_color="#80493A", hovering_color="#A77B5B")
        self.MENU_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(375, 550), text_input="MENU", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
    
    def run(self):
        SCREEN = self.display
        pygame.display.set_caption("End of Game")

        SCREEN.blit(self.BG, (0, 0))

        icon = pygame.image.load("assets/green-bin.png")

        #TEMPORARY
        score = 0

        ENDING_MOUSE_POS = pygame.mouse.get_pos()
        ENDING_TEXT = get_font(90).render("CONGRATS!",True,"#D3A068")
        ENDING_MSG_TEXT = get_font(30).render(f"You recycled {score} out of 10 items!", True, "#80493A")
        ENDING_RECT = ENDING_TEXT.get_rect(center=(255, 250))
        ENDING_MSG_RECT = ENDING_MSG_TEXT.get_rect(center=(250, 330))
        ICON_RESIZE = pygame.transform.scale(icon, (120,120))
        ICON_RECT = ICON_RESIZE.get_rect(center=(245, 430))
        SCREEN.blit(ENDING_TEXT, ENDING_RECT)
        SCREEN.blit(ENDING_MSG_TEXT, ENDING_MSG_RECT)
        SCREEN.blit(ICON_RESIZE, ICON_RECT)

        for button in [self.PLAY_BUTTON, self.MENU_BUTTON]:
            button.changeColor(ENDING_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(ENDING_MOUSE_POS):
                    print("go to game")
                    #self.gameStateManager.set_state('game')
                if self.MENU_BUTTON.checkForInput(ENDING_MOUSE_POS):
                    self.gameStateManager.set_state('menu')
                # if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     pygame.quit()
                #     sys.exit()
        
class GameOver:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.BG = pygame.transform.smoothscale(pygame.image.load("assets/dark-sky.png"), (500, 700))
        
        #resize button
        img = pygame.image.load("assets/button.png")
        DFLT_IMG_SZ = (187, 71)

        self.INFO_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(125, 550), text_input="VIEW INFO", font=get_font(30), base_color="#80493A", hovering_color="#A77B5B")
        self.MENU_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(375, 550), text_input="MENU", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
    
    def run(self):
        SCREEN = self.display
        pygame.display.set_caption("Game Over")

        SCREEN.blit(self.BG, (0, 0))

        ENDING_MOUSE_POS = pygame.mouse.get_pos()
        ENDING_TEXT = get_font(90).render("GAME OVER",True,"#352B42")
        ENDING_MSG_TEXT = get_font(28).render("You FAILED to recycle enough items", True, "#43436A")
        ENDING_MSG_TWO = get_font(28).render("Doomsday is upon us", True, "#43436A")

        ENDING_RECT = ENDING_TEXT.get_rect(center=(255, 250))
        ENDING_MSG_RECT = ENDING_MSG_TEXT.get_rect(center=(250, 350))
        ENDING_MSG_TWO_RECT = ENDING_MSG_TWO.get_rect(center=(250,380))
        
        SCREEN.blit(ENDING_TEXT, ENDING_RECT)
        SCREEN.blit(ENDING_MSG_TEXT, ENDING_MSG_RECT)
        SCREEN.blit(ENDING_MSG_TWO, ENDING_MSG_TWO_RECT)

        for button in [self.INFO_BUTTON, self.MENU_BUTTON]:
            button.changeColor(ENDING_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.INFO_BUTTON.checkForInput(ENDING_MOUSE_POS):
                    print("go to info")
                    #self.gameStateManager.set_state('game')
                if self.MENU_BUTTON.checkForInput(ENDING_MOUSE_POS):
                    self.gameStateManager.set_state('menu')
                # if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     pygame.quit()
                #     sys.exit()
                    

#CHANGES STATE
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state
    
if __name__ == '__main__':
    game = Manager()
    game.run()