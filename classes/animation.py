import pygame

load = pygame.image.load
get_ticks = pygame.time.get_ticks


class Animation():
    """
    Class that manages sprite animation for pygame
    """
    def __init__(self, image_list: list, default_frame_speed: int = 100):
        """
        pre-made list constructor
        """
        self.all_frames = image_list
        self.frame_count = image_list.__len__()
        self.current_index = 0

        self.ticks = get_ticks()

        self.frame_speeds = [default_frame_speed for i in range(self.frame_count)] #parallel list with frame speed for each frame

    def set_colorkey_all(self, colorkey, flags: int = 0):
        """
        sets colorkey for every frame in the animation
        """
        for frame in self.all_frames:
            frame.set_colorkey(colorkey, flags)
        return self

    def flip_frames(self, flip_x: bool = False, flip_y: bool = False) -> pygame.Surface:
        """
        flips every frame by the chosen axis
        """
        return Animation([pygame.transform.flip(frame, flip_x, flip_y) for frame in self.all_frames], self.frame_speeds[0])
    
    def reset(self):
        """
        resets animation frames
        """
        self.current_index = 0
        self.ticks = get_ticks()
    
    def update(self) -> pygame.image:
        """
        updates and returns the current animation frame
        """
        now = get_ticks()
        if now - self.ticks > self.frame_speeds[self.current_index]:
            self.ticks = now
            self.current_index = (self.current_index + 1) % self.frame_count
        return self.all_frames[self.current_index]
    
    def set_framespeed(self, frame: int, milliseconds: int):
        self.frame_speeds[frame] = milliseconds