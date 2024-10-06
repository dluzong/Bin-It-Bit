import pygame
import sys
from cutscenes import *

SCREENWIDTH, SCREENHEIGHT = 500,700
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Bin-It-Bit Game")
        self.clock = pygame.time.Clock()
        
        self.gameStateManager = GameStateManager('cutscene')
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
    def run(self):
        self.display.fill('red')
        
        

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