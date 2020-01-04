from chronometry.progress import ProgressBar, iterate
import secrets
import random
from pandas import DataFrame, Series


def get_nonzero_random_below(n):
	if secrets.randbelow(2) == 0:
		return secrets.randbelow(n-1) + 1
	else:
		return -secrets.randbelow(n-1) - 1


class Anonymizer:
	def __init__(self, map_numbers, upper_bound=1000):
		self._values_to_keys = {}
		self._keys_to_values = {}
		self._count = 0
		self._coefficient = get_nonzero_random_below(upper_bound)
		self._constant = get_nonzero_random_below(upper_bound)
		self._map_numbers = map_numbers

	@property
	def keys(self):
		return self._keys_to_values.keys()

	def anonymize_value(self, value, prefix='r'):
		if isinstance(value, str):
			if value in self._values_to_keys:
				return self._values_to_keys[value]
			else:
				key = f'{prefix}{self._count}'
				self._values_to_keys[value] = key
				self._keys_to_values[key] = value
				self._count += 1
				return key
		elif self._map_numbers and isinstance(value, (int, float)):
			return value * self._coefficient + self._constant
		else:
			return value

	def identify_key(self, key):
		if isinstance(key, str):
			return self._keys_to_values[key]
		elif self._map_numbers and isinstance(key, int):
			return int(round((key - self._constant) / self._coefficient))
		elif self._map_numbers and isinstance(key, float):
			return (key - self._constant) / self._coefficient
		else:
			return key

	def anonymize(self, values, shuffle=True, text=None, echo=0):
		"""
		:type values: list or Series
		:type shuffle: bool
		:type echo: int or bool
		:rtype: list
		"""
		echo = max(0, echo)
		values = list(values)
		if shuffle:
			shuffled = values.copy()
			random.shuffle(shuffled)
			[self.anonymize_value(value=x) for x in iterate(shuffled, echo=echo, text='shuffling')]

		return list(ProgressBar.map(
			function=lambda x: self.anonymize_value(value=x),
			iterable=values, echo=echo, text=text or 'anonymizing'
		))

	def identify(self, keys, text=None, echo=0):
		"""
		:type keys: list or Series
		:type echo: bool or int
		:rtype: list
		"""
		echo = max(0, echo)
		keys = list(keys)
		return list(ProgressBar.map(
			function=lambda x: self.identify_key(key=x),
			iterable=keys, echo=echo, text=text or 'identifying'
		))

class SecretKeeper:
	"""
	SecretKeeper is a data anonymizer
	"""
	def __init__(self, map_numbers=False):
		"""
		:type data: DataFrame
		"""
		self._value_anonymizers = {}
		self._name_anonymizer = Anonymizer(map_numbers=False)
		self._map_numbers = map_numbers

	def anonymize_series(self, series, name, shuffle=True, text=None, echo=1):
		"""
		:type series: list or Series
		:type name: str
		:type echo: bool or int
		:rtype: list
		"""
		echo = max(0, echo)
		name = str(name)
		if name not in self._value_anonymizers:
			self._value_anonymizers[name] = Anonymizer(map_numbers=self._map_numbers)

		anonymizer = self._value_anonymizers[name]
		return anonymizer.anonymize(values=series, shuffle=shuffle, text=text, echo=echo)

	def identify_series(self, series, key, text=None, echo=1):
		"""
		:type series: list or Series
		:type key: str
		:type echo: bool or int
		:rtype:
		"""
		echo = max(0, echo)
		key = str(key)
		anonymizer = self._value_anonymizers[key]
		return anonymizer.identify(keys=series, text=text, echo=echo)

	def anonymize(self, data, shuffle=True, echo=1):
		"""
		:type data: DataFrame
		:rtype:  data
		"""
		echo = max(0, echo)
		result = DataFrame()
		for name in data.columns:
			anonymized_name = self._name_anonymizer.anonymize_value(value=str(name), prefix='column_')
			result[anonymized_name] = self.anonymize_series(
				series=data[name], name=anonymized_name, shuffle=shuffle, text=f'anonymizing column {name}', echo=echo
			)

		return result

	def identify(self, data, echo=1):
		"""
		:type data: DataFrame
		:type echo: bool or int
		:rtype:
		"""
		echo = max(0, echo)
		result = DataFrame()
		for anonymized_name in data.columns:
			name = self._name_anonymizer.identify_key(key=anonymized_name)
			result[name] = self.identify_series(
				series=data[anonymized_name], key=anonymized_name, text=f'identifying column {name}', echo=echo
			)
		return result