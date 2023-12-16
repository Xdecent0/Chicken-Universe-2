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

        self.back_icon = pygame.image.load('./ThePyGame/Assets/Icons/Buttons/return.png') 

        self.font = pygame.font.Font(None, 32)

        self.icon_size = (25, 30)
        self.icon_left_offset = 10


    def draw_settings_menu(self):
        self.screen.fill(self.bg_color) 

        button_margin = 10 

        icon_size = (40, 40)
        icon_left_offset = 20
        text_offset = 30 

        self.screen.blit(pygame.transform.scale(self.back_icon, icon_size), (self.back_button_rect.x + icon_left_offset + button_margin, self.back_button_rect.centery - icon_size[1] // 2 + button_margin))

        text_surface = self.font.render("Back", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.back_button_rect.x + icon_left_offset + icon_size[0] + text_offset + button_margin, self.back_button_rect.centery + button_margin))
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


    def run(self):
        while True:
            self.handle_events()
            self.draw_settings_menu()


