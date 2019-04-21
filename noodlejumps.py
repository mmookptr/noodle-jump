import arcade
import os
import random

SPRITE_SCALING = 0.25
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Noodle jump"

VIEWPORT_MARGIN = 100
RIGHT_MARGIN = 150

MOVEMENT_SPEED = 3
JUMP_SPEED = 9
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
        self.player1_sprite = None
        self.player2_sprite = None
        self.physics1_engine = None
        self.physics2_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.game_over = False

        self.background = None

    def setup(self):

        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        # floor
        for x in range(0, 50, SPRITE_SIZE):
            wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x

            self.wall_list.append(wall)
        for x in range(800, 750, -SPRITE_SIZE):
            wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.right = x
            self.wall_list.append(wall)

        # build the platform total of 25 blocks
        map = [[3, 6, 1.3], [19, 22, 1.3], [
            5, 8, 2.5], [17, 20, 2.5], [4, 6, 3.7], [19, 21, 3.7], [9, 16, 3.7]]
        for i in range(len(map)):
            for x in range(SPRITE_SIZE * map[i][0], SPRITE_SIZE * map[i][1], SPRITE_SIZE):
                for k in range(1):
                    wall = arcade.Sprite(
                        'images/platform2.png', SPRITE_SCALING)
                    wall.bottom = SPRITE_SIZE * map[i][2]
                    wall.left = x
                    self.wall_list.append(wall)
                wall.bottom *= 2

        # player 1
        self.player1_sprite = arcade.Sprite(
            "images/character.png", SPRITE_SCALING)
        self.player_list.append(self.player1_sprite)

        # player1 falling position
        self.player1_sprite.center_x = 10
        self.player1_sprite.center_y = 10

        self.physics1_engine = arcade.PhysicsEnginePlatformer(self.player1_sprite,
                                                              self.wall_list,
                                                              gravity_constant=GRAVITY)
        # player 2
        self.player2_sprite = arcade.Sprite(
            "images/character.png", SPRITE_SCALING)
        self.player_list.append(self.player2_sprite)

        # player2 falling position
        self.player2_sprite.center_x = 790
        self.player2_sprite.center_y = 10

        self.physics2_engine = arcade.PhysicsEnginePlatformer(self.player2_sprite,
                                                              self.wall_list,
                                                              gravity_constant=GRAVITY)

        # background picture
        self.background = arcade.load_texture('images/background.jpg')

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # self.player1_sprite.draw()
        # self.player2_sprite.draw()
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()

    def on_key_press(self, key, modifiers):
        # player1
        if key == arcade.key.W:
            if self.physics1_engine.can_jump():
                self.player1_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.A:
            self.player1_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player1_sprite.change_x = MOVEMENT_SPEED

        # player2
        if key == arcade.key.UP:
            if self.physics2_engine.can_jump():
                self.player2_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player2_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player2_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.A or key == arcade.key.D:
            self.player1_sprite.change_x = 0

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player2_sprite.change_x = 0

    def update(self, delta_time):

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
            self.physics1_engine.update()
            self.physics2_engine.update()

            # See if the player hit a worm. If so, game over.
            if len(arcade.check_for_collision_with_list(self.player1_sprite, self.enemy_list)) > 0:
                self.game_over = True
            if len(arcade.check_for_collision_with_list(self.player2_sprite, self.enemy_list)) > 0:
                self.game_over = True


def main():
    window = NoodleJump()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
