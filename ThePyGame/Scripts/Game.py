import pygame
from Scenes.MainMenu import MainMenu
from GameData.PlayerData import PlayerData 


if __name__ == "__main__":
    pygame.init()
    player_data = PlayerData()
    player_data.load()
    main_menu = MainMenu(1280, 720, player_data)
    main_menu.run()
