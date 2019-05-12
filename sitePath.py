class SitePath:
	def __init__(self, hostname, app_name, port=80):
		self.hostname = hostname
		self.port = port
		self._site = f'http://{self.hostname}:{self.port}/{app_name}'

	@property
	def server_home(self):
		return f'http://{self.hostname}:{self.port}/'

	@property
	def home_site(self):
		return self._site

	@property
	def data_site(self):
		return f'{self._site}/fs/'

	@property
	def download_site(self):
		return f'{self._site}/download/'

	@property
	def delete_site(self):
		return f'{self._site}/remove/'

	@property
	def upload_site(self):
		return f'{self._site}/upload/'
