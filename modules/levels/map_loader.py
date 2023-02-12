from modules.entities.player import Player
from modules.entities.tree import Tree
from modules.entities.enemy_spawner01 import EnemySpawner01
from modules.entities.enemy_spawner02 import EnemySpawner02
from modules.entities.enemy_spawner03 import EnemySpawner03
from modules.entities.enemies.skeleton import Skeleton
from modules.entities.enemies.broccoli import Broccoli
from modules.entities.berries.berry import Berry
from modules.entities.entity import Entity


class MapLoader:
	def __init__(self, level):
		self.level = level
		self.entity_list = {"p" : Player, "0" : Tree, "-1" : Entity, "1" : EnemySpawner01, "2" : EnemySpawner02, "3" : EnemySpawner03}

		self.level.entity_list.append(Skeleton(self.level, (290, 200)))
		# self.level.entity_list.append(Berry(self.level, (290, 200), "images/berries/acai_berries_small.png", "acai")) #! TEMP

	def load_map(self, map): # Loops through any two-dimentional python list and initiate the different entities.
		for y in range(len(map)):
			for x in range(len(map[y])):
				type = map[y][x]
				if type == "p":
					self.level.player = self.entity_list[type](self.level, start_pos=(x * 16, y * 16))

				elif type != "-1":
					self.level.entity_list.append(self.entity_list[type](self.level, (x * 16, y * 16)))

	def load_csv(self, file):
		with open(file, "rb") as f:
			content = str(f.read())[2:-1]
			result = []
			for item in content.split("\\r\\n"):
				result.append([i for i in item.split(",")])

			result.remove(result[-1])
			self.load_map(result)