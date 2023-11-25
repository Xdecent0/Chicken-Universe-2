import pygame
import sys
import random
from pygame.locals import KEYDOWN, KEYUP, K_UP, K_DOWN

from GameObjects.GameObject import Player, Obstacle, SmallRocks, Coin

ICON_WIDTH = 25
ICON_HEIGHT = 30

class NormalMode:
    def __init__(self, window_width, window_height, game_data):

        self.window_width = window_width
        self.window_height = window_height
        self.game_data = game_data
        self.game_data.load()
        self.score = 0

        self.coins_icon = pygame.image.load('./Assets/Icons/heart.png')
        self.lives_icon = pygame.image.load('./Assets/Icons/money.png')
        self.score_icon = pygame.image.load('./Assets/Icons/money.png')
        self.highscore_icon = pygame.image.load('./Assets/Icons/money.png')


        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.bg_color = (133, 105, 219)
        self.level_rect_width = 900
        self.level_rect_height = 500
        self.level_rect_x = (self.window_width - self.level_rect_width) // 2
        self.level_rect_y = (self.window_height - self.level_rect_height) // 2 - 50

        self.is_up_key_pressed = False
        self.is_down_key_pressed = False

        self.obstacle_spawn_timer = pygame.time.get_ticks() 
        self.obstacle_spawn_interval = 1000 
        self.obstacle_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        self.back_button_width = 125
        self.back_button_height = 50
        self.back_button_rect = pygame.Rect(20, 20, self.back_button_width, self.back_button_height)
        self.back_button_color = (66, 136, 252)
        self.back_button_outline_rect = pygame.Rect(self.back_button_rect.x - 4, self.back_button_rect.y - 4,
                                                    self.back_button_rect.width + 8, self.back_button_rect.height + 8)
        self.font = pygame.font.Font(None, 32)
        self.back_text = self.font.render("Back", True, (255, 255, 255))
        self.back_text_rect = self.back_text.get_rect(center=self.back_button_rect.center)

        self.player = Player(f'./Assets/Players/{game_data.playerIndex}.png', (400, 200), size=(30, 60), upper_limit=50, lower_limit=500)

        self.panel_width = 894
        self.panel_height = 100
        self.panel_rect = pygame.Rect((self.window_width - self.panel_width) // 2, self.window_height - self.panel_height - 20, self.panel_width, self.panel_height)
        self.panel_color = (66, 136, 252)
        self.panel_outline_rect = pygame.Rect(self.panel_rect.x - 4, self.panel_rect.y - 4,
                                            self.panel_rect.width + 8, self.panel_rect.height + 8)


        icon_spacing = 10
        text_spacing = 50

        start_x = (self.panel_width ) // 2 + self.panel_rect.x

        self.coins_icon_rect = pygame.Rect(start_x, self.panel_rect.centery - ICON_HEIGHT // 2, ICON_WIDTH, ICON_HEIGHT)
        self.lives_icon_rect = pygame.Rect(self.coins_icon_rect.right + icon_spacing, self.panel_rect.centery - ICON_HEIGHT // 2, ICON_WIDTH, ICON_HEIGHT)
        self.score_icon_rect = pygame.Rect(self.lives_icon_rect.right + icon_spacing, self.panel_rect.centery - ICON_HEIGHT // 2, ICON_WIDTH, ICON_HEIGHT)
        self.highscore_icon_rect = pygame.Rect(self.score_icon_rect.right + icon_spacing, self.panel_rect.centery - ICON_HEIGHT // 2, ICON_WIDTH, ICON_HEIGHT)

        self.screen.blit(self.coins_icon, self.coins_icon_rect)
        self.screen.blit(self.lives_icon, self.lives_icon_rect)
        self.screen.blit(self.score_icon, self.score_icon_rect)
        self.screen.blit(self.highscore_icon, self.highscore_icon_rect)

        self.font_small = pygame.font.Font(None, 32)
        self.coins_text = self.font_small.render("Coins:", True, (255, 255, 255))
        self.lives_text = self.font_small.render("Lives:", True, (255, 255, 255))
        self.score_text = self.font_small.render("Score:", True, (255, 255, 255))
        self.highscore_text = self.font_small.render("Highscore:", True, (255, 255, 255))

        text_x = self.coins_icon_rect.right + text_spacing
        text_y = self.panel_rect.centery - self.coins_text.get_height() // 2
        self.coins_text_rect = self.coins_text.get_rect(topleft=(text_x, text_y))
        self.lives_text_rect = self.lives_text.get_rect(topleft=(text_x, text_y))
        self.score_text_rect = self.score_text.get_rect(topleft=(text_x, text_y))
        self.highscore_text_rect = self.highscore_text.get_rect(topleft=(text_x, text_y))
        self.running = True

    def game_over_screen(self):
        game_over_font = pygame.font.Font(None, 72)
        if self.score > self.game_data.normalHighscore:
            self.game_data.normalHighscore = self.score
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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button_rect.collidepoint(event.pos):
                        self.running = False

                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.is_up_key_pressed = True
                    elif event.key == K_DOWN:
                        self.is_down_key_pressed = True

                elif event.type == KEYUP:
                    if event.key == K_UP:
                        self.is_up_key_pressed = False
                    elif event.key == K_DOWN:
                        self.is_down_key_pressed = False


            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def update(self):
        if self.is_up_key_pressed:
            self.player.move("up", 4)
        elif self.is_down_key_pressed:
            self.player.move("down", 4)

        if pygame.sprite.spritecollide(self.player, self.obstacle_group, False):
            self.game_over_screen()
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.obstacle_spawn_timer > self.obstacle_spawn_interval:
            should_spawn_coin = random.randint(1, 5) == 1

            if should_spawn_coin:
                coin = Coin('./Assets/Icons/money.png', (1100, random.randint(130, 470)))
                self.coin_group.add(coin)
            else:
                obstacle_options = [Obstacle(f'./Assets/Obstacles/Planets/{self.game_data.planetIndex}.png', (1100, random.randint(130, 470))),
                                Obstacle(f'./Assets/Obstacles/Rocks/{self.game_data.rockIndex}.png', (1100, random.randint(130, 470)), (30, 70)),
                                SmallRocks(f'./Assets/Obstacles/UnderRocks/{self.game_data.smallRockIndex}.png')]

                obstacle = random.choice(obstacle_options)
                self.obstacle_group.add(obstacle)

            self.score += 1
            self.obstacle_spawn_timer = current_time

        self.obstacle_group.update()
        self.coin_group.update()

        if pygame.sprite.spritecollide(self.player, self.obstacle_group, False):
            print("Game Over!")
            pygame.quit()
            sys.exit()

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
        highscore_value_text = self.font_small.render(str(self.game_data.normalHighscore), True, (255, 255, 255))

        highscore_text_x = self.highscore_text_rect.move(text_spacing, 0).x + self.highscore_text_rect.width
        self.screen.blit(highscore_value_text, (highscore_text_x + 10, self.highscore_text_rect.y))

        self.screen.blit(score_value_text, self.score_text_rect.move(text_spacing - 200 + 70, 0))
        self.screen.blit(coins_value_text, self.coins_text_rect.move(text_spacing - 600 + 70, 0))
        self.screen.blit(lives_value_text, self.lives_text_rect.move(text_spacing - 400 + 70, 0))

        self.obstacle_group.draw(self.screen) 
        self.coin_group.draw(self.screen)

        pygame.display.flip()
