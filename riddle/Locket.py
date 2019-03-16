from .Riddle import Riddle
import route

class Locket:
	def __init__(self, key):
		self._riddle = Riddle(key=key)
		self._items

	def __getstate__(self):
		return self._riddle._key

	def __setstate__(self, state):
		self._riddle = Riddle(key=state)


