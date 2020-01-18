class HttpConfiguration:
	def __init__(self, name, url, root_path, local_path, is_removable=False, limit_per_site=0):
		self._name = name
		self._url = url
		self._root_path = root_path
		self._local_path = local_path
		self._is_removable = is_removable
		self._limit_per_site = limit_per_site

	@property
	def limit_per_site(self):
		return self._limit_per_site

	@property
	def url(self):
		return self._url

	@property
	def name(self):
		return self._name

	@property
	def root_path(self):
		return self.root_path

	@property
	def local_path(self):
		return self._local_path

	@property
	def is_removable(self):
		return self._is_removable
