import pygame
import sys
from Scenes.NormalMode import NormalMode
import random
from GameObjects.GameObject import Obstacle, Egg

ICON_WIDTH = 25
ICON_HEIGHT = 30

class SecretMode(NormalMode):
    def __init__(self, width, height, game_data):
        super().__init__(width, height, game_data)
        self.effect = 1
        self.effect_icon = pygame.image.load(f'./ThePyGame/Assets/Icons/Effects/{self.effect}.png')
        self.effect_timer = 0
        self.effect_speed = 4
        self.effect_inversion = False

    def update(self):
        if self.is_up_key_pressed:
            self.player.move("up", self.effect_speed, self.effect_inversion)
        elif self.is_down_key_pressed:
            self.player.move("down", self.effect_speed, self.effect_inversion)
        elif self.is_left_key_pressed:  
            self.player.move("left", self.effect_speed, self.effect_inversion)
        elif self.is_right_key_pressed:
            self.player.move("right", self.effect_speed, self.effect_inversion)

        current_time = pygame.time.get_ticks()
        if current_time - self.obstacle_spawn_timer > self.obstacle_spawn_interval:
            should_spawn_coin = random.randint(1, 6) == 1
            self.score += 1
            if should_spawn_coin:
                coin = Egg('./ThePyGame/Assets/Icons/Effects/egg.png', (1100, random.randint(130, 470)), (20, 20), 6)
                self.coin_group.add(coin)
            else:
                obstacle = Obstacle(f'./ThePyGame/Assets/Obstacles/Rocks/{self.game_data.rockIndex}.png', (1100, random.randint(130, 485)), (70, 150), 6)
                self.obstacle_group.add(obstacle)

            
            self.obstacle_spawn_timer = current_time
            
        self.update_effects()
        self.obstacle_group.update()
        self.coin_group.update()

        if pygame.sprite.spritecollide(self.player, self.obstacle_group, False):
            self.game_over_screen()
            return

        coin_collisions = pygame.sprite.spritecollide(self.player, self.coin_group, True)
        for coin in coin_collisions:
                self.handle_coin_collected()
                self.game_data.coins += 1
                self.game_data.save()
                

        self.obstacle_group.update()
        for obstacle in self.obstacle_group:
            obstacle.move()

        self.coin_group.update()
        for coin in self.coin_group:
            coin.move()

    def handle_coin_collected(self):
        self.effect = random.randint(2, 4)
        self.effect_icon = pygame.image.load(f'./ThePyGame/Assets/Icons/Effects/{self.effect}.png')
        self.effect_timer = 5000 

    def update_effects(self):
        if self.effect_timer > 0:
            if self.effect == 2:
                self.effect_inversion = True
            elif self.effect == 3:
                self.effect_speed = 2.5
            elif self.effect == 4:
                self.effect_speed = 5

            self.effect_timer -= self.clock.get_time()
        else:
            self.effect = 1
            self.effect_speed = 4
            self.effect_inversion = False
            self.effect_icon = pygame.image.load(f'./ThePyGame/Assets/Icons/Effects/{self.effect}.png') 
            self.lives =+ 1

    def game_over_screen(self):
        game_over_font = pygame.font.Font(None, 72)
        if self.score > self.game_data.secretHighscore:
            self.game_data.secretHighscore = self.score
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

        pygame.draw.rect(self.screen, self.back_button_color, self.back_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button_outline_rect, 2)
        self.screen.blit(self.back_text, self.back_text_rect)

        text_spacing = (self.panel_width - (len([self.coins_text, self.lives_text, self.score_text, self.highscore_text]) - 1) * 50) // 5

        icon_position = (self.back_button_rect.x + 25, self.back_button_rect.y + self.back_button_rect.height + 20)
        scaled_icon = pygame.transform.scale(self.effect_icon, (70, 70))
        self.screen.blit(scaled_icon, icon_position)

        self.screen.blit(self.coins_text, self.coins_text_rect.move(text_spacing - 600, 0))
        self.screen.blit(self.lives_text, self.lives_text_rect.move(text_spacing - 400, 0))
        self.screen.blit(self.score_text, self.score_text_rect.move(text_spacing - 200, 0))
        self.screen.blit(self.highscore_text, self.highscore_text_rect.move(text_spacing, 0))

        score_value_text = self.font_small.render(str(self.score), True, (255, 255, 255))
        coins_value_text = self.font_small.render(str(self.game_data.coins), True, (255, 255, 255))
        lives_value_text = self.font_small.render(str(self.game_data.lives), True, (255, 255, 255))
        highscore_value_text = self.font_small.render(str(self.game_data.secretHighscore), True, (255, 255, 255))

        highscore_text_x = self.highscore_text_rect.move(text_spacing, 0).x + self.highscore_text_rect.width
        self.screen.blit(highscore_value_text, (highscore_text_x + 10, self.highscore_text_rect.y))

        self.screen.blit(score_value_text, self.score_text_rect.move(text_spacing - 200 + 70, 0))
        self.screen.blit(coins_value_text, self.coins_text_rect.move(text_spacing - 600 + 70, 0))
        self.screen.blit(lives_value_text, self.lives_text_rect.move(text_spacing - 400 + 70, 0))

        self.obstacle_group.draw(self.screen) 
        self.coin_group.draw(self.screen)

        pygame.display.flip()
