import pygame
from src.core.player import Player
from src.config import get_config

class PlayerComponent:
    """Pygame component for rendering the player."""

    def __init__(self, player: Player):
        """Initialize the player component."""
        self.player = player

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player on the screen."""
        rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        if self.player.visible:
            pygame.draw.rect(screen, get_config("colors", "player"), rect)

    def update_position(self) -> None:
        """Update the player's position based on the core player object."""
        self.rect.x = self.player.x
        self.rect.y = self.player.y