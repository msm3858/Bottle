import os


class HttpFile:
	def __init__(self, configuration, path):
		self._configuration = configuration
		self._url_path = path
		self._previous_path = None
		self._files = []
		self._name = None
		self._extension = None
		self._is_directory = False
		self._is_file = False
		self._is_downloadable = True
		self._is_removable = True
		self._is_visible = True

	@property
	def configuration(self):
		return self._configuration

	@property
	def url_path(self):
		return self._url_path

	@property
	def previous_path(self):
		return self._previous_path

	@property
	def name(self):
		return self._name

	@property
	def extension(self):
		return self._extension

	@property
	def is_directory(self):
		return self._is_directory

	@property
	def is_file(self):
		return self._is_file

	@property
	def is_downloadable(self):
		return self._is_downloadable

	@property
	def is_removable(self):
		return self._is_removable

	@property
	def is_visible(self):
		return self._is_visible

	@configuration.setter
	def configuration(self, configuration):
		self._configuration = configuration

	@name.setter
	def name(self, name):
		self._name = name

	@extension.setter
	def extension(self, extension):
		self._extension = extension

	@is_downloadable.setter
	def is_downloadable(self, is_downloadable):
		self._is_downloadable = is_downloadable

	@is_removable.setter
	def is_removable(self, is_removable):
		self._is_removable = is_removable

	@is_visible.setter
	def is_visible(self, is_visible):
		self._is_visible = is_visible

	def full_path(self):
		return f"{self._configuration.local_path}{self._url_path}"

	def url_full_path(self):
		return f"{self.configuration.url}{self.previous_path}"

	def set_properties(self):
		print(f"FFPP: {self.full_path()}")
		print(f"{os.path.isfile(self.full_path())}")
		self._is_file = os.path.isfile(self.full_path())
		self._is_directory = os.path.isdir(self.full_path())
		_, self._extension = os.path.splitext(self.full_path())
		self._name = '/'.join(self._url_path.split('/')[-1:])
		self._previous_path = '/'.join(self._url_path.split('/')[:-1])
		print(f"PREVDIR: {self._previous_path}")
		print(f"URLPATH: {self._url_path}")
		if not self._previous_path:
			self._previous_path = ''
		if self._is_directory:
			self.is_downloadable = False
			self.is_removable = False
			self.is_visible = True

	def get_files(self):
		self._files = []
		if self._is_directory:
			files = os.listdir(self.full_path())
			for file in files:
				is_file = os.path.isfile(os.path.join(self.full_path(), file))
				is_directory = os.path.isdir(os.path.join(self.full_path(), file))
				self._files.append({
					'name': file,
					'is_file': is_file,
					'is_directory': is_directory,
				})
		return self._files[:self._configuration.limit_per_site]
