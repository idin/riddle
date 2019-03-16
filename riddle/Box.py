import route
import atexit
import send2trash
import os
from chronology import get_elapsed_seconds, get_now

class Box:
	def __init__(self, path, save_interval_seconds=60):
		self._path = route.Path(string=path)
		self._path.make_parent_directory(ignore_if_exists=True)

		self._num_saved_items = None

		self._dict = {}
		self.load(append=False)

		self._save_interval_seconds = save_interval_seconds
		self._save_time = get_now()

		atexit.register(self.save)

	# working with the file
	def file_exists(self):
		if self.path.exists():
			if self.path.is_file():
				return True
			else:
				raise ValueError(f'Box: {self.path} is not a file!')
		else:
			return False

	def load(self, append=True):
		if self.file_exists():
			dictionary = self._path.unpickle(method='pickle')
			if append:
				dictionary.update(self._dict)
			self._dict = dictionary

	def delete_file(self):
		if self.file_exists():

			Pickler.delete(path=self._path)

	def save(self, append=True, echo=1):
		echo = max(0, echo)
		if len(self._dict)>0:
			if echo: print(f'Saving to "{self._path}"')
			if append:
				self.load(append=True)
			Pickler.save(obj=self._dict, path=self._path)
		else:
			if echo: print('Nothing to save!')
			if not append:
				self.delete_file()

		self._save_time = get_now()

	@property
	def file_size(self):
		self.check()
		try:
			return os.path.getsize(self.path)
		except:
			return 0


	def copy(self):
		self.check()
		return self

	@property
	def path(self):
		self.check()
		return self._path

	@property
	def names(self):
		self.check()
		return self._dict.keys()

	@property
	def items(self):
		self.check()
		return self._dict.items()

	@property
	def objects(self):
		self.check()
		return self._dict.values()



	def get_all_names(self):
		self.check()
		return self._dict.keys()

	@property
	def size(self):
		return len(self._dict)

	def contains(self, name):
		self.check()
		return name in self._dict

	def get(self, name):
		self.check()
		return self._dict[name]

	def check(self, echo=0):
		echo = max(0, echo)
		# if the number of items increased by more than 10% o
		if get_elapsed_seconds(start=self._save_time)>self._save_interval_seconds:
			self.save(echo=echo, append=True)

	def put(self, name, obj):
		self._dict[name] = obj
		self.check()

	def remove(self, name):
		del self._dict[name]
		self.check()

	def flush(self):
		self._dict = {}
