import pygame
from pygame.locals import MOUSEBUTTONDOWN
from src.logging import get_logger

logger = get_logger()

class MainMenu:
    """Main menu scene for GNU Dash."""

    def __init__(self, game):
        """Initialize the main menu."""
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.play_button = pygame.Rect(300, 250, 200, 50)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events for the main menu."""
        if event.type == MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                logger.info("Starting new game")
                from src.game import Game  # Import here to avoid circular import
                self.game.current_scene = Game(self.game)

    def update(self) -> None:
        """Update the main menu."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the main menu."""
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), self.play_button)
        text = self.font.render("Play", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.play_button.center)
        screen.blit(text, text_rect)