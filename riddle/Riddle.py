from .encrypt import encrypt as _encrypt
from .encrypt import decrypt as _decrypt
from .hash import hash as _hash

import random
import dill

class Riddle:
	_ENCRYPTION_CHECK = 'Dark Mark'

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

	def encrypt(self, obj):
		# obj_plus: first element is for making sure the encryption was successful
		# second element is the actual object
		# third element is to make cracking the encryption harder
		obj_plus = [self._ENCRYPTION_CHECK, obj, random.uniform(0, 1)]

		clear = dill.dumps(obj_plus, protocol=0)
		clear = clear.decode(encoding='utf-8')
		return _encrypt(key=self._key, clear=clear)

	def decrypt(self, obj):
		clear_string = _decrypt(key=self._key, encrypted=obj)
		decrypted_list = dill.loads(clear_string.encode(encoding='utf-8'))
		if decrypted_list[0] != self._ENCRYPTION_CHECK:
			raise KeyError('Riddle: decryption failed!')
		return decrypted_list[1]

	def save(self, x, path):
		encrypted = self.encrypt(x)
		dill.dump(obj=encrypted, file=open(file=path, mode='wb'))

	def load(self, path):
		encrypted = dill.load(file=open(file=path, mode='rb'))
		return self.decrypt(encrypted)

	@staticmethod
	def hash(obj, base=64):
		return _hash(obj=obj, base=base)