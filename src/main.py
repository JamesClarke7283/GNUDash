import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from src.logging import get_logger
from src.main_menu import MainMenu
from src.game import Game

logger = get_logger()

class GNUDash:
    """Main game class for GNU Dash."""

    def __init__(self, width: int = 800, height: int = 600):
        """Initialize the game."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("GNU Dash")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = MainMenu(self)

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    if isinstance(self.current_scene, Game):
                        self.current_scene.toggle_pause()
                    else:
                        self.running = False
                self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

def main() -> None:
    """Entry point for the game."""
    logger.info("Starting GNU Dash")
    game = GNUDash()
    game.run()
    logger.info("Exiting GNU Dash")

if __name__ == "__main__":
    main()