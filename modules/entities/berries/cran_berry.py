from .berry import Berry
from .acai_berry import AcaiBerry
from .goji_berry import GojiBerry
from .sugar_berry import SugarBerry
from random import choice

class CranBerry(Berry):
    def __init__(self, parent, pos, vel=0):
        super().__init__(parent, pos, "images/berries/cran_berries_small.png", "cran", vel)

        acai = AcaiBerry(self.parent, (0, 0))
        goji = GojiBerry(self.parent, (0, 0))
        sugar = SugarBerry(self.parent, (0, 0))

        self.effect_list = [
                {"player.force" : acai.force_effect, "player.knockback" : acai.knockback_effect},

                {"player.knockback" : goji.knockback_effect, "player.force" : goji.force_effect},

                {"player.health" : sugar.effect_health}
        ]

    def on_on_used(self):
        random_berry = choice(self.effect_list)
        for player_var in random_berry:
            setattr(self, player_var, random_berry[player_var])
