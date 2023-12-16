import pygame
import sys

class InfoMenu:
    def __init__(self, width, height, player_data):
        self.width = width
        self.height = height
        self.player_data = player_data
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_color = (146, 106, 255) 

        button_width = 150
        button_height = 50
        self.back_button_rect = pygame.Rect(10, 10, button_width, button_height)

        self.coins_icon = pygame.image.load('./ThePyGame/Assets/Icons/money.png') 
        self.back_icon = pygame.image.load('./ThePyGame/Assets/Icons/Buttons/return.png') 

        self.font = pygame.font.Font(None, 32)

        self.reset_data_button_rect = pygame.Rect((self.width - button_width * 2) // 2, 100, button_width * 2, button_height)
        self.reset_data_icon = pygame.image.load('./ThePyGame/Assets/Icons/Buttons/again.png')  
        self.reset_data_text = self.font.render("Reset Data", True, (255, 255, 255))

        self.add_coins_button_rect = pygame.Rect((self.width - button_width * 2) // 2, 160, button_width * 2, button_height)
        self.add_coins_icon = pygame.image.load('./ThePyGame/Assets/Icons/money.png')  
        self.add_coins_text = self.font.render("Add Extra Coins", True, (255, 255, 255))

        panel_width = 200
        panel_height = 50
        panel_margin = 20
        self.coins_panel_rect = pygame.Rect(self.width - panel_width - panel_margin, panel_margin, panel_width, panel_height)

        self.icon_size = (25, 30)
        self.icon_left_offset = 10

    def draw_button(self, rect, icon, text):
        button_margin = 10
        pygame.draw.rect(self.screen, (66, 136, 252), rect.move(button_margin, button_margin))
        pygame.draw.rect(self.screen, (255, 255, 255), rect.move(button_margin, button_margin), 2) 

        self.screen.blit(pygame.transform.scale(icon, self.icon_size), (rect.x + self.icon_left_offset + button_margin, rect.centery - self.icon_size[1] // 2 + button_margin))

        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(rect.x + self.icon_left_offset + self.icon_size[0] + 2 * self.icon_left_offset + button_margin + 100, rect.centery + button_margin))
        self.screen.blit(text_surface, text_rect)

    def draw_settings_menu(self):
        self.screen.fill(self.bg_color) 

        button_margin = 10 
        pygame.draw.rect(self.screen, (66, 136, 252), self.back_button_rect.move(button_margin, button_margin))
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button_rect.move(button_margin, button_margin), 2) 

        icon_size = (40, 40)
        icon_left_offset = 20
        text_offset = 30 

        self.screen.blit(pygame.transform.scale(self.back_icon, icon_size), (self.back_button_rect.x + icon_left_offset + button_margin, self.back_button_rect.centery - icon_size[1] // 2 + button_margin))

        text_surface = self.font.render("Back", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.back_button_rect.x + icon_left_offset + icon_size[0] + text_offset + button_margin, self.back_button_rect.centery + button_margin))
        self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, (66, 136, 252), self.coins_panel_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.coins_panel_rect, 2) 

        self.screen.blit(pygame.transform.scale(self.coins_icon, self.icon_size), (self.coins_panel_rect.x + self.icon_left_offset, self.coins_panel_rect.centery - self.icon_size[1] // 2))

        coins_text_font = pygame.font.Font(None, 32)
        coins_text = coins_text_font.render(f"Coins: {self.player_data.coins}", True, (255, 255, 255))


        self.draw_button(self.reset_data_button_rect, self.reset_data_icon, "Reset Data")

        self.draw_button(self.add_coins_button_rect, self.add_coins_icon, "Add Extra Coins")

        text_rect = coins_text.get_rect(left=self.coins_panel_rect.x + self.icon_size[0] + 2 * self.icon_left_offset, centery=self.coins_panel_rect.centery)
        self.screen.blit(coins_text, text_rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button_rect.collidepoint(event.pos):
                    from Scenes.MainMenu import MainMenu
                    main_menu = MainMenu(self.width, self.height, self.player_data)
                    main_menu.run()

                elif self.reset_data_button_rect.collidepoint(event.pos):
                    self.handle_reset_data_click()
                elif self.add_coins_button_rect.collidepoint(event.pos):
                    self.handle_add_coins_click()


    def run(self):
        while True:
            self.handle_events()
            self.draw_settings_menu()

    def handle_reset_data_click(self):
        self.player_data.reset()

        coins_text_font = pygame.font.Font(None, 32)
        coins_text = coins_text_font.render(f"Coins: {self.player_data.coins}", True, (255, 255, 255))
        text_rect = coins_text.get_rect(left=self.coins_panel_rect.x + self.icon_size[0] + 2 * self.icon_left_offset,
                                        centery=self.coins_panel_rect.centery)
        self.screen.blit(coins_text, text_rect)

        self.player_data.save()

        pygame.display.flip()

    def handle_add_coins_click(self):
        self.player_data.coins += 50

        coins_text_font = pygame.font.Font(None, 32)
        coins_text = coins_text_font.render(f"Coins: {self.player_data.coins}", True, (255, 255, 255))
        text_rect = coins_text.get_rect(left=self.coins_panel_rect.x + self.icon_size[0] + 2 * self.icon_left_offset,
                                        centery=self.coins_panel_rect.centery - 2)
        self.screen.blit(coins_text, text_rect)

        self.player_data.save()

        pygame.display.flip()

