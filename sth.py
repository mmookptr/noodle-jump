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
        self.player_list = None
        self.noodle_list = None
        self.gold_noodle_list = None

        self.wall_left = None
        self.wall_right = None
        self.player1_sprite = None
        self.player2_sprite = None
        self.physics1_engine = None
        self.physics2_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.game_over = False

        self.background = None

        self.player1_score = 0
        self.player2_score = 0

        self.level = 1

    def level_1(self):

        self.level = arcade.Sprite("images/level1.png", SPRITE_SCALING)
        self.level.left = 350
        self.level.bottom = 770
        self.level.draw()

        map = [[3, 6, 1.3], [19, 22, 1.3], [5, 8, 2.5],
               [17, 20, 2.5], [4, 6, 3.7], [19, 21, 3.7],
               [9, 16, 3.7], [7, 8, 4.9], [17, 18, 4.9],
               [9, 16, 1.3], [1, 5, 6.1], [20, 24, 6.1],
               [6, 19, 7.3], [7, 8, 8.5], [17, 18, 8.5],
               [8, 9, 8.9], [16, 17, 8.9], [9, 10, 9.3],
               [15, 16, 9.3], [12, 13, 10.5]]
        for i in range(len(map)):
            for x in range(SPRITE_SIZE * map[i][0], SPRITE_SIZE * map[i][1], SPRITE_SIZE):
                for k in range(1):
                    wall = arcade.Sprite(
                        'images/platform2.png', SPRITE_SCALING)
                    wall.bottom = SPRITE_SIZE * map[i][2]
                    wall.left = x
                    self.wall_list.append(wall)
                wall.bottom *= 2

        noodle_map = [[10, 11, 1.8], [2, 3, 6.6], [14, 15, 1.8],
                      [12, 13, 1.8], [22, 23, 6.6], [12, 13, 4.2],
                      [4, 5, 4.2], [20, 21, 4.2], [9, 16, 6.1]]
        for i in range(len(noodle_map)):
            for x in range(SPRITE_SIZE * noodle_map[i][0], SPRITE_SIZE * noodle_map[i][1], SPRITE_SIZE):
                for k in range(1):
                    noodle = arcade.Sprite('images/noodle.png', SPRITE_SCALING)
                    noodle.bottom = SPRITE_SIZE * noodle_map[i][2]
                    noodle.left = x
                    self.noodle_list.append(noodle)
                noodle.bottom *= 2

        for j in range(SPRITE_SIZE * 12, SPRITE_SIZE * 13, SPRITE_SIZE):
            for p in range(1):
                gold_noodle = arcade.Sprite(
                    'images/goldennoodle.png', SPRITE_SCALING)
                gold_noodle.bottom = SPRITE_SIZE * 11
                gold_noodle.left = j
                self.gold_noodle_list.append(gold_noodle)
            gold_noodle.bottom *= 2

    def setup(self):

        self.wall_list = arcade.SpriteList()
        self.noodle_list = arcade.SpriteList()
        self.gold_noodle_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        # floor
        for x in range(-1, 50, SPRITE_SIZE):
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
        self.level_1()

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

        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.player_list.draw()
        self.wall_list.draw()
        self.noodle_list.draw()
        self.gold_noodle_list.draw()

        player1 = arcade.Sprite("images/player1.png", SPRITE_SCALING)
        player1.left = 20
        player1.bottom = 770
        player1.draw()
        score = arcade.Sprite('images/score.png', SPRITE_SCALING)
        score.left = 30
        score.bottom = 740
        score.draw()
        score.left = 690
        score.bottom = 740
        score.draw()

        output = f"{self.player1_score}"
        arcade.draw_text(output, 100, 740, arcade.color.BLACK_BEAN, 12)

        player2 = arcade.Sprite("images/player2.png", SPRITE_SCALING)
        player2.left = 680
        player2.bottom = 770
        player2.draw()
        output = f"{self.player2_score}"
        arcade.draw_text(output, 760, 740, arcade.color.BLACK_BEAN, 12)

        self.level.draw()

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
            self.noodle_list.update()
            self.gold_noodle_list.update()

            # check if any player hit any noodle
            player1_hit_list = arcade.check_for_collision_with_list(
                self.player1_sprite, self.noodle_list)
            player2_hit_list = arcade.check_for_collision_with_list(
                self.player2_sprite, self.noodle_list)

            # remove noodle got hit by any player
            # for coin in hit_list:
            # coin.kill()
            # self.score += 1
            for noodle in player1_hit_list:
                noodle.kill()
                self.player1_score += 100

            for noodle in player2_hit_list:
                noodle.kill()
                self.player2_score += 100

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
