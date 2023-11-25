import pygame
import sys
import random

class ShopScene:
    def __init__(self, width, height, player_data):
        self.width = width
        self.height = height
        self.player_data = player_data
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg_color = (66, 77, 252)  # Новый цвет фона #6AABD9

        self.back_button_rect = pygame.Rect(10, 10, 150, 50) 

        self.coins_icon = pygame.image.load('./Assets/Icons/money.png')

        self.back_icon = pygame.image.load('./Assets/Icons/Buttons/return.png')

        self.font = pygame.font.Font(None, 32)

        self.buy_buttons = [
            {"name": "Random Planet", "price": 20, "icon": pygame.image.load('./Assets/Obstacles/Planets/1.png')},
            {"name": "Random Rock", "price": 15, "icon": pygame.image.load('./Assets/Obstacles/Rocks/1.png')},
            {"name": "Random Skin", "price": 25, "icon": pygame.image.load('./Assets/Players/1.png')},
            {"name": "Random Small Rock", "price": 10, "icon": pygame.image.load('./Assets/Obstacles/UnderRocks/1.png')}
        ]

        panel_width = 200
        panel_height = 50
        panel_margin = 20
        self.coins_panel_rect = pygame.Rect(self.width - panel_width - panel_margin, panel_margin, panel_width, panel_height)

        self.icon_size = (40, 40)
        self.icon_left_offset = 10

    def draw_shop_scene(self):
        self.screen.fill(self.bg_color)

        button_margin = 10
        pygame.draw.rect(self.screen, (66, 136, 252), self.back_button_rect.move(button_margin, button_margin))
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button_rect.move(button_margin, button_margin), 2)

        icon_size = (40, 40)
        icon_left_offset = 20
        text_offset = 30

        self.screen.blit(pygame.transform.scale(self.back_icon, icon_size),
                         (self.back_button_rect.x + icon_left_offset + button_margin,
                          self.back_button_rect.centery - icon_size[1] // 2 + button_margin))

        text_surface = self.font.render("Back", True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(self.back_button_rect.x + icon_left_offset + icon_size[0] + text_offset + button_margin,
                    self.back_button_rect.centery + button_margin))
        self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, (66, 136, 252), self.coins_panel_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.coins_panel_rect, 2)

        self.screen.blit(pygame.transform.scale(self.coins_icon, (25, 30)),
                         (self.coins_panel_rect.x + self.icon_left_offset,
                          self.coins_panel_rect.centery - self.icon_size[1] // 2 +2))

        coins_text_font = pygame.font.Font(None, 32)
        coins_text = coins_text_font.render(f"Coins: {self.player_data.coins}", True, (255, 255, 255))

        text_rect = coins_text.get_rect(
            left=self.coins_panel_rect.x + self.icon_size[0] + 2 * self.icon_left_offset,
            centery=self.coins_panel_rect.centery)
        self.screen.blit(coins_text, text_rect)
        button_width = 600  
        button_height = 70

        for i, button in enumerate(self.buy_buttons):
            button_rect = pygame.Rect((self.width - button_width) // 2, 150 + i * 90, button_width, button_height)
            pygame.draw.rect(self.screen, (66, 136, 252), button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
  
            icon_rect = pygame.Rect(button_rect.x + 10, button_rect.y + 15, self.icon_size[0], self.icon_size[1])
            self.screen.blit(pygame.transform.scale(button["icon"], self.icon_size), icon_rect)
            text_surface = self.font.render(f"Swtich to {button['name']} ({button['price']} coins)", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(button_rect.centerx, button_rect.centery))
            self.screen.blit(text_surface, text_rect)

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

                for i, button in enumerate(self.buy_buttons):
                    button_rect = pygame.Rect((self.width - 300) // 2, 150 + i * 90, 300, 70)
                    if button_rect.collidepoint(event.pos):
                        self.handle_buy_button_click(button["name"], button["price"])

    def handle_buy_button_click(self, item_name, item_price):
        if self.player_data.coins >= item_price:
            self.player_data.coins -= item_price
            print(f"You've bought {item_name} for {item_price} coins!")

            if item_name == "Random Planet":
                new_index = self.generate_random_index(self.player_data.playerIndex, 1, 6)
                self.player_data.planetIndex = new_index
            elif item_name == "Random Rock":
                new_index = self.generate_random_index(self.player_data.rockIndex, 1, 17)
                self.player_data.rockIndex = new_index
            elif item_name == "Random Small Rock":
                new_index = self.generate_random_index(self.player_data.smallRockIndex, 1, 17)
                self.player_data.smallRockIndex = new_index
            elif item_name == "Random Skin":
                new_index = self.generate_random_index(self.player_data.playerIndex, 1, 6)
                self.player_data.playerIndex = new_index

            coins_text_font = pygame.font.Font(None, 32)
            coins_text = coins_text_font.render(f"Coins: {self.player_data.coins}", True, (255, 255, 255))
            text_rect = coins_text.get_rect(
                left=self.coins_panel_rect.x + self.icon_size[0] + 2 * self.icon_left_offset,
                centery=self.coins_panel_rect.centery)
            self.screen.blit(coins_text, text_rect)
            self.player_data.save()
            pygame.display.flip()


    def generate_random_index(self, current_index, first_index, last_index):
        possible_indices = list(range(first_index, last_index))
        possible_indices.remove(current_index) 
        return random.choice(possible_indices)   
    def run(self):
        while True:
            self.handle_events()
            self.draw_shop_scene()
