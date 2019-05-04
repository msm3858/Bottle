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
