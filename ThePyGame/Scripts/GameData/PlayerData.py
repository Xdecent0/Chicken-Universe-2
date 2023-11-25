import pickle

class PlayerData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PlayerData, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.normalHighscore = 0
        self.hardcoreHighscore = 0
        self.secretHighscore = 0
        self.coins = 0
        self.lives = 1
        self.playerIndex = 1
        self.planetIndex = 1
        self.rockIndex = 1
        self.smallRockIndex = 1

    def save(self):
        with open("./Scripts/GameData/game_data.pkl", "wb") as file:
            pickle.dump(self, file)

    def load(self):
        try:
            with open("./Scripts/GameData/game_data.pkl", "rb") as file:
                game_data = pickle.load(file)
                self.normalHighscore = game_data.normalHighscore
                self.hardcoreHighscore = game_data.hardcoreHighscore
                self.secretHighscore = game_data.secretHighscore
                self.coins = game_data.coins
                self.lives = game_data.lives
                self.playerIndex = game_data.playerIndex
                self.planetIndex = game_data.planetIndex
                self.rockIndex = game_data.rockIndex
                self.smallRockIndex = game_data.smallRockIndex
        except (FileNotFoundError, EOFError):
            self._initialize()

    def reset(self):
        self._initialize()
