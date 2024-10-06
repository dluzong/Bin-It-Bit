import pygame
import sys

from cutscenes import *
from info import *
from button import Button
from sine import *

from game import Game

SCREENWIDTH, SCREENHEIGHT = 500,700
FPS = 60

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/ARCADECLASSIC.TTF", size)

class Manager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Bin-It-Bit Game")
        self.clock = pygame.time.Clock()
        
        self.gameStateManager = GameStateManager('menu') #the app should start at the menu
        self.menu = Menu(self.screen, self.gameStateManager)
        self.cutscene = Cutscene(self.screen, self.gameStateManager)
        self.info = Info(self.screen, self.gameStateManager)
        self.index = Index(self.screen, self.gameStateManager)
        self.gameplay = Game(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.gameStateManager)
        self.ending = Ending(self.screen, self.gameStateManager)
        self.gameOver = GameOver(self.screen, self.gameStateManager)
        
        self.states = {'menu':self.menu, 'cutscene':self.cutscene, 'info':self.info, 'index':self.index, 'gameplay':self.gameplay, 'ending':self.ending, 'gameOver':self.gameOver}
        
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
        cutscene_manager.add_scene(DialogueScene('It was an ordinary day in Union Square.\nYou were on astroll when you\nlook up and notice...', 4))
        cutscene_manager.add_scene(DialogueScene('The doomsday clock was finally counting \ndown to...', 3))
        cutscene_manager.add_scene(DialogueScene('...', 2))
        cutscene_manager.add_scene(DialogueScene('...zero??', 2))
        cutscene_manager.add_scene(DialogueScene('The climate change apocalypse \nhas finally begun?!', 3))
        cutscene_manager.add_scene(DialogueScene('As a consequence of not taking \nenough precautions, the inhabitants of \nEarth are forced to collect trash \nunless they want to be buried \nunder it forever!!', 5))
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
                self.gameStateManager.set_state('gameplay') #now start the gameplay


class Menu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.BG = pygame.transform.smoothscale(pygame.image.load("assets/bright-sky.png"), (500, 700))
        
        # LOADING TRACK
        pygame.mixer.music.load("assets/tracks/A Hearty Fellow (LOOP).wav")
        # SET TRACK VOLUME
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        #resize button
        img = pygame.image.load("assets/button.png")
        DFLT_IMG_SZ = (187, 71)

        self.START_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(125, 470), text_input="START", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
        self.INDEX_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(375, 470), text_input="INDEX", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
        self.INFO_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(125, 590), text_input="INFO", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
        self.QUIT_BUTTON = Button(image=pygame.transform.scale(img, DFLT_IMG_SZ), pos=(375, 590), text_input="QUIT", font=get_font(40), base_color="#80493A", hovering_color="#A77B5B")
    
    def run(self):
        SCREEN = self.display
        pygame.display.set_caption("Menu")
        
        SCREEN.blit(self.BG, (0, 0))

        logo = pygame.image.load("assets/game-logo.png")

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = pygame.transform.scale(logo, (500,500))
        y = sine(200.0, 1280, 10.0, 240)
        MENU_RECT = MENU_TEXT.get_rect(center=(250, y+30))
        
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
                    self.gameStateManager.set_state('info')
                if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                pygame.mixer.music.stop

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
                    self.gameStateManager.set_state('info')
                if self.MENU_BUTTON.checkForInput(ENDING_MOUSE_POS):
                    self.gameStateManager.set_state('menu')
                # if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     pygame.quit()
                #     sys.exit()
                    


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
        pygame.display.set_caption("F")

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
    game = Manager()
    game.run()