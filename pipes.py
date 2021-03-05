import random
import os
import arcade as ar
MIN_HEIGHT = 50
GAP_SIZE = 120

# pipe = ["assets" + os.sep + "sprites" + os.sep + "fb_pipe2.png"]
pipe = "images/fb_pipe2.png"


class Pipe(ar.Sprite):

    def __init__(self, image, scale=1):
        super().__init__(image, scale)
        # the amount of pixels the pipe move each frame.
        self.horizontal_speed = -1.5
        # Just a boolean to check if the bird passed this pipe successfully.
        self.scored = False

    @classmethod
    def random_pipe_obstacle(cls, sprites, height):
        bottom_pipe = cls(pipe)
        bottom_pipe.top = random.randrange(sprites['base'].height + MIN_HEIGHT, height - GAP_SIZE - MIN_HEIGHT)
        bottom_pipe.left = sprites['background'].width

        top_pipe = cls(pipe)
        top_pipe.angle = 180
        top_pipe.left = sprites['background'].width
        top_pipe.bottom = bottom_pipe.top + GAP_SIZE 
        
        return bottom_pipe, top_pipe

    def update(self):
        # Move each frame in the negative x direction.
        self.center_x += self.horizontal_speed
        
    