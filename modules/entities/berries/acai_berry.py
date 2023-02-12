from .berry import Berry

class AcaiBerry(Berry):
    def __init__(self, parent, pos, vel = 0):
        super().__init__(parent, pos, "images/berries/acai_berries_small.png", "acai", vel)

        self.effect_duration = 10

        self.force_effect = 50

        self.knockback_effect = 20

    def on_on_used(self):
        self.player.force = self.force_effect
        self.player.knockback = self.knockback_effect