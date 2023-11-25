import pygame
import sys
from Scenes.NormalMode import NormalMode
import random
from GameObjects.GameObject import Obstacle, Coin

class HardcoreMode(NormalMode):
    def __init__(self, width, height, game_data):
        super().__init__(width, height, game_data)

    def update(self):
        if self.is_up_key_pressed:
            self.player.move("up", 4)
        elif self.is_down_key_pressed:
            self.player.move("down", 4)

        current_time = pygame.time.get_ticks()
        if current_time - self.obstacle_spawn_timer > self.obstacle_spawn_interval:
            should_spawn_coin = random.randint(1, 5) == 1

            if should_spawn_coin:
                coin = Coin('./ThePyGame/Assets/Icons/money.png', (1100, random.randint(130, 470)), (25, 30), 6)
                self.coin_group.add(coin)
            else:
                obstacle_options = [
                    Obstacle('./ThePyGame/Assets/Obstacles/Rocks/2.png', (1100, random.randint(130, 470)), (50, 100), 6),
                    Obstacle('./ThePyGame/Assets/Obstacles/Rocks/3.png', (1100, random.randint(130, 470)), (60, 120), 6),
                ]

                obstacle = random.choice(obstacle_options)
                self.obstacle_group.add(obstacle)

            self.score += 1
            self.obstacle_spawn_timer = current_time

        self.obstacle_group.update()
        self.coin_group.update()

        if pygame.sprite.spritecollide(self.player, self.obstacle_group, False):
            self.game_over_screen()
            return

        coin_collisions = pygame.sprite.spritecollide(self.player, self.coin_group, True)
        for coin in coin_collisions:
            self.game_data.coins += 1
            self.game_data.save()

        self.obstacle_group.update()
        for obstacle in self.obstacle_group:
            obstacle.move()

        self.coin_group.update()
        for coin in self.coin_group:
            coin.move()

    def game_over_screen(self):
        game_over_font = pygame.font.Font(None, 72)
        if self.score > self.game_data.hardcoreHighscore:
            self.game_data.hardcoreHighscore = self.score
            self.game_data.save()
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_text_rect = game_over_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50))

        button_width = 200
        button_height = 50
        button_color = (66, 136, 252)
        button_outline_color = (255, 255, 255)

        restart_button_rect = pygame.Rect(self.window_width // 4 - button_width // 2 + 200, self.window_height // 2 + 20, button_width, button_height)
        back_button_rect = pygame.Rect(2 * self.window_width // 4 - button_width // 2 + 150, self.window_height // 2 + 20, button_width, button_height)

        pygame.draw.rect(self.screen, button_color, restart_button_rect)
        pygame.draw.rect(self.screen, button_outline_color, restart_button_rect, 2)
        pygame.draw.rect(self.screen, button_color, back_button_rect)
        pygame.draw.rect(self.screen, button_outline_color, back_button_rect, 2)

        restart_text = self.font.render("Restart", True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)

        back_text = self.font.render("Back", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button_rect.center)

        self.screen.blit(game_over_text, game_over_text_rect)
        self.screen.blit(restart_text, restart_text_rect)
        self.screen.blit(back_text, back_text_rect)

        pygame.display.flip()
        
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button_rect.collidepoint(event.pos):
                        self.__init__(self.window_width, self.window_height, self.game_data)
                        return

                    elif back_button_rect.collidepoint(event.pos):
                        waiting_for_input = False
                        self.running = False
                        return

            self.clock.tick(60)

    def draw(self):
        self.screen.fill(self.bg_color)

        pygame.draw.rect(self.screen, (105, 151, 219), (self.level_rect_x, self.level_rect_y, self.level_rect_width, self.level_rect_height))

        pygame.draw.rect(self.screen, self.back_button_color, self.back_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button_outline_rect, 2)
        self.screen.blit(self.back_text, self.back_text_rect)

        self.player.draw(self.screen)

        pygame.draw.rect(self.screen, self.panel_color, self.panel_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.panel_outline_rect, 2)

        text_spacing = (self.panel_width - (len([self.coins_text, self.lives_text, self.score_text, self.highscore_text]) - 1) * 50) // 5

        self.screen.blit(self.coins_text, self.coins_text_rect.move(text_spacing - 600, 0))
        self.screen.blit(self.lives_text, self.lives_text_rect.move(text_spacing - 400, 0))
        self.screen.blit(self.score_text, self.score_text_rect.move(text_spacing - 200, 0))
        self.screen.blit(self.highscore_text, self.highscore_text_rect.move(text_spacing, 0))

        score_value_text = self.font_small.render(str(self.score), True, (255, 255, 255))
        coins_value_text = self.font_small.render(str(self.game_data.coins), True, (255, 255, 255))
        lives_value_text = self.font_small.render(str(self.game_data.lives), True, (255, 255, 255))
        highscore_value_text = self.font_small.render(str(self.game_data.hardcoreHighscore), True, (255, 255, 255))

        highscore_text_x = self.highscore_text_rect.move(text_spacing, 0).x + self.highscore_text_rect.width
        self.screen.blit(highscore_value_text, (highscore_text_x + 10, self.highscore_text_rect.y))

        self.screen.blit(score_value_text, self.score_text_rect.move(text_spacing - 200 + 70, 0))
        self.screen.blit(coins_value_text, self.coins_text_rect.move(text_spacing - 600 + 70, 0))
        self.screen.blit(lives_value_text, self.lives_text_rect.move(text_spacing - 400 + 70, 0))

        self.obstacle_group.draw(self.screen) 
        self.coin_group.draw(self.screen)

        pygame.display.flip()