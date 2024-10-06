import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 500,700

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class CutsceneManager:
    def __init__(self):
        self.scenes = []
        self.active_scene = None
        self.scene_index = 0

    def add_scene(self, scene):
        self.scenes.append(scene)

    def start(self):
        if self.scenes:
            self.active_scene = self.scenes[0]
            self.scene_index = 0
            self.active_scene.start()

    def update(self):
        if self.active_scene is not None:
            if self.active_scene.is_finished():
                print('we have finished and will move on') #this isnt printing?
                self.scene_index += 1
                if self.scene_index < len(self.scenes):
                    self.active_scene = self.scenes[self.scene_index]
                    self.active_scene.start()
                else:
                    self.active_scene = None
            else:
                self.active_scene.update()

    def draw(self, screen):
        if self.active_scene is not None:
            self.active_scene.draw(screen)
    
    def return_scene_index(self):
        return self.scene_index

# Base class for scenes
class Scene:
    def start(self):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def is_finished(self):
        return True

# Example of a specific scene
class DialogueScene(Scene):
    def __init__(self, text, duration):
        #if the text is too 
        self.text = text.split('\n')    
        self.duration = duration
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.start_ticks = pygame.time.get_ticks()
        self.current_ticks = 0
        self.elapsed_time = 0

    def start(self):
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        current_ticks = pygame.time.get_ticks()  # Get current time in milliseconds
        self.elapsed_time = (current_ticks - self.start_ticks) / 1000  # Convert to seconds


    def draw(self, screen):
        #background square
        pygame.draw.rect(screen, (255, 236, 161), pygame.Rect(35, 570, 440, 115))
        offset = 0
        for item in self.text:
            print(item)
            render_text = self.font.render(item, True, BLACK)
            screen.blit(render_text, (42, 575+offset))
            offset += 20

    def is_finished(self):
        return self.elapsed_time >= self.duration