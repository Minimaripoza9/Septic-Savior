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
        for frame in self.all_frames:
            frame.set_colorkey(colorkey, flags)

    def load(self, image_name_and_directory: str, extension: str,frame_count: int):
        extension = extension.removeprefix(".")
        image_name_and_directory = image_name_and_directory.removeprefix("/")

        self.image_list = [load(f"{image_name_and_directory}{i}.{extension}") for i in range(frame_count)]
        self.frame_count = self.image_list.__len__()
        self.current_index = 0
        self.ticks = get_ticks()
        return self.image_list
    
    def reset(self):
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