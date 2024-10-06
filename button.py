class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        
        #create button's rect based on image size
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen): #puts button on screen
        if self.image is not None:
            screen.blit(self.image, self.rect)
        #draw text on top of button, centered
        screen.blit(self.text, self.text_rect)
              
    def checkForInput(self, position): #checks if position is within bounds of button
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color) #hex A77B5B
        else:
            self.text = self.font.render(self.text_input, True, self.base_color) #hex 80493A
        #re-center after re-rendering
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
