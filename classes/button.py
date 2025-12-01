import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.rect.Rect, onclickFunction, font : pygame.font, buttonText='\0', col = ("#ff6600", "#FF9500", "#d05a06")):
        """
        creates a 
        """
        self.onclickFunction = onclickFunction

        self.fillColors = {
            'normal': col[0],
            'hover': col[1],
            'pressed':col[2],
        }

        self.buttonRect = rect
        self.buttonSurface = pygame.Surface((self.buttonRect.width, self.buttonRect.height))

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

    def process(self):

        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        return self.buttonSurface