import arcade as ar
import random
from pyglet.libs.win32.constants import TRUE

SPRITE_SCALING_PLAYER = 0.11
PIPE_SCALING = 0.5
MOVEMENT_SPEED = 25
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FLOOR_KILL = 200
PIPE_GAP = 100

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
class Pipe(ar.Sprite):

    def __init__(self, image, scale = 1):
        super().__init__(image, scale)
        self.scored = False
        self.pipe_movement = -2 
        
    @classmethod
    def random_pipe(cls, sprites, height):
        self.top_pipe = cls(Pipe)
        self.top_pipe = ar.Sprite("images/fb_pipe2.png")
        self.top_pipe.angle = 180
        
        self.bottom_pipe = ar.Sprite("images/fb_pipe2.png")
        return self.top_pipe, self.bottom_pipe


class GameWindow(ar.Window):
    def __init__(self):
        super().__init__(450, 512, "Flappy Bird")
        
        
        
      #  ar.set_background_color(ar.csscolor.LIGHT_SKY_BLUE)
        self.background = None
        self.sprite_list = None
     #   self.set_mouse_visible(False)
        self.bird_sprite = None
        self.shut_keys = False
        self.pipe_sprites = None
        
        
        
        # Background
        self.background = None
        
        self.view_bottom = 0
        self.view_left = 0
        
        self.score = 0
    
    

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.sprite_list = ar.SpriteList()
        self.pipe_list = ar.SpriteList()

        self.pipe_sprites = ar.SpriteList()
	
        # A dict holding a reference to the textures
        self.sprites = dict()
        # self.sprites['background'] = self.background
        # self.sprites['base'] = self.base
        
        # Create a random pipe (obstacle) to start with
        start_pipe1 = Pipe.random_pipe("images/fb_pipe2.png", self.height)
        self.pipe_sprites.append(start_pipe1[0])
        self.pipe_sprites.append(start_pipe1[1])

        # bird sprite
        self.bird_sprite = ar.Sprite("images/fb_icon3.png", SPRITE_SCALING_PLAYER)
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
        

        # Setup background
        bg_choice = random.randint(0,1)
        if bg_choice == 0:
            self.background = ar.load_texture("images/fb_background_day.png")
        else:
            self.background = ar.load_texture("images/fb_background_night.png")
            
            
        # Setup floor
        self.base = ar.load_texture("images/fb_base.png")
        

        # pipe image 1
        # self.pipe1_sprite = ar.Sprite("images/fb_pipe1.png", PIPE_SCALING)
        # self.pipe1_sprite.center_y = 360
        # self.pipe1_sprite.center_x = 200
        # self.pipe_list.append(self.pipe1_sprite)
        # pipe image 2
        self.pipe2_sprite = ar.Sprite("images/fb_pipe2.png", 0.3)
        self.pipe2_sprite.center_y = 360
        self.pipe2_sprite.center_x = 400
        self.pipe_list.append(self.pipe2_sprite)




    def on_draw(self):
        """ Render the screen. """

        ar.start_render()

        # Whatever the state, we need to draw background, then pipes on top, then base, then bird.
        self.draw_background()
        self.pipe_sprites.draw()
        self.draw_base()
        self.bird_list.draw()


        # draw background image
        ar.draw_texture_rectangle(144, 256, self.background.width * 2.2, self.background.height, self.background)
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
        self.gameover_icon = ar.Sprite("images/fb_gameover.png", 0.25)
        self.gameover_icon.center_y = 350
        self.gameover_icon.center_x = 230
        if self.bird_sprite.center_y <= 130: 
            self.gameover_icon.draw()
            self.shut_keys = True
            self.bird_sprite.center_y = 130
           # ar.play_sound(die_sound)

        """display score"""
        output = f"Score: {self.score}"
        ar.draw_text(output, 10, 20, ar.color.WHITE, 16)

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
        self.pipe_sprites.update()
			
	
	# If the bird passed the center of the pipe safely, count it as a point.
            # Hard coding.. :)
        if self.bird.center_x >= self.pipe_sprites[0].center_x and not self.pipe_sprites[0].scored:
            # arcade.play_sound(SOUNDS['point'])
            self.score += 1
            # Well, since each "obstacle" is a two pipe system, we gotta count them both as scored.
            self.pipe_sprites[0].scored = True
            self.pipe_sprites[1].scored = True
            print(self.score)
	
	# Check if the bird collided with any of the pipes
        hit = ar.check_for_collision_with_list(self.bird, self.pipe_sprites)


        

    def on_key_press(self, key, modifier): # to go up
            if key == ar.key.SPACE and self.shut_keys == False:    
                self.bird_sprite.change_y = MOVEMENT_SPEED
                ar.play_sound(wing_sound)
            
      

    def on_key_release(self, key, modifier): # to go down
            if key == ar.key.SPACE and self.shut_keys == False:   
                self.bird_sprite.change_y = -10 
            


        
            
       
def main(): 
    
    """ Main method """
    window = GameWindow()
    window.setup()
    ar.run()
    
if __name__ == "__main__":
    main()

