import pygame
import sys
from Scenes.Shop import ShopScene
from Scenes.Settings import SettingsMenu
from Scenes.HardcoreMode import HardcoreMode
from Scenes.NormalMode import NormalMode
from Scenes.SecretMode import SecretMode

class MainMenu:
    def __init__(self, width, height, player_data):

        self.width = width
        self.height = height
        self.player_data = player_data

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chicken Universe 2")

        self.settings_icon = pygame.image.load('./Assets/Icons/Buttons/settings.png')
        self.shop_icon = pygame.image.load('./Assets/Icons/Buttons/shop.png')
        self.exit_icon = pygame.image.load('./Assets/Icons/Buttons/exit.png')

        self.color1 = (146, 106, 255)  # #926AFF
        self.color2 = (66, 77, 252)    # #424DFC
        self.button_color = (66, 136, 252)  # #4288FC

        self.left_width = self.width // 2 + 200  
        self.right_width = self.width // 2 - 200 

        self.left_half = pygame.Rect(0, 0, self.left_width, self.height)
        self.right_half = pygame.Rect(self.left_width, 0, self.right_width, self.height)

        self.font = pygame.font.Font(None, 32) 

        self.settings_text = self.font.render("Settings", True, (255, 255, 255))
        self.shop_text = self.font.render("Shop", True, (255, 255, 255))
        self.exit_text = self.font.render("Exit", True, (255, 255, 255))

        self.normal_mode_text = self.font.render("Normal Mode", True, (255, 255, 255))
        self.flappy_mode_text = self.font.render("Hardcore Mode", True, (255, 255, 255))
        self.secret_mode_text = self.font.render("Secret Mode", True, (255, 255, 255))

        button_width = max(self.settings_text.get_width(), self.shop_text.get_width(), self.exit_text.get_width()) + 160
        button_height = self.settings_text.get_height() + 60

        gap = 20
        top_margin = (self.height - (gap * 2 + button_height * 3)) // 2

        self.settings_rect = pygame.Rect(self.left_width + (self.right_width - button_width) // 2, top_margin, button_width, button_height)
        self.shop_rect = pygame.Rect(self.left_width + (self.right_width - button_width) // 2, top_margin + gap + button_height, button_width, button_height)
        self.exit_rect = pygame.Rect(self.left_width + (self.right_width - button_width) // 2, top_margin + 2 * (gap + button_height), button_width, button_height)

        outline_thickness = 4
        self.settings_outline_rect = pygame.Rect(self.settings_rect.x - outline_thickness, self.settings_rect.y - outline_thickness,
                                                 self.settings_rect.width + 2 * outline_thickness, self.settings_rect.height + 2 * outline_thickness)
        self.shop_outline_rect = pygame.Rect(self.shop_rect.x - outline_thickness, self.shop_rect.y - outline_thickness,
                                             self.shop_rect.width + 2 * outline_thickness, self.shop_rect.height + 2 * outline_thickness)
        self.exit_outline_rect = pygame.Rect(self.exit_rect.x - outline_thickness, self.exit_rect.y - outline_thickness,
                                             self.exit_rect.width + 2 * outline_thickness, self.exit_rect.height + 2 * outline_thickness)
        

        
        text_right_offset = 20

        icon_left_offset = 20

        icon_text_gap = 10

        self.settings_text_rect = self.settings_text.get_rect()
        self.shop_text_rect = self.shop_text.get_rect()
        self.exit_text_rect = self.exit_text.get_rect()

        self.settings_text_rect.topleft = (self.settings_rect.x + icon_left_offset + self.settings_icon.get_width() + icon_text_gap, self.settings_rect.y + (self.settings_rect.height - self.settings_text_rect.height) // 2)
        self.shop_text_rect.topleft = (self.shop_rect.x + icon_left_offset + self.shop_icon.get_width() + icon_text_gap, self.shop_rect.y + (self.shop_rect.height - self.shop_text_rect.height) // 2)
        self.exit_text_rect.topleft = (self.exit_rect.x + icon_left_offset + self.exit_icon.get_width() + icon_text_gap, self.exit_rect.y + (self.exit_rect.height - self.exit_text_rect.height) // 2)

        self.settings_text_rect.x = min(self.settings_text_rect.x, self.settings_rect.x + self.settings_rect.width - text_right_offset - self.settings_text_rect.width)
        self.shop_text_rect.x = min(self.shop_text_rect.x, self.shop_rect.x + self.shop_rect.width - text_right_offset - self.shop_text_rect.width)
        self.exit_text_rect.x = min(self.exit_text_rect.x, self.exit_rect.x + self.exit_rect.width - text_right_offset - self.exit_text_rect.width)

        panel_gap = 20
        panel_width = self.left_width - panel_gap * 2
        panel_height = (self.height - panel_gap * 4) / 3 
        self.panel1_rect = pygame.Rect(panel_gap, panel_gap, panel_width, panel_height)
        self.panel2_rect = pygame.Rect(panel_gap, panel_gap * 2 + panel_height, panel_width, panel_height)
        self.panel3_rect = pygame.Rect(panel_gap, panel_gap * 3 + panel_height * 2, panel_width, panel_height)

        panel_margin = 24
        panel_width = self.right_width - panel_margin * 2
        panel_height = 50
        
        self.coins_panel_rect = pygame.Rect(self.left_width + panel_margin, panel_margin, panel_width, panel_height)

        self.coins_panel_outline_rect = pygame.Rect(self.coins_panel_rect.x - outline_thickness, self.coins_panel_rect.y - outline_thickness,
                                            self.coins_panel_rect.width + 2 * outline_thickness, self.coins_panel_rect.height + 2 * outline_thickness)

        self.coins_panel_color = (66, 136, 252)


        play_button_width = 150
        play_button_height = 50

        self.play_button_rect1 = pygame.Rect(self.panel1_rect.x + 600, self.panel1_rect.centery - 25, play_button_width, play_button_height)
        self.play_button_outline_rect1 = pygame.Rect(self.play_button_rect1.x - 4, self.play_button_rect1.y - 4, self.play_button_rect1.width + 8, self.play_button_rect1.height + 8)

        self.play_button_rect2 = pygame.Rect(self.panel2_rect.x + 600, self.panel2_rect.centery - 25, play_button_width, play_button_height)
        self.play_button_outline_rect2 = pygame.Rect(self.play_button_rect2.x - 4, self.play_button_rect2.y - 4, self.play_button_rect2.width + 8, self.play_button_rect2.height + 8)

        self.play_button_rect3 = pygame.Rect(self.panel3_rect.x + 600, self.panel3_rect.centery - 25, play_button_width, play_button_height)
        self.play_button_outline_rect3 = pygame.Rect(self.play_button_rect3.x - 4, self.play_button_rect3.y - 4, self.play_button_rect3.width + 8, self.play_button_rect3.height + 8)

    def draw_menu(self):
            self.screen.fill(self.color1, self.left_half)
            self.screen.fill(self.color2, self.right_half)

            pygame.draw.rect(self.screen, (255, 255, 255), self.settings_outline_rect, 2)
            pygame.draw.rect(self.screen, (255, 255, 255), self.shop_outline_rect, 2)
            pygame.draw.rect(self.screen, (255, 255, 255), self.exit_outline_rect, 2)

            pygame.draw.rect(self.screen, self.button_color, self.settings_rect)
            pygame.draw.rect(self.screen, self.button_color, self.shop_rect)
            pygame.draw.rect(self.screen, self.button_color, self.exit_rect)

            pygame.draw.rect(self.screen, self.coins_panel_color, self.coins_panel_rect)

            icon_size = (40, 40)
            icon_left_offset = 5
            self.screen.blit(pygame.transform.scale(self.settings_icon, icon_size), (self.settings_rect.x + icon_left_offset, self.settings_rect.centery - icon_size[1] // 2))
            self.screen.blit(pygame.transform.scale(self.shop_icon, icon_size), (self.shop_rect.x + icon_left_offset, self.shop_rect.centery - icon_size[1] // 2))
            self.screen.blit(pygame.transform.scale(self.exit_icon, icon_size), (self.exit_rect.x + icon_left_offset, self.exit_rect.centery - icon_size[1] // 2))

            self.screen.blit(self.settings_text, self.settings_text_rect)
            self.screen.blit(self.shop_text, self.shop_text_rect)
            self.screen.blit(self.exit_text, self.exit_text_rect)

            panel_bg_color = (66, 136, 252)  

            pygame.draw.rect(self.screen, panel_bg_color, self.panel1_rect)

            pygame.draw.rect(self.screen, panel_bg_color, self.panel2_rect)

            pygame.draw.rect(self.screen, panel_bg_color, self.panel3_rect)

            pygame.draw.rect(self.screen, (255, 255, 255), self.coins_panel_outline_rect, 2)

            play_button_rect1 = pygame.Rect(self.panel1_rect.x + 600, self.panel1_rect.centery - 25, 150, 50)
            play_button_outline_rect1 = pygame.Rect(play_button_rect1.x - 4, play_button_rect1.y - 4, play_button_rect1.width + 8, play_button_rect1.height + 8)

            play_button_rect2 = pygame.Rect(self.panel2_rect.x + 600, self.panel2_rect.centery - 25, 150, 50)
            play_button_outline_rect2 = pygame.Rect(play_button_rect2.x - 4, play_button_rect2.y - 4, play_button_rect2.width + 8, play_button_rect2.height + 8)

            play_button_rect3 = pygame.Rect(self.panel3_rect.x + 600, self.panel3_rect.centery - 25, 150, 50)
            play_button_outline_rect3 = pygame.Rect(play_button_rect3.x - 4, play_button_rect3.y - 4, play_button_rect3.width + 8, play_button_rect3.height + 8)

            play_text1 = self.font.render("Play", True, (255, 255, 255))
            play_text_rect1 = play_text1.get_rect(center=play_button_rect1.center)

            play_text2 = self.font.render("Play", True, (255, 255, 255))
            play_text_rect2 = play_text2.get_rect(center=play_button_rect2.center)

            play_text3 = self.font.render("Play", True, (255, 255, 255))
            play_text_rect3 = play_text3.get_rect(center=play_button_rect3.center)

            pygame.draw.rect(self.screen, (255, 255, 255), play_button_outline_rect1, 2)
            pygame.draw.rect(self.screen, (255, 255, 255), play_button_outline_rect2, 2)
            pygame.draw.rect(self.screen, (255, 255, 255), play_button_outline_rect3, 2)

            pygame.draw.rect(self.screen, self.button_color, play_button_rect1)
            pygame.draw.rect(self.screen, self.button_color, play_button_rect2)
            pygame.draw.rect(self.screen, self.button_color, play_button_rect3)

            self.screen.blit(play_text1, play_text_rect1)
            self.screen.blit(play_text2, play_text_rect2)
            self.screen.blit(play_text3, play_text_rect3)

            coins_text_font = pygame.font.Font(None, 32)
            self.coins_text = coins_text_font.render(f"Coins: {self.player_data.coins}", True, (255, 255, 255))

            pygame.draw.rect(self.screen, self.coins_panel_color, self.coins_panel_rect)

            text_rect = self.coins_text.get_rect(center=self.coins_panel_rect.center)
            self.screen.blit(self.coins_text, text_rect)

            text_rect = self.normal_mode_text.get_rect(center=self.panel1_rect.center)
            self.screen.blit(self.normal_mode_text, text_rect)

            text_rect = self.flappy_mode_text.get_rect(center=self.panel2_rect.center)
            self.screen.blit(self.flappy_mode_text, text_rect)

            text_rect = self.secret_mode_text.get_rect(center=self.panel3_rect.center)
            self.screen.blit(self.secret_mode_text, text_rect)

            coins_icon_rect = pygame.Rect(self.coins_panel_rect.x + 110, self.coins_panel_rect.centery - 20, 30, 30)
            coins_icon = pygame.image.load('./Assets/Icons/money.png')
            self.screen.blit(pygame.transform.scale(coins_icon, (25, 30)), coins_icon_rect.topleft)


            highscore_rect1 = self.font.render(f"Highscore: {self.player_data.normalHighscore}", True, (255, 255, 255)).get_rect(left=self.panel1_rect.x + 40, centery=self.panel1_rect.centery)
            self.screen.blit(self.font.render(f"Highscore: {self.player_data.normalHighscore}", True, (255, 255, 255)), highscore_rect1)

            highscore_rect2 = self.font.render(f"Highscore: {self.player_data.hardcoreHighscore}", True, (255, 255, 255)).get_rect(left=self.panel2_rect.x + 40, centery=self.panel2_rect.centery)
            self.screen.blit(self.font.render(f"Highscore: {self.player_data.hardcoreHighscore}", True, (255, 255, 255)), highscore_rect2)

            highscore_rect3 = self.font.render(f"Highscore: {self.player_data.secretHighscore}", True, (255, 255, 255)).get_rect(left=self.panel3_rect.x + 40, centery=self.panel3_rect.centery)
            self.screen.blit(self.font.render(f"Highscore: {self.player_data.secretHighscore}", True, (255, 255, 255)), highscore_rect3)

            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.shop_rect.collidepoint(event.pos):
                    shop_scene = ShopScene(self.width, self.height, self.player_data)
                    shop_scene.run()
                elif self.exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif self.settings_rect.collidepoint(event.pos):
                    settings_menu = SettingsMenu(self.width, self.height, self.player_data)
                    settings_menu.run()
                
                elif self.panel1_rect.collidepoint(event.pos) and self.play_button_rect1.collidepoint(event.pos):
                    normal_mode = NormalMode(self.width, self.height, self.player_data)
                    normal_mode.run()
                elif self.panel2_rect.collidepoint(event.pos) and self.play_button_rect2.collidepoint(event.pos):
                    flappy_mode = HardcoreMode(self.width, self.height, self.player_data)
                    flappy_mode.run()
                elif self.panel3_rect.collidepoint(event.pos) and self.play_button_rect3.collidepoint(event.pos):
                    secret_mode = SecretMode(self.width, self.height, self.player_data)
                    secret_mode.run()


    def run(self):
        while True:
            self.handle_events()
            self.draw_menu()


