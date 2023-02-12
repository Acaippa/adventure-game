from .berry import Berry 

class GojiBerry(Berry):
    def __init__(self, parent, pos, vel = 0):
        super().__init__(parent, pos, "images/berries/goji_berries_small.png", "goji", vel)

        self.effect_duration = 10

        self.knockback_effect = 30

        self.force_effect = 25

    def on_on_used(self):
        self.player.knockback = self.knockback_effect
        self.player.foce = self.force_effect