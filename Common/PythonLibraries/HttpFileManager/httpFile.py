import datetime
import glob
import math
import os


class HttpFile:
	def __init__(self, configuration, path):
		self._configuration = configuration
		self._url_path = path
		self._previous_path = None
		self._files = []
		self._filtered_files = []
		self._count_not_filtered_files = 0
		self._count_filtered_files = 0
		self._name = None
		self._extension = None
		self._mask = '*'
		self._is_directory = False
		self._is_file = False
		self._is_downloadable = True
		self._is_removable = True
		self._is_visible = True
		self._pages = 1

	@property
	def configuration(self):
		return self._configuration

	@property
	def count_not_filtered_files(self):
		return self._count_not_filtered_files

	@property
	def count_filtered_files(self):
		return self._count_filtered_files
	@property
	def pages(self):
		return self._pages
	@property
	def files(self):
		return self._files
	@property
	def url_path(self):
		return self._url_path

	@property
	def previous_path(self):
		return self._previous_path

	@property
	def mask(self):
		return self._mask

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

	@mask.setter
	def mask(self, mask):
		self._mask = mask

	@name.setter
	def name(self, name):
		self._name = name

	@pages.setter
	def pages(self, pages):
		self._pages = pages

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

	def set_site_properties(self):
		self._is_file = os.path.isfile(self.full_path())
		self._is_directory = os.path.isdir(self.full_path())
		_, self._extension = os.path.splitext(self.full_path())
		self._name = '/'.join(self._url_path.split('/')[-1:])
		self._previous_path = '/'.join(self._url_path.split('/')[:-1])

		if not self._previous_path:
			self._previous_path = ''

		if self._is_directory:
			self.is_downloadable = False
			self.is_removable = False
			self.is_visible = True

	def list_files(self, page=1):
		return self.get_filtered_files(page)

	def set_files_from_directory(self):
		self._files = []
		self._filtered_files = []
		current_dir = os.getcwd()
		os.chdir(self.full_path())
		self._count_not_filtered_files = len(os.listdir('.'))
		self._filtered_files= glob.glob(self._mask)
		self._count_filtered_files = len(self._filtered_files)
		self._pages = math.ceil(len(self._filtered_files)/self.configuration.limit_per_site)
		self._files = self.set_files_properties(self._filtered_files)
		os.chdir(current_dir)

	def get_filtered_files(self, page):
		return self.get_limited_files(page)

	def get_limited_files(self, page):
		upper_limit = self._configuration.limit_per_site*page
		if upper_limit > len(self._files):
			upper_limit = len(self._files)

		if self._configuration.limit_per_site != 0:
			if page > 1:
				lower_limit = self._configuration.limit_per_site*(page-1)
			else:
				lower_limit = 0
			return self._files[lower_limit:upper_limit]
		else:
			return self._files

	def set_files_properties(self, files):
		files_list = []

		for file in files:
			file_path = os.path.join(self.full_path(), file)
			is_file = os.path.isfile(file_path)
			is_directory = os.path.isdir(file_path)
			# created = time.ctime(os.path.getctime(file_path))
			created = datetime.datetime.fromtimestamp(
				os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')

			# modified = time.ctime(os.path.getmtime(file_path))
			modified = datetime.datetime.fromtimestamp(
				os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
			size = os.path.getsize(file_path)
			mb = 2**20
			kb = 2**10

			# Check is size is greater than 1MB
			if size >= mb:
				size = "%.2f MB" % round(size/mb, 2)
			# Check is size is greater than 1KB
			elif size >= kb:
				size = "%.2f KB" % round(size / kb, 2)
			else:
				size = f"{size} B"

			files_list.append({
				'name': file,
				'is_file': is_file,
				'is_directory': is_directory,
				'created': created,
				'modified': modified,
				'size': size,
			})
		return sorted(sorted(files_list, key = lambda field: field['name']), key = lambda field: field['is_directory'], reverse=True)