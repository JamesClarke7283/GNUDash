from src.logging import get_logger
from src.config import get_config

logger = get_logger()

class Player:
    """Core player class for GNU Dash."""

    def __init__(self, x: float = get_config("player", "initial_x"), y: float = get_config("player", "initial_y")):
        """Initialize the player."""
        self.x = x
        self.y = y
        self.width = get_config("player", "width")
        self.height = get_config("player", "height")
        self.speed = get_config("player", "move_speed")
        self.jump_strength = get_config("player", "jump_strength")
        self.freedom = 0
        self.liberty_shields = get_config("player", "initial_liberty_shields")
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.bounce_factor = 0.5  # Bounce factor when hitting a block from below
        self.can_double_jump = False

    def move(self, dx: float, dy: float) -> None:
        """Move the player by the given delta."""
        self.velocity_x = dx * self.speed
        if dy < 0:
            self.jump()

    def jump(self) -> None:
        """Make the player jump."""
        if self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False
            self.can_double_jump = True
        elif self.can_double_jump:
            self.velocity_y = self.jump_strength
            self.can_double_jump = False

    def update(self, gravity: float, blocks: list) -> None:
        """Update the player's state."""
        self.velocity_y += gravity

        # Apply velocity
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.on_ground = False
        self.check_collision(blocks)

        # Apply friction
        self.velocity_x *= 0.9
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0

    def check_collision(self, blocks: list) -> None:
        """Check for collisions with blocks and adjust position."""
        for block in blocks:
            if self.x < block.rect.right and self.x + self.width > block.rect.left and \
               self.y < block.rect.bottom and self.y + self.height > block.rect.top:
                
                # Collision from above
                if self.velocity_y > 0 and self.y + self.height - self.velocity_y <= block.rect.top:
                    self.y = block.rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                    self.can_double_jump = False
                # Collision from below
                elif self.velocity_y < 0 and self.y - self.velocity_y >= block.rect.bottom:
                    self.y = block.rect.bottom
                    self.velocity_y = -self.velocity_y * self.bounce_factor  # Bounce effect
                # Collision from left
                elif self.velocity_x > 0 and self.x + self.width - self.velocity_x <= block.rect.left:
                    self.x = block.rect.left - self.width
                    self.velocity_x = 0
                # Collision from right
                elif self.velocity_x < 0 and self.x - self.velocity_x >= block.rect.right:
                    self.x = block.rect.right
                    self.velocity_x = 0

    def collect_source_code(self) -> None:
        """Collect source code and increase freedom."""
        self.freedom += 1
        logger.info(f"Player collected source code. Freedom: {self.freedom}")

    def lose_shield(self) -> None:
        """Lose a liberty shield."""
        self.liberty_shields -= 1
        logger.info(f"Player lost a shield. Remaining shields: {self.liberty_shields}")

    def teleport(self, new_x: float, new_y: float) -> None:
        """Teleport the player to a new position."""
        self.x = new_x
        self.y = new_y
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.can_double_jump = False
        logger.info(f"Player teleported to x={self.x}, y={self.y}")