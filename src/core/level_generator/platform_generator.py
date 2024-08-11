# ./src/core/level_generator/platform_generator.py

import random
from src.config import get_config
from src.core.blocks import Block

def generate_platform(screen_width: int, last_platform_end: int, min_height: int, max_height: int, max_jump_distance: int) -> tuple:
    x = max(screen_width, last_platform_end + random.randint(max_jump_distance // 4, max_jump_distance // 2))
    y = random.randint(min_height, max_height)
    width = random.randint(get_config("level", "block_min_width"), get_config("level", "block_max_width"))
    height = random.randint(get_config("level", "block_min_height"), get_config("level", "block_max_height"))
    return x, y, width, height

def generate_stepping_stones(start_x: int, start_y: int, main_platform_width: int, max_jump_distance: int) -> list:
    stones = []
    num_stones = random.randint(2, 4)
    stone_width = 30
    stone_height = 10
    total_stepping_width = (num_stones * stone_width) + ((num_stones - 1) * max_jump_distance // 4)

    if random.choice([True, False]):  # Stepping stones before the platform
        x = start_x - total_stepping_width
    else:  # Stepping stones after the platform
        x = start_x + main_platform_width

    for _ in range(num_stones):
        y = start_y + random.randint(-30, 30)
        stones.append(Block(x, y, stone_width, stone_height))
        x += stone_width + max_jump_distance // 4

    return stones