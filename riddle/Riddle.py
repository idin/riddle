from .encrypt import encrypt as _encrypt
from .encrypt import decrypt as _decrypt
from slytherin.hash import hash_object

import random
import dill


# Riddle encrypts and decrypts objects
class Riddle:
	_ENCRYPTION_CHECK = 'Marvolo'

	# a class that can encrypt or decrypt an object
	def __init__(self, key=None, hash=True, hash_base=64):
		self._hash = hash
		self._hash_base = hash_base
		self._dict = {}
		if key is not None:
			key = str(key)
		self._key = None
		self.unlock(key=key)

	def __getstate__(self):
		return {
			'hash': self._hash,
			'hash_base': self._hash_base,
			'dict': self._dict,
			'key': self._key
		}

	def __setstate__(self, state):
		self._hash = state['hash']
		self._hash_base = state['hash_base']
		self._dict = state['dict']
		self._key = state['key']

	def lock(self):
		self._key = None

	def unlock(self, key):
		if key is None:
			raise ValueError('key cannot be None!')
		if self._hash:
			self._key = self.hash(obj=key, base=self._hash_base)
		else:
			self._key = str(key)

	@property
	def key(self):
		if self._key is None:
			raise KeyError('Riddle is locked!')
		else:
			return self._key

	def get(self, item):
		encrypted_item = self._dict[item]
		return self.decrypt(encrypted_item)

	def set(self, item, obj):
		encrypted_item = self.encrypt(obj=obj)
		self._dict[item] = encrypted_item

	def __getitem__(self, item):
		return self.get(item=item)

	def __setitem__(self, key, value):
		self.set(item=key, obj=value)

	def encrypt(self, obj):
		# obj_plus: first element is for making sure the encryption was successful
		# second element is the actual object
		# third element is to make cracking the encryption harder
		key = self.key
		obj_plus = (
			str(round(random.uniform(0, 1), 3)),
			self._ENCRYPTION_CHECK,
			obj,
			str(round(random.uniform(0, 1), 3))
		)
		clear = dill.dumps(obj_plus, protocol=0)
		decoded = clear.decode(encoding='utf-8')
		return _encrypt(key=key, clear=decoded)

	def decrypt(self, obj):
		key = self.key
		clear_string = _decrypt(key=key, encrypted=obj)
		decrypted_list = dill.loads(clear_string.encode(encoding='utf-8'))
		if decrypted_list[1] != self._ENCRYPTION_CHECK:
			raise KeyError('Riddle: decryption failed!')
		return decrypted_list[2]

	def save(self, x, path):
		encrypted = self.encrypt(x)
		dill.dump(obj=encrypted, file=open(file=path, mode='wb'))

	def load(self, path):
		encrypted = dill.load(file=open(file=path, mode='rb'))
		return self.decrypt(encrypted)

	@staticmethod
	def hash(obj, base=64):
		return hash_object(obj=obj, base=base)