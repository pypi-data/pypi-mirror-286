"""Готовые игры и программы написанные на PyGame!"""
import pygame
import random, pygame_gui

def change_color(name: str = 'Измени цвет фона - FlorestDEV', text: str = 'Нажми!'):
    """Измени цвет фона с помощью кнопки.\nname: наименование окна.\ntext: текст на кнопке."""
    pygame.init()
    pygame.display.set_caption(name)
    window_surface = pygame.display.set_mode((300, 300))
    background = pygame.Surface((300, 300))
    background.fill(pygame.Color('#000000'))

    color_list = [
        pygame.Color('#FF0000'),  # красный
        pygame.Color('#00FF00'),  # зеленый
        pygame.Color('#0000FF'),  # синий
        pygame.Color('#FFFF00'),  # желтый
        pygame.Color('#00FFFF'),  # бирюзовый
        pygame.Color('#FF00FF'),  # пурпурный
        pygame.Color('#FFFFFF')   # белый
    ]

    current_color_index = 0

    button_font = pygame.font.SysFont('Verdana', 15) # используем шрифт Verdana
    button_text_color = pygame.Color("black")
    button_color = pygame.Color("gray")
    button_rect = pygame.Rect(100, 115, 100, 50)
    button_text = button_font.render(text, True, button_text_color)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    current_color_index = (current_color_index + 1) % len(color_list)
                    background.fill(color_list[current_color_index])

            window_surface.blit(background, (0, 0))
            pygame.draw.rect(window_surface, button_color, button_rect)
            button_rect_center = button_text.get_rect(center=button_rect.center)
            window_surface.blit(button_text, button_rect_center)
            pygame.display.update()

def matrix(name: str = 'Матрица - FlorestDEV', text: str = 'Матрица'):
    """Создайте матрицу в Python!\nname: имя окна.\ntext: текст в кнопке."""
    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption(name)
    pygame.init()
    gui_manager = pygame_gui.UIManager(window_size)

    font = pygame.font.SysFont('Consolas', 20)
    text_color = pygame.Color('green')
    text_symbols = ['0', '1']
    text_pos = [(random.randint(0, window_size[0]), 0) for i in range(50)]
    text_speed = [(0, random.randint(1, 5)) for i in range(50)]
    text_surface_list = []

    button_size = (100, 50)
    button_pos = (350, 250)
    button_text = text

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(button_pos, button_size),
        text=button_text,
        manager=gui_manager
    )

    while True:
        time_delta = pygame.time.Clock().tick(60) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                text_surface_list = []
                for i in range(50):
                    text_symbol = random.choice(text_symbols)
                    text_surface = font.render(text_symbol, True, text_color)
                    text_surface_list.append(text_surface)

            gui_manager.process_events(event)

        gui_manager.update(time_delta)

        window.fill(pygame.Color('black'))

        for i in range(50):
            text_pos[i] = (text_pos[i][0], text_pos[i][1] + text_speed[i][1])
            if text_pos[i][1] > window_size[1]:
                text_pos[i] = (random.randint(0, window_size[0]), -20)
            if len(text_surface_list) > i:
                window.blit(text_surface_list[i], text_pos[i])

        gui_manager.draw_ui(window)
        pygame.display.update()



