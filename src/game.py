# ./src/game.py

import pygame
from pygame.locals import (
    K_LEFT, K_RIGHT, K_UP, K_DOWN,
    K_a, K_d, K_w, K_s,
    K_SPACE, K_ESCAPE,
    KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP
)
from src.logging import get_logger
from src.core.player import Player
from src.components.player import PlayerComponent
from src.core.level_generator import LevelGenerator
from src.config import get_config

logger = get_logger()

class Game:
    def __init__(self, game):
        self.game = game
        self.player = Player()
        self.player_component = PlayerComponent(self.player)
        self.level_generator = LevelGenerator(game.width, game.height)
        self.font = pygame.font.Font(None, get_config("fonts", "hud_size"))
        self.paused = False
        self.game_over = False
        self.pause_menu = PauseMenu(self)
        self.move_left = False
        self.move_right = False
        self.jump_pressed = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.game_over:
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                self.game.current_scene = Game(self.game)
            return

        if self.paused:
            self.pause_menu.handle_event(event)
        else:
            if event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a):
                    self.move_left = True
                elif event.key in (K_RIGHT, K_d):
                    self.move_right = True
                elif event.key in (K_UP, K_w, K_SPACE):
                    self.jump_pressed = True
                    self.player.start_jump()
                elif event.key == K_ESCAPE:
                    self.toggle_pause()
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    self.move_left = False
                elif event.key in (K_RIGHT, K_d):
                    self.move_right = False
                elif event.key in (K_UP, K_w, K_SPACE):
                    self.jump_pressed = False
                    self.player.end_jump()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.jump_pressed = True
                    self.player.start_jump()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.jump_pressed = False
                    self.player.end_jump()

    def update(self) -> None:
        if self.game_over or self.paused:
            return

        dx = 0
        if self.move_left:
            dx -= 1
        if self.move_right:
            dx += 1
        
        self.player.move(dx, -1 if self.jump_pressed else 0)
        self.player.update(get_config("game", "gravity"), self.level_generator.blocks)
        self.level_generator.update()
        self.check_collisions()
        self.keep_player_on_screen()

        if self.player.liberty_shields <= 0:
            self.game_over = True
            logger.info(f"Game Over. Final Freedom Score: {self.player.freedom}")

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(get_config("colors", "background"))
        self.level_generator.draw(screen)
        self.player_component.draw(screen)
        self.draw_hud(screen)

        if self.paused:
            self.pause_menu.draw(screen)
        elif self.game_over:
            self.draw_game_over(screen)

    def draw_hud(self, screen: pygame.Surface) -> None:
        freedom_text = self.font.render(f"Freedom: {self.player.freedom}", True, get_config("colors", "text"))
        shields_text = self.font.render(f"Liberty Shields: {self.player.liberty_shields}", True, get_config("colors", "text"))
        screen.blit(freedom_text, (10, 10))
        screen.blit(shields_text, (10, 40))

    def draw_game_over(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        game_over_font = pygame.font.Font(None, get_config("fonts", "game_over_size"))
        game_over_text = game_over_font.render("GAME OVER", True, get_config("colors", "text"))
        score_text = self.font.render(f"Final Freedom Score: {self.player.freedom}", True, get_config("colors", "text"))
        restart_text = self.font.render("Press any key to restart", True, get_config("colors", "text"))

        screen.blit(game_over_text, game_over_text.get_rect(center=(self.game.width // 2, self.game.height // 2 - 50)))
        screen.blit(score_text, score_text.get_rect(center=(self.game.width // 2, self.game.height // 2 + 20)))
        screen.blit(restart_text, restart_text.get_rect(center=(self.game.width // 2, self.game.height // 2 + 70)))

    def check_collisions(self) -> None:
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for source_code in self.level_generator.source_codes:
            if player_rect.colliderect(source_code.rect):
                self.player.collect_source_code()
                self.level_generator.remove_source_code(source_code)
                logger.info(f"Player collected source code. Freedom: {self.player.freedom}")

        if self.player.y > self.game.height:
            self.player.lose_shield()
            self.teleport_player_to_safe_area()
            logger.info("Player fell off the screen")

    def teleport_player_to_safe_area(self) -> None:
        safe_y = self.find_safe_y_position()
        self.player.teleport(get_config("player", "initial_x"), safe_y)

    def find_safe_y_position(self) -> float:
        player_height = self.player.height
        screen_height = get_config("game", "screen_height")
        
        for y in range(0, screen_height - player_height, player_height):
            rect = pygame.Rect(get_config("player", "initial_x"), y, self.player.width, player_height)
            if not any(block.rect.colliderect(rect) for block in self.level_generator.blocks):
                return y
        
        # If no safe position is found, return the top of the screen
        return 0

    def keep_player_on_screen(self) -> None:
        if self.player.x < 0:
            self.player.x = 0
        elif self.player.x > self.game.width - self.player.width:
            self.player.x = self.game.width - self.player.width
        if self.player.y < 0:
            self.player.y = 0
            self.player.velocity_y = 0

    def toggle_pause(self) -> None:
        self.paused = not self.paused
        logger.info(f"Game {'paused' if self.paused else 'resumed'}")

class PauseMenu:
    def __init__(self, game_scene):
        self.game_scene = game_scene
        self.font = pygame.font.Font(None, get_config("fonts", "main_size"))
        self.continue_button = pygame.Rect(300, 200, 200, 50)
        self.exit_button = pygame.Rect(300, 300, 200, 50)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == MOUSEBUTTONDOWN:
            if self.continue_button.collidepoint(event.pos):
                self.game_scene.toggle_pause()
            elif self.exit_button.collidepoint(event.pos):
                self.game_scene.game.running = False

    def draw(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (0, 255, 0), self.continue_button)
        pygame.draw.rect(screen, (255, 0, 0), self.exit_button)

        continue_text = self.font.render("Continue", True, get_config("colors", "text"))
        exit_text = self.font.render("Exit", True, get_config("colors", "text"))

        screen.blit(continue_text, continue_text.get_rect(center=self.continue_button.center))
        screen.blit(exit_text, exit_text.get_rect(center=self.exit_button.center))