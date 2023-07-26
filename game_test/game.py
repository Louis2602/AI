import pygame
from utils import (
    Direction,
    ScoreType,
    GhostBehaviour,
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
    ):
        self._size = in_size
        self._renderer: GameRenderer = in_surface
        self._surface = in_surface._screen
        self.y = y
        self.x = x
        self._color = in_color
        self._circle = is_circle
        self._shape = pygame.Rect(self.x, self.y, in_size, in_size)

    def draw(self):
        if self._circle:
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


class Pacman(MovableObject):
    def __init__(self, in_surface, in_game_controller, x, y, in_size: int, pacman_path):
        super().__init__(in_surface, x, y, in_size, (255, 255, 0), False)
        self.game_controller = in_game_controller
        self.last_non_colliding_position = (1, 1)
        self.open = pygame.image.load("images/paku.png")
        self.closed = pygame.image.load("images/man.png")
        self.location_queue = pacman_path
        self.image = self.open
        self.mouth_open = True

    def reached_target(self):
        if (self.x, self.y) == self.next_target:
            self.next_target = self.get_next_location()
        self.current_direction = self.calculate_direction_to_next_target()

    def calculate_direction_to_next_target(self) -> Direction:
        if self.next_target is None:
            self.next_target = self.get_next_location()
            return Direction.NONE

        diff_x = self.next_target[0] - self.x
        diff_y = self.next_target[1] - self.y

        if diff_x == 0:
            return Direction.DOWN if diff_y > 0 else Direction.UP
        if diff_y == 0:
            return Direction.LEFT if diff_x < 0 else Direction.RIGHT
        self.next_target = self.get_next_location()
        return Direction.NONE

    def automatic_move(self, in_direction: Direction):
        # print(in_direction)
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
        super(Pacman, self).draw()


class Ghost(MovableObject):
    def __init__(
        self,
        in_surface,
        x,
        y,
        in_size: int,
        in_game_controller,
        ghost_path,
        sprite_path="images/ghost_fright.png",
    ):
        super().__init__(in_surface, x, y, in_size)
        self.game_controller = in_game_controller
        self.location_queue = ghost_path
        self.sprite_normal = pygame.image.load(sprite_path)

    def reached_target(self):
        if (self.x, self.y) == self.next_target:
            self.next_target = self.get_next_location()
        self.current_direction = self.calculate_direction_to_next_target()

    def calculate_direction_to_next_target(self) -> Direction:
        if self.next_target is None:
            self.next_target = self.get_next_location()
            return Direction.NONE

        diff_x = self.next_target[0] - self.x
        diff_y = self.next_target[1] - self.y
        if diff_x == 0:
            return Direction.DOWN if diff_y > 0 else Direction.UP
        if diff_y == 0:
            return Direction.LEFT if diff_x < 0 else Direction.RIGHT

        self.next_target = self.get_next_location()
        return Direction.NONE

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
        self._hero: Pacman = None
        self._score = 0
        self._score_cookie_pickup = 10
        self._current_mode = GhostBehaviour.NONE  # default
        self._current_level = 1  # default
        self._mode_switch_event = pygame.USEREVENT + 1  # custom event
        self._pakupaku_event = pygame.USEREVENT + 3

    def tick(self, in_fps: int):
        black = (0, 0, 0)

        self.handle_level()
        pygame.time.set_timer(self._pakupaku_event, 200)  # open close mouth
        while not self._done:
            for game_object in self._game_objects:
                game_object.tick()
                game_object.draw()

            self.display_text(f"[Score: {self._score}]")

            if self._hero is None:
                self.display_text(
                    "YOU DIED",
                    (self._width / 2 - self._width / 4, self._height / 2),
                    50,
                )
            if self.get_won():
                self.display_text(
                    "YOU WON", (self._width / 2 - self._width / 4, self._height / 2), 50
                )
            pygame.display.flip()
            self._clock.tick(in_fps)
            self._screen.fill(black)
            self._handle_events()

        print("Game over")

    def handle_level(self):
        if self._current_level == 1:
            self.set_current_mode(GhostBehaviour.NONE)
        elif self._current_level == 2:
            self.set_current_mode(GhostBehaviour.IDLE)
        elif self._current_level == 3:
            self.set_current_mode(GhostBehaviour.SCATTER)
        elif self._current_level == 4:
            self.set_current_mode(GhostBehaviour.CHASE)

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
        self._hero.next_target = None
        self._hero.location_queue.clear()
        self._hero.set_direction(Direction.NONE)
        self.end_game()

    def display_text(self, text, in_position=(32, 0), in_size=25):
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
                self.handle_level()

            if event.type == self._pakupaku_event:
                if self._hero is None:
                    break
                self._hero.mouth_open = not self._hero.mouth_open

        if self._hero is None:
            return
