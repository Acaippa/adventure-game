from modules.entities.player import Player
from modules.entities.tree import Tree
from modules.entities.enemy_spawner01 import EnemySpawner01
from modules.entities.enemy_spawner02 import EnemySpawner02
from modules.entities.enemy_spawner03 import EnemySpawner03
from modules.entities.enemies.skeleton import Skeleton
from modules.entities.berries.acai_berry import *
from modules.entities.berries.goji_berry import *
from modules.entities.berries.sugar_berry import *
from modules.entities.berries.cran_berry import *
from modules.entities.entity import Entity


class MapLoader:
	def __init__(self, level):
		self.level = level
		self.entity_list = {"p" : Player, "0" : Tree, "-1" : Entity, "1" : EnemySpawner01, "2" : EnemySpawner02, "3" : EnemySpawner03}

		self.level.entity_list.append(Skeleton(self.level, (290, 200)))
		self.level.entity_list.append(AcaiBerry(self.level, (290, 230))) #! TEMP
		self.level.entity_list.append(GojiBerry(self.level, (290, 240))) #! TEMP
		self.level.entity_list.append(SugarBerry(self.level, (290, 250))) #! TEMP
		self.level.entity_list.append(CranBerry(self.level, (290, 260))) #! TEMP

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