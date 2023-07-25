import pygame
from utils import (
    Direction,
    ScoreType,
    GhostBehaviour,
    translate_maze_to_screen,
    translate_screen_to_maze,
)


class GameObject:
    def __init__(
        self,
        in_surface,
        x,
        y,
        in_size: int,
        in_color=(255, 0, 0),
        is_circle: bool = False,
        is_line: bool = False,
    ):
        self._size = in_size
        self._renderer: GameRenderer = in_surface
        self._surface = in_surface._screen
        self.y = y
        self.x = x
        self._color = in_color
        self._circle = is_circle
        self._line = is_line
        # self._shape = pygame.Rect(self.x, self.y, in_size, in_size)

    def draw(self):
        if self._line:
            print(self.x, self.y)
            pygame.draw.line(self._surface, self._color, self.x, self.y, 5)
        elif self._circle:
            pygame.draw.circle(self._surface, self._color, (self.x, self.y), self._size)
        else:
            rect_object = pygame.Rect(self.x, self.y, self._size, self._size)
            pygame.draw.rect(self._surface, self._color, rect_object, border_radius=1)

    def tick(self):
        pass

    def get_shape(self):
        return pygame.Rect(self.x, self.y, self._size, self._size)

    def set_position(self, in_x, in_y):
        self.x = in_x
        self.y = in_y

    def get_position(self):
        return (self.x, self.y)


class Wall(GameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(0, 0, 255)):
        super().__init__(in_surface, x * in_size, y * in_size, in_size, in_color)


class Line(GameObject):
    def __init__(self, in_surface, x, y, in_color=(255, 0, 0)):
        super().__init__(
            in_surface,
            x,
            y,
            in_color,
            is_circle=False,
            is_line=True,
        )


class MovableObject(GameObject):
    def __init__(
        self,
        in_surface,
        x,
        y,
        in_size: int,
        in_color=(255, 0, 0),
        is_circle: bool = False,
    ):
        super().__init__(in_surface, x, y, in_size, in_color, is_circle)
        self.current_direction = Direction.NONE
        self.last_working_direction = Direction.NONE
        self.location_queue = []
        self.next_target = None
        self.image = pygame.image.load("images/ghost.png")

    def get_next_location(self):
        return None if len(self.location_queue) == 0 else self.location_queue.pop(0)

    def set_direction(self, in_direction):
        self.current_direction = in_direction

    def collides_with_wall(self, in_position):
        collision_rect = pygame.Rect(
            in_position[0], in_position[1], self._size, self._size
        )
        collides = False
        walls = self._renderer.get_walls()
        for wall in walls:
            collides = collision_rect.colliderect(wall.get_shape())
            if collides:
                break
        return collides

    def check_collision_in_direction(self, in_direction: Direction):
        desired_position = (1, 1)
        if in_direction == Direction.NONE:
            return False, desired_position
        if in_direction == Direction.UP:
            desired_position = (self.x, self.y - 1)
        elif in_direction == Direction.DOWN:
            desired_position = (self.x, self.y + 1)
        elif in_direction == Direction.LEFT:
            desired_position = (self.x - 1, self.y)
        elif in_direction == Direction.RIGHT:
            desired_position = (self.x + 1, self.y)

        return self.collides_with_wall(desired_position), desired_position

    def automatic_move(self, in_direction: Direction):
        pass

    def tick(self):
        self.reached_target()
        self.automatic_move(self.current_direction)

    def reached_target(self):
        pass

    def draw(self):
        self.image = pygame.transform.scale(self.image, (32, 32))
        self._surface.blit(self.image, self.get_shape())


class Hero(MovableObject):
    def __init__(self, in_surface, in_game_controller, x, y, in_size: int):
        super().__init__(in_surface, x, y, in_size, (255, 255, 0), False)
        self.game_controller = in_game_controller
        self.last_non_colliding_position = (1, 1)
        self.open = pygame.image.load("images/paku.png")
        self.closed = pygame.image.load("images/man.png")
        self.image = self.open
        self.mouth_open = True

    # def tick(self):
    #     # TELEPORT
    #     if self.x < 0:
    #         self.x = self._renderer._width

    #     if self.x > self._renderer._width:
    #         self.x = 0

    #     self.last_non_colliding_position = self.get_position()

    #     if self.check_collision_in_direction(self.current_direction)[0]:
    #         self.automatic_move(self.current_direction)
    #     else:
    #         self.automatic_move(self.current_direction)

    #     if self.collides_with_wall((self.x, self.y)):
    #         self.set_position(
    #             self.last_non_colliding_position[0], self.last_non_colliding_position[1]
    #         )
    #     self.handle_cookie_pickup()
    #     self.handle_ghosts()

    def reached_target(self):
        if (self.x, self.y) == self.next_target:
            self.next_target = self.get_next_location()
        self.current_direction = self.calculate_direction_to_next_target()

    def set_new_path(self, in_path):
        for item in in_path:
            self.location_queue.append(item)
        self.next_target = self.get_next_location()

    def calculate_direction_to_next_target(self) -> Direction:
        if self.next_target is None:
            self.request_path_to_cookie(self)
            return Direction.NONE

        diff_x = self.next_target[0] - self.x
        diff_y = self.next_target[1] - self.y
        if diff_x == 0:
            return Direction.DOWN if diff_y > 0 else Direction.UP
        if diff_y == 0:
            return Direction.LEFT if diff_x < 0 else Direction.RIGHT
        self.request_path_to_cookie(self)
        return Direction.NONE

    def request_path_to_cookie(self, in_hero):
        player_position = translate_screen_to_maze(in_hero.get_position())

        print("Player:", player_position)
        cookie_position = translate_screen_to_maze(
            in_hero._renderer.get_cookie_position()
        )
        print("Cookie:", cookie_position)
        path = in_hero.game_controller.p.get_path_a_star(
            player_position, cookie_position
        )
        print("PATH:", path)
        new_path = [translate_maze_to_screen(item) for item in path]
        in_hero.set_new_path(new_path)

    def automatic_move(self, in_direction: Direction):
        if in_direction == Direction.UP:
            self.set_position(self.x, self.y - 1)
        elif in_direction == Direction.DOWN:
            self.set_position(self.x, self.y + 1)
        elif in_direction == Direction.LEFT:
            self.set_position(self.x - 1, self.y)
        elif in_direction == Direction.RIGHT:
            self.set_position(self.x + 1, self.y)
        self.handle_cookie_pickup()
        self.handle_ghosts()

    # def automatic_move(self, in_direction: Direction):
    #     collision_result = self.check_collision_in_direction(in_direction)

    #     desired_position_collides = collision_result[0]
    #     if not desired_position_collides:
    #         self.last_working_direction = self.current_direction
    #         desired_position = collision_result[1]
    #         self.set_position(desired_position[0], desired_position[1])
    #     else:
    #         self.current_direction = self.last_working_direction

    def handle_cookie_pickup(self):
        collision_rect = pygame.Rect(self.x, self.y, self._size, self._size)
        cookies = self._renderer.get_cookies()
        game_objects = self._renderer.get_game_objects()
        cookie_to_remove = None
        for cookie in cookies:
            collides = collision_rect.colliderect(cookie.get_shape())
            if collides and cookie in game_objects:
                game_objects.remove(cookie)
                self._renderer.add_score(ScoreType.COOKIE)
                cookie_to_remove = cookie

        if cookie_to_remove is not None:
            cookies.remove(cookie_to_remove)

        if len(self._renderer.get_cookies()) == 0:
            self._renderer.set_won()

    def handle_ghosts(self):
        collision_rect = pygame.Rect(self.x, self.y, self._size, self._size)
        ghosts = self._renderer.get_ghosts()
        game_objects = self._renderer.get_game_objects()
        for ghost in ghosts:
            collides = collision_rect.colliderect(ghost.get_shape())
            if collides and ghost in game_objects:
                if not self._renderer.get_won():
                    self._renderer.kill_pacman()

    def draw(self):
        half_size = self._size / 2
        self.image = self.open if self.mouth_open else self.closed
        self.image = pygame.transform.rotate(self.image, self.current_direction.value)
        super(Hero, self).draw()


class Ghost(MovableObject):
    def __init__(
        self,
        in_surface,
        x,
        y,
        in_size: int,
        in_game_controller,
        sprite_path="images/ghost_fright.png",
    ):
        super().__init__(in_surface, x, y, in_size)
        self.game_controller = in_game_controller
        self.sprite_normal = pygame.image.load(sprite_path)

    def reached_target(self):
        if (self.x, self.y) == self.next_target:
            self.next_target = self.get_next_location()
        self.current_direction = self.calculate_direction_to_next_target()

    def set_new_path(self, in_path):
        for item in in_path:
            self.location_queue.append(item)
        self.next_target = self.get_next_location()

    def calculate_direction_to_next_target(self) -> Direction:
        if self.next_target is None:
            if self._renderer.get_current_mode() == GhostBehaviour.CHASE:
                self.request_path_to_player(self)
            else:
                self.game_controller.request_new_random_path(self)
            return Direction.NONE

        diff_x = self.next_target[0] - self.x
        diff_y = self.next_target[1] - self.y
        if diff_x == 0:
            return Direction.DOWN if diff_y > 0 else Direction.UP
        if diff_y == 0:
            return Direction.LEFT if diff_x < 0 else Direction.RIGHT

        if self._renderer.get_current_mode() == GhostBehaviour.CHASE:
            self.request_path_to_player(self)
        else:
            self.game_controller.request_new_random_path(self)
        return Direction.NONE

    def request_path_to_player(self, in_ghost):
        player_position = translate_screen_to_maze(
            in_ghost._renderer.get_hero_position()
        )
        ghost_position = translate_screen_to_maze(in_ghost.get_position())
        # Chasing player mode
        path = self.game_controller.p.get_path_a_star(ghost_position, player_position)
        print("GHOST:", ghost_position)
        print("PATH TO PLAYER:", path)
        new_path = [translate_maze_to_screen(item) for item in path]
        in_ghost.set_new_path(new_path)

    def automatic_move(self, in_direction: Direction):
        if in_direction == Direction.UP:
            self.set_position(self.x, self.y - 1)
        elif in_direction == Direction.DOWN:
            self.set_position(self.x, self.y + 1)
        elif in_direction == Direction.LEFT:
            self.set_position(self.x - 1, self.y)
        elif in_direction == Direction.RIGHT:
            self.set_position(self.x + 1, self.y)

    def draw(self):
        self.image = self.sprite_normal
        super(Ghost, self).draw()


class Cookie(GameObject):
    def __init__(self, in_surface, x, y):
        super().__init__(in_surface, x, y, 4, (255, 255, 0), True)

    def get_position(self):
        return (self.x, self.y)


class GameRenderer:
    def __init__(self, in_width: int, in_height: int):
        pygame.init()
        self._width = in_width
        self._height = in_height
        self._screen = pygame.display.set_mode((in_width, in_height))
        pygame.display.set_caption("Pacman")
        self._clock = pygame.time.Clock()
        self._done = False
        self._won = False
        self._game_objects = []
        self._walls = []
        self._cookies = []
        self._ghosts = []
        self._hero: Hero = None
        self._lives = 3
        self._score = 0
        self._score_cookie_pickup = 10
        self._current_mode = GhostBehaviour.SCATTER  # default
        self._current_level = 1  # default
        self._mode_switch_event = pygame.USEREVENT + 1  # custom event
        self._pakupaku_event = pygame.USEREVENT + 3
        self._modes = [
            (7, 20),
            (7, 20),
            (5, 20),
            (5, 999999),  # 'infinite' chase seconds
        ]
        self._current_phase = 0

    def tick(self, in_fps: int):
        black = (0, 0, 0)

        self.handle_mode_switch()
        pygame.time.set_timer(self._pakupaku_event, 200)  # open close mouth
        while not self._done:
            for game_object in self._game_objects:
                game_object.tick()
                game_object.draw()

            self.display_text(f"[Score: {self._score}]  [Lives: {self._lives}]")

            if self._hero is None:
                self.display_text(
                    "YOU DIED", (self._width / 2 - 256, self._height / 2 - 256), 100
                )
            if self.get_won():
                self.display_text(
                    "YOU WON", (self._width / 2 - 256, self._height / 2 - 256), 100
                )
            pygame.display.flip()
            self._clock.tick(in_fps)
            self._screen.fill(black)
            self._handle_events()

        print("Game over")

    def handle_mode_switch(self):
        if self._current_level == 1:
            self.set_current_mode(GhostBehaviour.NONE)
        elif self._current_level == 2:
            self.set_current_mode(GhostBehaviour.SCATTER)
        elif self._current_level == 4:
            self.set_current_mode(GhostBehaviour.CHASE)

        # current_phase_timings = self._modes[self._current_phase]
        # print(
        #     f"Current phase: {str(self._current_phase)}, current_phase_timings: {str(current_phase_timings)}"
        # )
        # scatter_timing = current_phase_timings[0]
        # chase_timing = current_phase_timings[1]

        # if self._current_mode == GhostBehaviour.CHASE:
        #     self._current_phase += 1
        #     self.set_current_mode(GhostBehaviour.SCATTER)
        # else:
        #     self.set_current_mode(GhostBehaviour.CHASE)

        # used_timing = (
        #     scatter_timing
        #     if self._current_mode == GhostBehaviour.SCATTER
        #     else chase_timing
        # )
        # pygame.time.set_timer(self._mode_switch_event, used_timing * 1000)

    def add_game_object(self, obj: GameObject):
        self._game_objects.append(obj)

    def add_cookie(self, obj: GameObject):
        self._game_objects.append(obj)
        self._cookies.append(obj)

    def add_ghost(self, obj: GameObject):
        self._game_objects.append(obj)
        self._ghosts.append(obj)

    def set_won(self):
        self._won = True

    def get_won(self):
        return self._won

    def add_score(self, in_score: ScoreType):
        self._score += in_score.value

    def get_hero_position(self):
        return self._hero.get_position() if self._hero != None else (1, 1)

    def get_cookie_position(self):
        cookie_position = self.get_hero_position()
        if len(self._cookies) != 0:
            cookie_position = self._cookies[0].get_position()
        return cookie_position

    def set_current_mode(self, in_mode: GhostBehaviour):
        self._current_mode = in_mode

    def set_current_level(self, in_level):
        self._current_level = in_level

    def get_current_mode(self):
        return self._current_mode

    def end_game(self):
        if self._hero in self._game_objects:
            self._game_objects.remove(self._hero)
        self._hero = None

    def kill_pacman(self):
        self._lives -= 1
        self._hero.set_position(32, 32)
        self._hero.next_target = None
        self._hero.location_queue.clear()
        self._hero.set_direction(Direction.NONE)
        if self._lives == 0:
            self.end_game()

    def display_text(self, text, in_position=(32, 0), in_size=30):
        font = pygame.font.SysFont("Arial", in_size)
        text_surface = font.render(text, False, (255, 255, 255))
        self._screen.blit(text_surface, in_position)

    def add_wall(self, obj: Wall):
        self.add_game_object(obj)
        self._walls.append(obj)

    def get_walls(self):
        return self._walls

    def get_cookies(self):
        return self._cookies

    def get_ghosts(self):
        return self._ghosts

    def get_game_objects(self):
        return self._game_objects

    def add_hero(self, in_hero):
        self.add_game_object(in_hero)
        self._hero = in_hero

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True

            if event.type == self._mode_switch_event:
                self.handle_mode_switch()

            if event.type == self._pakupaku_event:
                if self._hero is None:
                    break
                self._hero.mouth_open = not self._hero.mouth_open

        if self._hero is None:
            return

        # Movement

        # pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_UP]:
        #     self._hero.set_direction(Direction.UP)
        # elif pressed[pygame.K_LEFT]:
        #     self._hero.set_direction(Direction.LEFT)
        # elif pressed[pygame.K_DOWN]:
        #     self._hero.set_direction(Direction.DOWN)
        # elif pressed[pygame.K_RIGHT]:
        #     self._hero.set_direction(Direction.RIGHT)
