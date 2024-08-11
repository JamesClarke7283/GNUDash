import random
import pygame
from src.logging import get_logger
from src.config import get_config

logger = get_logger()

class Block:
    """Represents a block in the game world."""

    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize a block."""
        self.rect = pygame.Rect(x, y, width, height)

class SourceCode:
    """Represents a source code collectible in the game world."""

    def __init__(self, x: int, y: int):
        """Initialize a source code collectible."""
        self.rect = pygame.Rect(x, y, get_config("source_code", "width"), get_config("source_code", "height"))

class LevelGenerator:
    """Generates and manages the game level."""

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize the level generator."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.blocks = []
        self.source_codes = []
        self.scroll_speed = get_config("level", "scroll_speed")
        self.floor_height = get_config("level", "floor_height")
        self.hole_chance = get_config("level", "hole_chance")
        self.hole_min_width = get_config("level", "hole_min_width")
        self.hole_max_width = get_config("level", "hole_max_width")
        self.platform_chance = 0.3  # Chance to generate a platform
        self.generate_initial_level()

    def generate_initial_level(self) -> None:
        """Generate the initial level layout."""
        self.generate_floor()
        for _ in range(get_config("level", "min_blocks")):
            self.add_new_platform()
        for _ in range(get_config("level", "min_source_codes")):
            self.add_new_source_code()

    def generate_floor(self) -> None:
        """Generate the floor with occasional holes."""
        x = 0
        while x < self.screen_width:
            if random.random() < self.hole_chance:
                hole_width = random.randint(self.hole_min_width, self.hole_max_width)
                x += hole_width
            else:
                block_width = random.randint(100, 300)
                self.blocks.append(Block(x, self.screen_height - self.floor_height, block_width, self.floor_height))
                x += block_width

    def add_new_platform(self) -> None:
        """Add a new platform to the level."""
        x = self.screen_width
        y = random.randint(self.screen_height // 4, self.screen_height - self.floor_height - 100)
        width = random.randint(get_config("level", "block_min_width"), get_config("level", "block_max_width"))
        height = random.randint(get_config("level", "block_min_height"), get_config("level", "block_max_height"))
        self.blocks.append(Block(x, y, width, height))

    def add_new_source_code(self) -> None:
        """Add a new source code collectible to the level."""
        x = self.screen_width
        y = random.randint(50, self.screen_height - self.floor_height - 50)
        
        # Ensure the source code is not inside a block
        while any(block.rect.collidepoint(x, y) for block in self.blocks):
            y = random.randint(50, self.screen_height - self.floor_height - 50)
        
        self.source_codes.append(SourceCode(x, y))

    def update(self) -> None:
        """Update the level state."""
        self.scroll_level()
        self.remove_offscreen_objects()
        self.add_new_objects()

    def scroll_level(self) -> None:
        """Scroll the level to the left."""
        for block in self.blocks:
            block.rect.x -= self.scroll_speed
        for source_code in self.source_codes:
            source_code.rect.x -= self.scroll_speed

    def remove_offscreen_objects(self) -> None:
        """Remove objects that have scrolled off the screen."""
        self.blocks = [block for block in self.blocks if block.rect.right > 0]
        self.source_codes = [sc for sc in self.source_codes if sc.rect.right > 0]

    def add_new_objects(self) -> None:
        """Add new objects to the level as needed."""
        if self.blocks[-1].rect.right < self.screen_width:
            if random.random() < self.platform_chance:
                self.add_new_platform()
            else:
                self.generate_floor()
        if len(self.source_codes) < get_config("level", "min_source_codes"):
            self.add_new_source_code()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the level objects on the screen."""
        for block in self.blocks:
            pygame.draw.rect(screen, get_config("colors", "block") if block.rect.bottom < self.screen_height else get_config("colors", "floor"), block.rect)
        for source_code in self.source_codes:
            pygame.draw.rect(screen, get_config("colors", "source_code"), source_code.rect)

    def remove_source_code(self, source_code: SourceCode) -> None:
        """Remove a collected source code from the level."""
        self.source_codes.remove(source_code)
        logger.debug("Removed collected source code from the level")