import arcade
import os
import random

SPRITE_SCALING = 0.25
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Noodle jump"

VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

MOVEMENT_SPEED = 3
JUMP_SPEED = 10
GRAVITY = 0.5


class NoodleJump(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.wall_list = None
        self.enemy_list = None
        self.player_list = None

        self.score = 0
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.game_over = False

        self.background = None

    def setup(self):

        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        # floor
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)

        # Draw the platform
        map = []
        for x in range(SPRITE_SIZE * 3, SPRITE_SIZE * 6, SPRITE_SIZE):
            for i in range(1):
                wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

                wall.bottom = SPRITE_SIZE * 1.5
                wall.left = x
                self.wall_list.append(wall)
            wall.bottom *= 2

        # -- Set up the player
        self.player_sprite = arcade.Sprite(
            "images/character.png", SPRITE_SCALING)
        self.player_list.append(self.player_sprite)

        # Starting position of the player
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

        # Set the background color

        self.background = arcade.load_texture('images/background.jpg')

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        # Update the player based on the physics engine
        if not self.game_over:
            # Move the enemies
            self.enemy_list.update()

            # Check each enemy
            for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
                if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                    enemy.change_x *= -1
                # If the enemy hit the left boundary, reverse
                elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

            # Update the player using the physics engine
            self.physics_engine.update()

            # See if the player hit a worm. If so, game over.
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                self.game_over = True


def main():
    window = NoodleJump()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
