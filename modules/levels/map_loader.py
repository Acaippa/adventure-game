from modules.entities.entities import*

class MapLoader:
	def __init__(self, level):
		self.level = level
		self.entity_list = {"p" : Player, "1" : Tree, "0" : Entity}

	def load_map(self, map): # Loops through any two-dimentional python list and initiate the different entities.
		for y in range(len(map)):
			for x in range(len(map[y])):
				type = map[y][x]
				if type == "p":
					self.level.player = self.entity_list[type](self.level)

				elif type != "0":
					self.level.entity_list.append(self.entity_list[type](self.level, (x * 16, y * 16)))

