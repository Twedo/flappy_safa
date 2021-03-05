import arcade as ar
import random
from pyglet.libs.win32.constants import TRUE
import os
from pipes import Pipe

# from pyglet.libs.x11.xlib import True_

SPRITE_SCALING_PLAYER = 0.09
PIPE_SCALING = 0.5
MOVEMENT_SPEED = 25
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FLOOR_KILL = 190
PIPE_GAP = 100
MIN_HEIGHT = 50
# BIRD_MOVE = 5
pipe = ["assets" + os.sep + "sprites" + os.sep + "fb_pipe2.png"]

# sounds
die_sound = ar.load_sound("sound_effects/die.mp3")
hit_sound = ar.load_sound("sound_effects/hit.mp3")
point_sound= ar.load_sound("sound_effects/point.mp3")
swoosh_sound = ar.load_sound("sound_effects/swoosh.mp3")
wing_sound = ar.load_sound("sound_effects/wing.mp3")


class Player(ar.Sprite):
    """ Player Class """

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        self.bottom = SCREEN_HEIGHT
        self.top = SCREEN_HEIGHT
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


        # checks for collision with floor. 
        if self.bird_sprite.center_y <= 200: 
            print("hit floor")



class GameWindow(ar.Window):
    def __init__(self, win_width, win_height):
        super().__init__(win_width, win_height, "Flappy Safa")
        
        
        
      #  ar.set_background_color(ar.csscolor.LIGHT_SKY_BLUE)
        self.background = None
        self.sprite_list = None
     #   self.set_mouse_visible(False)
        self.bird_sprite = None
        self.shut_keys = False
        
        
        
        # Background
        self.background = None
        self.view_bottom = 0
        self.view_left = 0
        self.score = 0
    
        # Pipes
        self.pipe_sprites = None
        # self.horizontal_speed = -1.5
        self.BIRD_MOVE = -5
    
    

    def setup(self):
        """ Set up the game here """
        self.sprite_list = ar.SpriteList()
        
        # Setup background
        bg_choice = random.randint(0,1)
        if bg_choice == 0:
            self.background = ar.load_texture("images/fb_background_day.png")
        else:
            self.background = ar.load_texture("images/fb_background_night.png")
            
            
        # Setup floor
        self.base = ar.load_texture("images/fb_base.png")
        
        
        
        
        
        # Pipes
        self.pipe_sprites = ar.SpriteList()
        
        self.sprites = dict()
        self.sprites["background"] = self.background
        self.sprites["base"] = self.base
        
        
        # Create a random pipe to start with
        start_pipe1 = Pipe.random_pipe_obstacle(self.sprites, self.height)
        self.pipe_sprites.append(start_pipe1[0])
        self.pipe_sprites.append(start_pipe1[1])
        
    
        # Has the game started?
        self.begin = False

        # bird sprite
        self.bird_sprite = ar.Sprite("images/fb_icon5.png", SPRITE_SCALING_PLAYER)
        self.bird_sprite.center_x = 135
        self.bird_sprite.center_y = 280
        self.sprite_list.append(self.bird_sprite)
        
        
        # Setup Background
        # speed = 30
        # self.background = ar.load_texture("images/fb_background.png")
        
        # Minimum margins for bg
        left_margin = 250
        right_margin = 250
        bottom_margin = 50
        top_margin = 100
        

    




    def on_draw(self):
        """ Render the screen. """

        ar.start_render()

        # draw background image
        ar.draw_texture_rectangle(144, 256, self.background.width * 2.2, self.background.height, self.background)
        # Draw pipes
        self.pipe_sprites.draw()
        # Draw base       
        ar.draw_texture_rectangle(168, 45, self.base.width * 2.25, self.base.height, self.base)
        # draw flappy bird
        self.sprite_list.draw()
       
        # print(SCREEN_WIDTH // 6)
        #print(self.base.height)
        # print(self.background.width)
        # print(self.background.height)
        
        # self.top_pipe.draw()
        
        
        """gameover screen"""
        self.gameover_icon = ar.Sprite("images/fb_gameover.png", 0.20)
        self.gameover_icon.center_y = 350
        self.gameover_icon.center_x = 144
        if self.bird_sprite.center_y <= 120: 
            self.gameover_icon.draw()
            self.shut_keys = True
            self.bird_sprite.center_y = 120
           # ar.play_sound(die_sound)

        """display score"""
        output = f"Score: {self.score}"
        ar.draw_text(output, 10, 20, ar.color.WHITE, 25, font_name = "04B_19__")
        
        
        """ Are you ready? """
        

        pipe_list = []
        location_x_axis = 0
        # while self.shut_keys == False:
        #     location_x_axis += 300
        #     self.pipe = random.choice(pipe_list)
        #     pipe.center_x = location_x_axis
        #     pipe.draw()
        # pipe_spawn()

       
    
    def on_update(self, delta_time):
        "Movement and Game Logic"
        self.sprite_list.update()
        
        new_pipe = None
        
        # Kill pipes that are no longer shown on the screen as they're useless and live in ram and create a new pipe
            # when needed. (If the center_x of the closest pipe to the bird passed the middle of the screen)
        for pipe in self.pipe_sprites:
            if pipe.right <= 0:
                pipe.kill()
            elif len(self.pipe_sprites) == 2 and pipe.right <= random.randrange(self.width // 2, self.width // 2 + 15):
                new_pipe = Pipe.random_pipe_obstacle(self.sprites, self.height)

        if new_pipe:
            self.pipe_sprites.append(new_pipe[0])
            self.pipe_sprites.append(new_pipe[1])
            
        
        # This calls "update()" Method on each object in the SpriteList
        
        # self.bird.update(delta_time)
        # self.bird_list.update()
        
        # If the bird passed the center of the pipe safely, count it as a point.
        if self.bird_sprite.center_x >= self.pipe_sprites[0].center_x and not self.pipe_sprites[0].scored:
            ar.play_sound(point_sound) 
            self.score += 1
            # Well, since each "obstacle" is a two pipe system, we gotta count them both as scored.
            self.pipe_sprites[0].scored = True
            self.pipe_sprites[1].scored = True
            print(self.score)

        # Check if the bird collided with any of the pipes
        self.hit = ar.check_for_collision_with_list(self.bird_sprite, self.pipe_sprites)
        # print(self.hit)
        if len(self.hit) <= 0:
            self.pipe_sprites.update()
        if len(self.hit) >= 1:
            self.shut_keys = True
            self.bird_sprite.center_y = 120
           #ar.play_sound(hit_sound)
            # print(self.shut_keys)
       # if self.bird_sprite.center_y == 120:
           # ar.play_sound(die_sound)
            
            


        

    def on_key_press(self, key, modifier): # to go up
            
            if key == ar.key.SPACE and self.shut_keys == False and len(self.hit) <= 0:    
                self.bird_sprite.change_y = 5
                ar.play_sound(wing_sound)
                self.begin = True
                
            

    def on_key_release(self, key, modifier): # to go down
            if key == ar.key.SPACE and self.shut_keys == False:   
                self.bird_sprite.change_y = self.BIRD_MOVE
                print(key)



        
            
       
def main(): 
    
    """ Main method """
    window = GameWindow(288, 512)
    window.setup()
    ar.run()
    
if __name__ == "__main__":
    main()

