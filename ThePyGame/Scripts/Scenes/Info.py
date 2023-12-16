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
        self.none_icon = pygame.image.load('./ThePyGame/Assets/Icons/Effects/1.png')
        self.inversion_icon = pygame.image.load('./ThePyGame/Assets/Icons/Effects/2.png')
        self.slow_icon = pygame.image.load('./ThePyGame/Assets/Icons/Effects/3.png')
        self.fast_icon = pygame.image.load('./ThePyGame/Assets/Icons/Effects/4.png')

        self.font = pygame.font.Font(None, 32)

        self.icon_size = (25, 30)
        self.icon_left_offset = 10

    def draw_settings_menu(self):
        self.screen.fill(self.bg_color)

        rules_text = self.font.render("Rules of the game:", True, (255, 255, 255))
        rules_text_rect = rules_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(rules_text, rules_text_rect)

        rule1_text = self.font.render("1. Dodge obstacles. Collect coins and improve your record.", True, (255, 255, 255))
        rule1_rect = rule1_text.get_rect(center=(self.width // 2, 120))
        self.screen.blit(rule1_text, rule1_rect)

        controls_text = self.font.render("Controls:", True, (255, 255, 255))
        controls_rect = controls_text.get_rect(center=(self.width // 2, 190))
        self.screen.blit(controls_text, controls_rect)

        control_up_text = self.font.render("Up arrow - move up", True, (255, 255, 255))
        control_up_rect = control_up_text.get_rect(center=(self.width // 2, 220))
        self.screen.blit(control_up_text, control_up_rect)

        control_down_text = self.font.render("Down arrow - move down", True, (255, 255, 255))
        control_down_rect = control_down_text.get_rect(center=(self.width // 2, 250))
        self.screen.blit(control_down_text, control_down_rect)

        control_left_text = self.font.render("Left arrow - move left", True, (255, 255, 255))
        control_left_rect = control_left_text.get_rect(center=(self.width // 2, 280))
        self.screen.blit(control_left_text, control_left_rect)

        control_right_text = self.font.render("Right arrow - move right", True, (255, 255, 255))
        control_right_rect = control_right_text.get_rect(center=(self.width // 2, 310))
        self.screen.blit(control_right_text, control_right_rect)

        # Adding information about game modes
        modes_text = self.font.render("Game Modes:", True, (255, 255, 255))
        modes_rect = modes_text.get_rect(center=(self.width // 2, 360))
        self.screen.blit(modes_text, modes_rect)

        normal_mode_text = self.font.render("- Normal - 4 types of obstacles, task is to collect coins.", True, (255, 255, 255))
        normal_mode_rect = normal_mode_text.get_rect(center=(self.width // 2, 390))
        self.screen.blit(normal_mode_text, normal_mode_rect)

        hardcore_mode_text = self.font.render("- Hardcore - 2 types of obstacles (1 large and 1 smaller), player slower, obstacles faster, task is to collect coins.", True, (255, 255, 255))
        hardcore_mode_rect = hardcore_mode_text.get_rect(center=(self.width // 2, 430))
        self.screen.blit(hardcore_mode_text, hardcore_mode_rect)

        secret_mode_text = self.font.render("- Secret - 1 type of obstacle, goal is to collect special eggs with effects.", True, (255, 255, 255))
        secret_mode_rect = secret_mode_text.get_rect(center=(self.width // 2, 470))
        self.screen.blit(secret_mode_text, secret_mode_rect)

        # Adding information about effects
        effects_text = self.font.render("Effects:", True, (255, 255, 255))
        effects_rect = effects_text.get_rect(center=(self.width // 2, 520))
        self.screen.blit(effects_text, effects_rect)

        none_effect_text = self.font.render("None - No special effect", True, (255, 255, 255))
        none_effect_rect = none_effect_text.get_rect(center=(self.width // 2, 550))
        self.screen.blit(none_effect_text, none_effect_rect)
        self.screen.blit(pygame.transform.scale(self.none_icon, self.icon_size),
                         (self.width // 2 + 140, 550 - self.icon_size[1] // 2))

        inversion_effect_text = self.font.render("Inversion - Inverts controls", True, (255, 255, 255))
        inversion_effect_rect = inversion_effect_text.get_rect(center=(self.width // 2, 580))
        self.screen.blit(inversion_effect_text, inversion_effect_rect)
        self.screen.blit(pygame.transform.scale(self.inversion_icon, self.icon_size),
                         (self.width // 2 + 150, 580 - self.icon_size[1] // 2))

        slow_effect_text = self.font.render("Slow - Slows down player", True, (255, 255, 255))
        slow_effect_rect = slow_effect_text.get_rect(center=(self.width // 2, 610))
        self.screen.blit(slow_effect_text, slow_effect_rect)
        self.screen.blit(pygame.transform.scale(self.slow_icon, self.icon_size),
                         (self.width // 2 + 140, 610 - self.icon_size[1] // 2))

        fast_effect_text = self.font.render("Fast - Speeds up player", True, (255, 255, 255))
        fast_effect_rect = fast_effect_text.get_rect(center=(self.width // 2, 640))
        self.screen.blit(fast_effect_text, fast_effect_rect)
        self.screen.blit(pygame.transform.scale(self.fast_icon, self.icon_size),
                         (self.width // 2 + 130, 640 - self.icon_size[1] // 2))

        # Code to display the "Back" button
        button_margin = 10
        icon_size = (40, 40)
        icon_left_offset = 20
        text_offset = 30

        self.screen.blit(pygame.transform.scale(self.back_icon, icon_size),
                         (self.back_button_rect.x + icon_left_offset + button_margin,
                          self.back_button_rect.centery - icon_size[1] // 2 + button_margin))

        text_surface = self.font.render("Back", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.back_button_rect.x + icon_left_offset + icon_size[0] + text_offset + button_margin,
                                                  self.back_button_rect.centery + button_margin))
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
