import random
import pygame
from src.logging import get_logger
from src.config import get_config
from src.core.blocks import Block
from src.core.source_code import SourceCode
from .platform_generator import generate_platform, generate_stepping_stones

logger = get_logger()

class LevelGenerator:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.blocks = []
        self.source_codes = []
        self.scroll_speed = get_config("level", "scroll_speed")
        self.floor_height = get_config("level", "floor_height")
        self.hole_chance = get_config("level", "hole_chance")
        self.hole_min_width = get_config("level", "hole_min_width")
        self.hole_max_width = get_config("level", "hole_max_width")
        self.platform_chance = get_config("level", "platform_chance")
        self.min_platform_height = get_config("level", "min_platform_height")
        self.max_platform_height = get_config("level", "max_platform_height")
        self.max_jump_distance = get_config("level", "max_jump_distance")
        self.last_platform_end = 0
        self.generate_initial_level()

    def generate_initial_level(self) -> None:
        self.generate_floor(0, self.screen_width * 2)
        for _ in range(get_config("level", "min_blocks")):
            self.add_new_platform()
        for _ in range(get_config("level", "min_source_codes")):
            self.add_new_source_code()

    def generate_floor(self, start_x: int, end_x: int) -> None:
        x = start_x
        while x < end_x:
            if random.random() < self.hole_chance:
                hole_width = random.randint(self.hole_min_width, min(self.hole_max_width, self.max_jump_distance // 2))
                x += hole_width
            else:
                block_width = random.randint(100, 300)
                self.blocks.append(Block(x, self.screen_height - self.floor_height, block_width, self.floor_height))
                x += block_width
        self.last_platform_end = max(self.last_platform_end, end_x)

    def add_new_platform(self) -> None:
        x, y, width, height = generate_platform(self.screen_width, self.last_platform_end, self.min_platform_height, self.max_platform_height, self.max_jump_distance)
        self.blocks.append(Block(x, y, width, height))
        self.last_platform_end = x + width

        # Add stepping stones
        new_stones = generate_stepping_stones(x, y, width, self.max_jump_distance)
        self.blocks.extend(new_stones)
        if new_stones:
            self.last_platform_end = max(self.last_platform_end, new_stones[-1].rect.right)

        # Add source code near the platform
        if random.random() < 0.5:
            self.add_new_source_code(x, y, width)

    def add_new_source_code(self, platform_x: int = None, platform_y: int = None, platform_width: int = None) -> None:
        if platform_x is None:
            x = max(self.screen_width, self.last_platform_end + random.randint(50, 100))
            y = random.randint(50, self.screen_height - self.floor_height - 50)
        else:
            x = platform_x + random.randint(0, platform_width)
            y = platform_y - random.randint(50, 100)

        if not any(block.rect.collidepoint(x, y) for block in self.blocks):
            self.source_codes.append(SourceCode(x, y))
        else:
            # If the position is occupied, try to place it above the highest nearby platform
            nearby_platforms = [b for b in self.blocks if abs(b.rect.centerx - x) < self.max_jump_distance]
            if nearby_platforms:
                highest_platform = min(nearby_platforms, key=lambda b: b.rect.top)
                y = highest_platform.rect.top - get_config("source_code", "height") - 10
                self.source_codes.append(SourceCode(x, y))

    def update(self) -> None:
        self.scroll_level()
        self.remove_offscreen_objects()
        self.add_new_objects()

    def scroll_level(self) -> None:
        for block in self.blocks:
            block.rect.x -= self.scroll_speed
        for source_code in self.source_codes:
            source_code.rect.x -= self.scroll_speed
        self.last_platform_end -= self.scroll_speed

    def remove_offscreen_objects(self) -> None:
        self.blocks = [block for block in self.blocks if block.rect.right > 0]
        self.source_codes = [sc for sc in self.source_codes if sc.rect.right > 0]

    def add_new_objects(self) -> None:
        while self.last_platform_end < self.screen_width * 1.5:
            if random.random() < self.platform_chance:
                self.add_new_platform()
            else:
                self.generate_floor(self.last_platform_end, self.last_platform_end + self.screen_width)
        while len(self.source_codes) < get_config("level", "min_source_codes"):
            self.add_new_source_code()

    def draw(self, screen: pygame.Surface) -> None:
        for block in self.blocks:
            pygame.draw.rect(screen, get_config("colors", "block") if block.rect.bottom < self.screen_height else get_config("colors", "floor"), block.rect)
        for source_code in self.source_codes:
            pygame.draw.rect(screen, get_config("colors", "source_code"), source_code.rect)
            
    def remove_source_code(self, source_code: SourceCode) -> None:
        self.source_codes.remove(source_code)
        logger.debug("Removed collected source code from the level")