import pygame
from src.config import get_config

class SourceCode:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, get_config("source_code", "width"), get_config("source_code", "height"))

    def collide(self, player_rect: pygame.Rect) -> bool:
        return self.rect.colliderect(player_rect)