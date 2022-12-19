import pygame

headless = True

if not headless:
    pygame.init()

height = 80
square_size = 1000 // height
grid_width = 350
grid_height = height * square_size

# Set the width and height of the screen [width, height]
screen_size = (grid_width * 2, grid_height)
if not headless:
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

if not headless:
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Calibri", 25, True, False)


layers = [[0] * 7 for _ in range(10000)]

stuck_max = -1


def occupied(coord):
    return layers[coord[1]][coord[0]] == 1


shapes = ["hor", "diamond", "j", "vert", "square"]


def get_next_shape_type(prev_type):
    next_index = (shapes.index(prev_type) + 1) % len(shapes)

    return shapes[next_index]


shape_height = {"square": 2, "diamond": 3, "hor": 1, "j": 3, "vert": 4}
shape_width = {"square": 2, "diamond": 3, "hor": 4, "j": 3, "vert": 1}


def can_move_shape(shape, movement):
    shape_type = shape["type"]
    print("shape y", shape["y"])
    print("shape_height", shape_height[shape_type])
    if movement[1] == -1 and shape["y"] + 1 == shape_height[shape_type]:
        # We hit bottom
        return False
    if shape["x"] == 0 and movement[0] == -1:
        # We hit left wall
        return False
    if shape["x"] == 7 - shape_width[shape_type] and movement[0] == 1:
        # We hit right wall
        return False
    if any(
        occupied(coord)
        for coord in [(x + movement[0], y + movement[1]) for x, y in get_coords(shape)]
    ):
        return False
    return True


def get_coords(shape):
    top_left = (shape["x"], shape["y"])
    shape_type = shape["type"]

    if shape_type == "square":
        return [
            top_left,
            (top_left[0] + 1, top_left[1]),
            (top_left[0], top_left[1] - 1),
            (top_left[0] + 1, top_left[1] - 1),
        ]
    elif shape_type == "diamond":
        return [
            (top_left[0] + 1, top_left[1]),
            (top_left[0], top_left[1] - 1),
            (top_left[0] + 1, top_left[1] - 1),
            (top_left[0] + 2, top_left[1] - 1),
            (top_left[0] + 1, top_left[1] - 2),
        ]
    elif shape_type == "hor":
        return [
            top_left,
            (top_left[0] + 1, top_left[1]),
            (top_left[0] + 2, top_left[1]),
            (top_left[0] + 3, top_left[1]),
        ]
    elif shape_type == "j":
        return [
            (top_left[0] + 2, top_left[1]),
            (top_left[0] + 2, top_left[1] - 1),
            (top_left[0] + 2, top_left[1] - 2),
            (top_left[0], top_left[1] - 2),
            (top_left[0] + 1, top_left[1] - 2),
            (top_left[0] + 2, top_left[1] - 2),
        ]
    elif shape_type == "vert":
        return [
            (top_left[0], top_left[1]),
            (top_left[0], top_left[1] - 1),
            (top_left[0], top_left[1] - 2),
            (top_left[0], top_left[1] - 3),
        ]


rock_count = 0


def spawn_shape(prev_type="square"):
    global rock_count
    if rock_count == 2022:
        print("Tower height after rock 2022 have stopped: ", stuck_max + 1)
        exit()
    rock_count += 1
    next_type = get_next_shape_type(prev_type)
    return {"x": 2, "y": stuck_max + 3 + shape_height[next_type], "type": next_type}


cur_shape = spawn_shape()

jet_pattern = open("input.txt").read().strip()

jet_index = 0


def get_next_jet():
    global jet_index
    instruction = jet_pattern[jet_index % len(jet_pattern)]
    jet_index += 1

    return -1 if instruction == "<" else 1


def draw_coord(coord, color):
    pygame.draw.rect(
        screen,
        color,
        (
            coord[0] * square_size,
            square_size * (height - coord[1] - 1),
            square_size,
            square_size,
        ),
    )


paused = False
delay = 1000
prev_draw_tick = 0

tick_state = 0


def step_tetris():
    global cur_shape
    global tick_state
    global stuck_max
    if tick_state == 0:
        lateral_movement = get_next_jet()
        print("*** Next step", cur_shape["type"], "***")
        if can_move_shape(cur_shape, (lateral_movement, 0)):
            print("Moving laterally: ", lateral_movement)
            cur_shape["x"] += lateral_movement
        else:
            print("Can't make lateral movement: ", lateral_movement)
    else:
        if can_move_shape(cur_shape, (0, -1)):
            print("Dropping one level")
            cur_shape["y"] -= 1
        else:
            print("Can't move down")
            stuck_max = max(stuck_max, cur_shape["y"])
            # Add the shape to the layers
            for coord in get_coords(cur_shape):
                layers[coord[1]][coord[0]] = 1
            cur_shape = spawn_shape(cur_shape["type"])
    tick_state = 1 - tick_state


step_mode = False
did_step = False

while not done:
    if headless:
        step_tetris()
    else:
        screen.fill((255, 255, 255))

        # Draw the existing blocks
        for layer_index, layer in enumerate(layers):
            for x, v in enumerate(layer):
                if v != 0:
                    draw_coord((x, layer_index), GREEN)
        # Draw the current shape
        for coord in get_coords(cur_shape):
            draw_coord(coord, BLUE)

        # Draw the grid
        for x in range(0, square_size * (len(layers[0])) + 1, square_size):
            pygame.draw.line(screen, BLACK, (x, 0), (x, grid_height))
            for y in range(0, grid_height, square_size):
                pygame.draw.line(
                    screen, BLACK, (0, y), (square_size * (len(layers[0])), y)
                )

        text = font.render("Rock count: " + str(rock_count), True, BLACK)
        screen.blit(text, [grid_width + 20, 5])

        if paused:
            text = font.render("Paused", True, BLACK)
            screen.blit(text, [grid_width + 20, 50])

        pygame.display.flip()

        cur_tick = pygame.time.get_ticks()
        if cur_tick - prev_draw_tick > delay:
            prev_draw_tick = cur_tick
            if not paused:
                if not step_mode or step_mode and did_step:
                    did_step = False
                    step_tetris()

        clock.tick(60)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            done = True
        if keys[pygame.K_p]:
            paused = True
        if keys[pygame.K_LEFT]:
            delay = delay * 1.1
        if keys[pygame.K_RIGHT]:
            delay = delay * 0.9
        if keys[pygame.K_s]:
            step_mode = True
        if keys[pygame.K_SPACE]:
            did_step = True
        if keys[pygame.K_c]:
            paused = False

        pygame.event.pump()
