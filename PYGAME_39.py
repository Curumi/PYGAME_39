import pygame as pg
from random import choice
from all_colors import COLORS  # Ensure this includes at least 20+ distinct colors

pg.init()

# Setup
size = (1280, 720)
screen = pg.display.set_mode(size)
BACKGROUND = (255, 255, 255)
screen.fill(BACKGROUND)

# Canvas and palette setup
canvas = pg.Surface(screen.get_size())
canvas.fill(BACKGROUND)

# Color palette setup
color_size = 50
palette_rect = pg.Rect(10, 10, color_size * 18, color_size)
palette = pg.Surface(palette_rect.size)
palette.fill(BACKGROUND)

BORDER_COLOR = (0, 0, 0)
CUR_INDEX = 0
brush_color = COLORS[CUR_INDEX]
brush_width = 5
dragging_palette = False

# Rectangle drawing variables
rectangles = []
RECTANGLE_COLOR = (255, 0, 0)
top_left = (0, 0)
current_size = (0, 0)
dragging_rect = False

# Clock setup
FPS = 60
clock = pg.time.Clock()

# Draw color palette
def draw_palette():
    palette.fill(BACKGROUND)
    for i in range(18):
        color_rect = pg.Rect(i * color_size, 0, color_size, color_size)
        pg.draw.rect(palette, COLORS[i], color_rect)

    bonder_rect = pg.Rect(CUR_INDEX * color_size, 0, color_size, color_size)
    pg.draw.rect(palette, BORDER_COLOR, bonder_rect, width=3)
    screen.blit(palette, palette_rect.topleft)

# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                rectangles = [(rect, color, True) for rect, color, filled in rectangles]

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if palette_rect.collidepoint(event.pos):
                    selected_color_index = (event.pos[0] - palette_rect.left) // color_size
                    if 0 <= selected_color_index < len(COLORS):
                        CUR_INDEX = selected_color_index
                        brush_color = COLORS[CUR_INDEX]
                else:
                    top_left = event.pos
                    current_size = 0, 0
                    dragging_rect = True
            elif event.button == 3:  # Right click
                dragging_palette = True
                offset = (event.pos[0] - palette_rect.left, event.pos[1] - palette_rect.top)

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and dragging_rect:
                right_bottom = event.pos
                current_size = (right_bottom[0] - top_left[0], right_bottom[1] - top_left[1])
                rect = pg.Rect(top_left, current_size)
                rectangles.append((rect, brush_color, False))
                dragging_rect = False
            elif event.button == 3:
                dragging_palette = False

        elif event.type == pg.MOUSEMOTION:
            if dragging_rect:
                right_bottom = event.pos
                current_size = (right_bottom[0] - top_left[0], right_bottom[1] - top_left[1])
            elif dragging_palette:
                mouse_pos = event.pos
                new_pos = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
                palette_rect.topleft = new_pos

    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed()

    if mouse_pressed[0] and not palette_rect.collidepoint(mouse_pos) and not dragging_rect:
        pg.draw.circle(canvas, brush_color, mouse_pos, brush_width)

    # Redraw
    screen.fill(BACKGROUND)
    screen.blit(canvas, (0, 0))
    if dragging_rect:
        pg.draw.rect(screen, RECTANGLE_COLOR, (top_left, current_size), 1)
    for rect, color, filled in rectangles:
        if filled:
            pg.draw.rect(screen, color, rect)
        else:
            pg.draw.rect(screen, color, rect, 1)
    draw_palette()
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
