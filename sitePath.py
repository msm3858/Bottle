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
