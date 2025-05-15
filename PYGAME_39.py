import pygame as pg
from random import choice
from all_colors import COLORS

pg.init()

size = (1280, 720)
screen = pg.display.set_mode(size)
BACKGROUND = (255, 255, 255)
screen.fill(BACKGROUND)

# Настройки кисти
brush_color = (0, 0, 0)
brush_width = 5
CUR_INDEX = 0

# Холст
canvas = pg.Surface(screen.get_size())
canvas.fill(BACKGROUND)

# Палитра
palette_size = 50
palette_rect = pg.Rect(10, 10, palette_size * 18, palette_size)
palette = pg.Surface(palette_rect.size)

def draw_palette():
    palette.fill(BACKGROUND)
    for i in range(18):
        color_rect = pg.Rect(i * palette_size, 0, palette_size, palette_size)
        pg.draw.rect(palette, COLORS[i], color_rect)
    border_rect = pg.Rect(CUR_INDEX * palette_size, 0, palette_size, palette_size)
    pg.draw.rect(palette, (0, 0, 0), border_rect, width=3)
    screen.blit(palette, palette_rect.topleft)

# Прямоугольники
rectangles = []
RECTANGLE_COLOR = (255, 0, 0)
top_left = (0, 0)
current_size = (0, 0)
dragging_rect = False

# Палитра перемещение
dragging_palette = False

FPS = 60
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if palette_rect.collidepoint(event.pos):
                    selected_index = (event.pos[0] - palette_rect.left) // palette_size
                    if 0 <= selected_index < len(COLORS):
                        CUR_INDEX = selected_index
                        brush_color = COLORS[CUR_INDEX]
                else:
                    pass  # Рисуем в основном цикле

            elif event.button == 3:
                if palette_rect.collidepoint(event.pos):
                    dragging_palette = True
                    offset = (event.pos[0] - palette_rect.left, event.pos[1] - palette_rect.top)
                else:
                    top_left = event.pos
                    current_size = (0, 0)
                    dragging_rect = True

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 3:
                if dragging_palette:
                    dragging_palette = False
                elif dragging_rect:
                    right_bottom = event.pos
                    width = right_bottom[0] - top_left[0]
                    height = right_bottom[1] - top_left[1]
                    if abs(width) > 5 and abs(height) > 5:
                        rect = pg.Rect(top_left, (width, height))
                        rectangles.append((rect, brush_color, False))
                    dragging_rect = False

    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed()

    if dragging_palette:
        new_pos = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
        palette_rect.topleft = new_pos

    # Рисование кистью
    if mouse_pressed[0] and not palette_rect.collidepoint(mouse_pos):
        pg.draw.circle(canvas, brush_color, mouse_pos, brush_width)

    # Обновление прямоугольника при перетаскивании
    if dragging_rect:
        right_bottom = mouse_pos
        current_size = (right_bottom[0] - top_left[0], right_bottom[1] - top_left[1])

    screen.fill(BACKGROUND)
    screen.blit(canvas, (0, 0))

    # Рисуем прямоугольник в процессе перетаскивания
    if dragging_rect:
        pg.draw.rect(screen, RECTANGLE_COLOR, (top_left, current_size), 1)

    # Отображение сохра
