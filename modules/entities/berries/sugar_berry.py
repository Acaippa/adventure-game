from .berry import Berry 

class SugarBerry(Berry):
    def __init__(self, parent, pos, vel = 0):
        super().__init__(parent, pos, "images/berries/sugar_berries_small.png", "sugar", vel)

        self.effect_health = 35

    def on_on_used(self):
        self.player.health += 35