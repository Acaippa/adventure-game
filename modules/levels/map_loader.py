from modules.entities.entities import*

class MapLoader:
	def __init__(self, level):
		self.level = level
		self.entity_list = {"p" : Player, "0" : Tree, "-1" : Entity}

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