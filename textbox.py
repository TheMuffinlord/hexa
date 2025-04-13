import pygame
from constants import *

def debug_box(surface, lines=["none"]):
    text_font = pygame.font.get_default_font()
    text_object = pygame.font.Font(text_font, 18)
    #box_text = text_object.render(text, True, "white")
    #box_text2 = text_object.render(text2, True, "white")
    box_left = int(SCREEN_WIDTH * 0.8)
    box_width = int(SCREEN_WIDTH * 0.2)
    box_top = int(SCREEN_HEIGHT * 0.7)
    box_height = int(SCREEN_HEIGHT * 0.3)
    box = pygame.Rect(box_left, box_top, box_width, box_height)
    pygame.draw.rect(surface, "white", box, 2)
    line_left = box_left + 10
    line_top = box_top + 10
    for line in range(len(lines)):
        box_text = text_object.render(lines[line], True, "white")
        line_top = box_top + ((line + 1) * 20)
        surface.blit(box_text, (line_left, line_top))
    #surface.blit(box_text, (box_left + 10, box_top + 10))
    #surface.blit(box_text2, (box_left + 10, box_top + 30))
