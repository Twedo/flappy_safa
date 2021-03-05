# import arcade as ar

# SPRITE_SCALING_PLAYER = 0.5
# MOVEMENT_SPEED = 5

# class GameWindow(ar.Window):
#     def __init__(self):
#         super().__init__(400, 800, "Flappy Bird")
        
#         ar.set_background_color(ar.csscolor.LIGHT_SKY_BLUE)
#         self.sprite_list = None
#         self.set_mouse_visible(False)
#         self.bird_sprite = None
        
#         # or 
#         # ar.set_background_color(ar.color.CHAMPAGNE)
    

#     def setup(self):
#         """ Set up the game here. Call this function to restart the game. """
#         self.sprite_list = ar.SpriteList()

#         # bird sprite
#         self.bird_sprite = ar.Sprite("images/fb_icon3.png", SPRITE_SCALING_PLAYER)
#         self.bird_sprite.center_x = 600
#         self.bird_sprite.center_y = 300
#         self.sprite_list.append(self.bird_sprite)


#     def on_draw(self):
#         """ Render the screen. """
#         ar.start_render()

#         # Code to draw the screen goes here
#         self.sprite_list.draw()

#     def on_key_press(self, key):
#         if key == ar.key.SPACE: 
            

# def main():
#     """ Main method """
#     window = GameWindow()
#     window.setup()
#     ar.run()
    
# if __name__ == "__main__":
#     main()

import arcade

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move Sprite with Keyboard Example"

MOVEMENT_SPEED = 5


class Player(arcade.Sprite):
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

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("fb.icon2.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # If the player presses a key, update the speed
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()