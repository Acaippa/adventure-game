class intFloat:
	def __init__(self, value):
		self.return_value = value

	def get(self):
		return round(self.return_value)

	def __iadd__(self, other):
		self.return_value += other
		return self

	def __isub__(self, other):
		self.return_value -= other
		return self

	def __add__(self, other):
		return self.return_value + other

	def __sub__(self, other):
		return self.return_value - other