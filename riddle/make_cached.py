from .Folder import Folder


def make_cached(function, path):
	def cached(*args, **kwargs):
		folder = Folder(path=path)
		if (args, kwargs) in folder:
			return folder[(args, kwargs)]
		else:
			result = function(*args, **kwargs)
			folder[(args, kwargs)] = result
			return result
	return cached
