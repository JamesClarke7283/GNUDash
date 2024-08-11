import pygame

class Block:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)

    def collide(self, player_rect: pygame.Rect) -> bool:
        return self.rect.colliderect(player_rect)
