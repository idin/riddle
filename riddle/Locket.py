from .Riddle import Riddle

from disk import Box


# Locket is a Box that uses a Riddle to encrypt objects before storing and decrypt them after accessing
class Locket(Box):
	def __init__(self, path, key=None, save_interval_seconds=60):
		super().__init__(path=path, save_interval_seconds=save_interval_seconds)
		self._riddle = Riddle(key=key)

	def __getstate__(self):
		state = super().__getstate__()
		state['riddle'] = self._riddle
		return state

	def __setstate__(self, state):
		super().__setstate__(state=state)
		self._riddle = state['riddle']

	def get(self, name):
		encrypted_item = super().get(name=name)
		return self._riddle.decrypt(obj=encrypted_item)

	def set(self, name, obj):
		encrypted_item = self._riddle.encrypt(obj=obj)
		super().set(name=name, obj=encrypted_item)

	@property
	def items(self):
		self.check()
		encrypted_items = self._dict.items()
		return {key: self._riddle.decrypt(obj=encrypted_value) for key, encrypted_value in encrypted_items}

	def unlock(self, key):
		self._riddle.unlock(key=key)

	def lock(self):
		self._riddle.lock()

