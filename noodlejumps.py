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
        self.door_list = None

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

        self.head = None
        self.title = None

        self.level = 1

        self.instruction = []
        self.current_state = 0

        
        page = arcade.load_texture('images/instructionpage.png')
        self.instruction.append(page)

    def create_platform(self, map):
        for i in range(len(map)):
            for x in range(SPRITE_SIZE * map[i][0], SPRITE_SIZE * map[i][1], SPRITE_SIZE):
                for k in range(1):
                    wall = arcade.Sprite(
                        'images/platform2.png', SPRITE_SCALING)
                    wall.bottom = SPRITE_SIZE * map[i][2]
                    wall.left = x
                    self.wall_list.append(wall)
                wall.bottom *= 2

    def create_noodle(self, noodle_map):
        for i in range(len(noodle_map)):
            for x in range(SPRITE_SIZE * noodle_map[i][0], SPRITE_SIZE * noodle_map[i][1], SPRITE_SIZE):
                for k in range(1):
                    noodle = arcade.Sprite('images/noodle.png', SPRITE_SCALING)
                    noodle.bottom = SPRITE_SIZE * noodle_map[i][2]
                    noodle.left = x
                    self.noodle_list.append(noodle)
                noodle.bottom *= 2

    def level_1(self):

        self.head = arcade.Sprite("images/level1.png", SPRITE_SCALING)
        self.head.left = 350
        self.head.bottom = 770
        self.head.draw()

        map = [[3, 6, 1.3], [19, 22, 1.3], [5, 8, 2.5],
               [17, 20, 2.5], [4, 6, 3.7], [19, 21, 3.7],
               [9, 16, 3.7], [7, 8, 4.9], [17, 18, 4.9],
               [9, 16, 1.3], [1, 5, 6.1], [20, 24, 6.1],
               [6, 19, 7.3], [7, 8, 8.5], [17, 18, 8.5],
               [8, 9, 8.9], [16, 17, 8.9], [9, 10, 9.3],
               [15, 16, 9.3], [12, 13, 10.5]]

        self.create_platform(map)

        noodle_map = [[10, 11, 2.5], [2, 3, 7.3], [14, 15, 2.5],
                      [12, 13, 2.5], [22, 23, 7.3],[4, 5, 4.9], 
                      [20, 21, 4.9], [10, 11, 4.7], [11, 12, 5], 
                      [12, 13, 5.3], [13, 14, 5.3], [14, 15, 5],
                      [15, 16, 4.7]]

        self.create_noodle(noodle_map)

        for j in range(SPRITE_SIZE * 12, SPRITE_SIZE * 13, SPRITE_SIZE):
            for p in range(1):
                door = arcade.Sprite(
                    'images/door.png', SPRITE_SCALING)
                door.bottom = SPRITE_SIZE * 11
                door.left = j
                self.door_list.append(door)
            door.bottom *= 2

    def level_2(self):
        self.level_init()

        self.head = arcade.Sprite("images/level2.png", SPRITE_SCALING)
        self.head.left = 350
        self.head.bottom = 770
        self.head.draw()

        for x in range(0, 800, SPRITE_SIZE):
            wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x

            self.wall_list.append(wall)

        for x in range(0, 800, SPRITE_SIZE):
            wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

            wall.bottom = 375
            wall.left = x

            self.wall_list.append(wall)

        # player 1
        self.player1_sprite = arcade.Sprite(
            "images/character1.png", SPRITE_SCALING)
        self.player_list.append(self.player1_sprite)

        # player1 falling position
        self.player1_sprite.center_x = 70
        self.player1_sprite.center_y = 410

        self.physics1_engine = arcade.PhysicsEnginePlatformer(self.player1_sprite,
                                                              self.wall_list,
                                                              gravity_constant=GRAVITY)
        # player 2
        self.player2_sprite = arcade.Sprite(
            "images/character2left.png", SPRITE_SCALING)
        self.player_list.append(self.player2_sprite)

        # player2 falling position
        self.player2_sprite.center_x = 70
        self.player2_sprite.center_y = 10

        self.physics2_engine = arcade.PhysicsEnginePlatformer(self.player2_sprite,
                                                              self.wall_list,
                                                              gravity_constant=GRAVITY)

        map = [[3, 7, 1.3], [3, 7, 7.2], [8, 10, 1.3], [8, 10, 7.2],
               [12, 15, 1.3], [12, 15, 7.2], [16, 19, 1.3], [16, 19, 7.2],
               [21, 24, 2.4], [21, 24, 8.3], [4, 19, 3.5], [4, 19, 9.4], [1, 2, 4.5], [1, 2, 10.4]]

        self.create_platform(map)

        noodle_map = [[5, 6, 2.5], [5, 6, 8.4], [9, 10, 2.5],
                      [9, 10, 8.4], [13, 14, 2.5], [13, 14, 8.4],
                      [22, 23, 3.6], [22, 23, 9.5], [5, 6, 4.4],
                      [5, 6, 10.3], [6, 7, 10], [6, 7, 4.1], [7, 8, 10.3],
                      [7, 8, 4.4], [8, 9, 4.7], [8, 9, 10.6], [9, 10, 5],
                      [9, 10, 10.9], [10, 11, 10.6], [
                          10, 11, 4.7], [11, 12, 4.4],
                      [11, 12, 10.3], [12, 13, 4.1], [
                          12, 13, 10], [13, 14, 4.4],
                      [13, 14, 10.3], [14, 15, 10.6], [14, 15, 4.7],
                      [15, 16, 5],[15, 16, 10.9],[16, 17, 4.7],[16, 17, 10.6]
                      ]

        self.create_noodle(noodle_map)

        door_map = [[1, 2, 4.5], [1, 2, 10.4]]

        for j in range(SPRITE_SIZE * 1, SPRITE_SIZE * 2, SPRITE_SIZE):
            for p in range(1):
                door = arcade.Sprite(
                    'images/door.png', SPRITE_SCALING)
                door.bottom = SPRITE_SIZE * 5
                door.left = j
                self.door_list.append(door)
            door.bottom *= 2

        for j in range(SPRITE_SIZE * 1, SPRITE_SIZE * 2, SPRITE_SIZE):
            for p in range(1):
                door = arcade.Sprite(
                    'images/door.png', SPRITE_SCALING)
                door.bottom = SPRITE_SIZE * 10.9
                door.left = j
                self.door_list.append(door)
            door.bottom *= 2

    def level_3(self):
        self.level_init()

        self.head = arcade.Sprite("images/level3.png", SPRITE_SCALING)
        self.head.left = 350
        self.head.bottom = 770
        self.head.draw()

        for x in range(29, 200, SPRITE_SIZE):
            wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x

            self.wall_list.append(wall)
        for x in range(770, 590, -SPRITE_SIZE):
            wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.right = x
            self.wall_list.append(wall)

        # player 1
        self.player1_sprite = arcade.Sprite(
            "images/character1.png", SPRITE_SCALING)
        self.player_list.append(self.player1_sprite)

        # player1 falling position
        self.player1_sprite.center_x = 70
        self.player1_sprite.center_y = 10

        self.physics1_engine = arcade.PhysicsEnginePlatformer(self.player1_sprite,
                                                              self.wall_list,
                                                              gravity_constant=GRAVITY)
        # player 2
        self.player2_sprite = arcade.Sprite(
            "images/character2.png", SPRITE_SCALING)
        self.player_list.append(self.player2_sprite)

        # player2 falling position
        self.player2_sprite.center_x = 710
        self.player2_sprite.center_y = 10

        self.physics2_engine = arcade.PhysicsEnginePlatformer(self.player2_sprite,
                                                              self.wall_list,
                                                              gravity_constant=GRAVITY)

        map = [[6, 7, 1.3], [18, 19, 1.3], [3, 4, 2.5], [21, 22, 2.5],
               [6, 7, 3.7], [18, 19, 3.7], [3, 4, 4.9], [21, 22, 4.9],
               [6, 7, 6.1], [18, 19, 6.1], [3, 4, 7.3], [21, 22, 7.3],
               [6, 7, 8.5], [18, 19, 8.5], [3, 4, 9.7], [21, 22, 9.7],
               [6, 11, 10.9], [14, 19, 10.9], [10, 11, 10.4], [14, 15, 10.4],
               [10, 11, 9.9], [14, 15, 9.9], [10, 11, 9.4], [14, 15, 9.4],
               [10, 11, 8.9], [14, 15, 8.9], [10, 11, 8.4], [14, 15, 8.4],
               [10, 11, 7.9], [14, 15, 7.9], [10, 11, 7.4], [14, 15, 7.4],
               [10, 15, 6.9], [9, 16, 4.1]]

        self.create_platform(map)

        noodle_map = [[6, 7, 2.5], [18, 19, 2.5], [3, 4, 3.7], [21, 22, 3.7],
                      [6, 7, 4.9], [18, 19, 4.9], [3, 4, 6.1], [21, 22, 6.1],
                      [6, 7, 7.3], [18, 19, 7.3], [3, 4, 8.5], [21, 22, 8.5],
                      [11, 14, 5.3], ]

        self.create_noodle(noodle_map)

        for j in range(SPRITE_SIZE * 12, SPRITE_SIZE * 13, SPRITE_SIZE):
            for p in range(1):
                door = arcade.Sprite(
                    'images/door.png', SPRITE_SCALING)
                door.bottom = SPRITE_SIZE * 7.4
                door.left = j
                self.door_list.append(door)
            door.bottom *= 2

    def level_4(self):
        self.level_init()

    def level_init(self):
        self.wall_list = arcade.SpriteList()
        self.noodle_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

    def draw_game_over(self):

        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, 310, 300, arcade.color.WHITE, 24)

    def setup(self):
        self.current_state = 1
        self.level_init()

        self.level_1()
        self.level = 1

        # floor
        for x in range(49, 100, SPRITE_SIZE):
            wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x

            self.wall_list.append(wall)
        for x in range(750, 700, -SPRITE_SIZE):
            wall = arcade.Sprite("images/platform1.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.right = x
            self.wall_list.append(wall)

        # player 1
        self.player1_sprite = arcade.Sprite(
            "images/character1.png", SPRITE_SCALING)
        self.player_list.append(self.player1_sprite)

        # player1 falling position
        self.player1_sprite.center_x = 70
        self.player1_sprite.center_y = 10

        self.physics1_engine = arcade.PhysicsEnginePlatformer(self.player1_sprite,
                                                              self.wall_list,
                                                              gravity_constant=GRAVITY)
        # player 2
        self.player2_sprite = arcade.Sprite(
            "images/character2.png", SPRITE_SCALING)
        self.player_list.append(self.player2_sprite)

        # player2 falling position
        self.player2_sprite.center_x = 710
        self.player2_sprite.center_y = 10

        self.physics2_engine = arcade.PhysicsEnginePlatformer(self.player2_sprite,
                                                              self.wall_list,
                                                              gravity_constant=GRAVITY)

        # background picture
        self.background = arcade.load_texture('images/background.jpg')

    def draw_game(self):

        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)


        self.player_list.draw()
        self.wall_list.draw()
        self.noodle_list.draw()
        self.door_list.draw()

        player1 = arcade.Sprite("images/player1.png", SPRITE_SCALING)
        player1.left = 20
        player1.bottom = 770
        player1.draw()
        score = arcade.Sprite('images/score.png', SPRITE_SCALING)
        score.left = 20
        score.bottom = 740
        score.draw()
        score.left = 680
        score.bottom = 740
        score.draw()

        output = f"{self.player1_score}"
        arcade.draw_text(output, 90, 740, arcade.color.BLACK_BEAN, 12)

        player2 = arcade.Sprite("images/player2.png", SPRITE_SCALING)
        player2.left = 680
        player2.bottom = 770
        player2.draw()
        output = f"{self.player2_score}"
        arcade.draw_text(output, 750, 740, arcade.color.BLACK_BEAN, 12)

        # self.level.draw()
        self.head.draw()
        self.current = 1

    def on_draw(self):
        
        if self.current_state == 1:
            self.draw_instruction()

        else:
            self.draw_game()

    def on_mouse_press(self, x, y, button, modifiers):
    
        if self.current_state == 1:
            self.current_state = 2
        elif self.current_state == 2:
            self.setup()

    def draw_instruction(self):

        
        self.background = arcade.load_texture('images/background.jpg')
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.title = arcade.Sprite("images/header.png")
        self.title.left = 70 
        self.title.bottom = 720
        self.title.draw()
        
        page_texture = arcade.load_texture('images/instructionpage.png')
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.3,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
        
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
        if key == arcade.key.A or key == arcade.key.D:
            self.player1_sprite.change_x = 0

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player2_sprite.change_x = 0

    def update(self, delta_time):


        # Update the player based on the physics engine
        if self.current_state == 2 :
            # Move the enemies
            self.noodle_list.update()
            self.door_list.update()

            # check if any player hit any noodle
            player1_hit_list = arcade.check_for_collision_with_list(
                self.player1_sprite, self.noodle_list)
            player2_hit_list = arcade.check_for_collision_with_list(
                self.player2_sprite, self.noodle_list)

            # chech if any player hit gold noodle
            player1_door_list = arcade.check_for_collision_with_list(
                self.player1_sprite, self.door_list)
            player2_door_list = arcade.check_for_collision_with_list(
                self.player2_sprite, self.door_list)


            # add score by 100 if hits noodle
            for noodle in player1_hit_list:
                noodle.kill()
                self.player1_score += 100

            for noodle in player2_hit_list:
                noodle.kill()
                self.player2_score += 100

            # add score by 300 if hits door and pass to next level
            if len(player1_door_list) > 0 and self.level == 1:
                self.player1_score += 300
                self.level += 1
                self.level_2()

            elif len(player2_door_list) > 0 and self.level == 1:
                self.player2_score += 300
                self.level += 1
                self.level_2()

            elif len(player1_door_list) > 0 and self.level == 2:
                self.player1_score += 300
                self.level += 1
                self.level_3()

            elif len(player2_door_list) > 0 and self.level == 2:
                self.player2_score += 300
                self.level += 1
                self.level_3()

            elif len(player1_door_list) > 0 and self.level == 3:
                self.player1_score += 300
                # self.level += 1 
                # self.level_4()
                self.game_over = True

            elif len(player2_door_list) > 0 and self.level == 3:
                self.player2_score += 300
                # self.level += 1
                # self.level_4()
                self.game_over = True

            # Update the player using the physics engine
            self.physics1_engine.update()
            self.physics2_engine.update()

        elif  self.game_over == True:
            self.draw_game_over()

def main():
    window = NoodleJump()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
