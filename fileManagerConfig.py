class SitePath:
	def __init__(self, hostname='localhost', port=5000):
		self.hostname = hostname
		self.port = port

	@property
	def server_home(self):
		return f'http://{self.hostname}'

	@property
	def home_site(self):
		return f'http://{self.hostname}:{self.port}'

	@property
	def data_site(self):
		return f'http://{self.hostname}:{self.port}/fs/'

	@property
	def download_site(self):
		return f'http://{self.hostname}:{self.port}/download/'

	@property
	def delete_site(self):
		return f'http://{self.hostname}:{self.port}/remove/'

	@property
	def upload_site(self):
		return f'http://{self.hostname}:{self.port}/upload/'


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


class HttpConfigurations:
	def __init__(self):
		self._configurations = []

	@property
	def configurations(self):
		return self._configurations

	def add_configuration(self, http_configuration):
		self._configurations.append(http_configuration)

	def set_configurations(self, http_configurations):
		self._configurations = http_configurations

	def get_names(self):
		names = []
		for configuration in self._configurations:
			names.append(configuration.name)
		return names

	def get_urls(self):
		urls = []
		for configuration in self._configurations:
			urls.append(configuration.url)
		return urls

	def urls_pattern(self):
		return '|'.join(list(self.get_urls()))

	def names_pattern(self):
		return '|'.join(list(self.get_names()))

	def get_configuration_by_url(self, url):
		matching_configuration = None
		for configuration in self._configurations:
			if configuration.url == url:
				matching_configuration = configuration
		if matching_configuration:
			return matching_configuration
		else:
			return None
