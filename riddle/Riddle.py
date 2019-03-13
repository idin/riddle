from .encrypt import encrypt as _encrypt
from .encrypt import decrypt as _decrypt
from .hash import hash as _hash
from .hash import hash_dictionary as _hash_dictionary

import dill

class Riddle:
	# a class that can encrypt or decrypt an object
	def __init__(self, key, hash=True, base=64):
		if hash:
			self._key = self.hash(obj=key, base=base)

		else:
			self._key = str(key)

	def __getstate__(self):
		return self._key

	def __setstate__(self, state):
		self._key = state

	def encrypt(self, x):
		clear = dill.dumps(x, protocol=0)
		clear = clear.decode(encoding='utf-8')
		return _encrypt(key=self._key, clear=clear)

	def decrypt(self, x):
		clear_string = _decrypt(key=self._key, encrypted=x)
		return dill.loads(clear_string.encode(encoding='utf-8'))

	def write_pickle(self, x, file):
		encrypted = self.encrypt(x)
		dill.dump(obj=encrypted, file=open(file=file, mode='wb'))

	def read_pickle(self, file):
		encrypted = dill.load(file=open(file=file, mode='rb'))
		return self.decrypt(encrypted)

	@staticmethod
	def hash(obj, base=64):
		return _hash(obj=obj, base=base)