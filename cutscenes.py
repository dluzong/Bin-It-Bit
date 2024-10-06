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
        self.text = text
        self.duration = duration
        self.font = pygame.font.SysFont('Arial', 32)
        self.start_ticks = pygame.time.get_ticks()

    def start(self):
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        current_ticks = pygame.time.get_ticks()
        self.elapsed_time = (current_ticks - self.start_ticks) / 1000

    def draw(self, screen):
        screen.fill(BLACK)
        render_text = self.font.render(self.text, True, WHITE)
        text_rect = render_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(render_text, text_rect)

    def is_finished(self):
        return self.elapsed_time >= self.duration