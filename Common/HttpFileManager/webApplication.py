import bottle
import logging
import os
from zipfile import ZipFile

from bottle import jinja2_view, request, static_file


from CommonConfig.HttpConfigurationDictionary import configurations_dictionary, limit_per_site, hostname, port, template_path, apache_dir, temp_apache_directory
from Common.PythonLibraries.HttpFileManager.httpConfiguration import HttpConfiguration
from Common.PythonLibraries.HttpFileManager.httpConfigurations import HttpConfigurations
from Common.PythonLibraries.HttpFileManager.sitePath import SitePath
from Common.PythonLibraries.HttpFileManager.httpFile import HttpFile

bottle.TEMPLATE_PATH.insert(0, template_path)
logging.debug(os.path.join(os.getcwd(), 'templates'))
app = bottle.Bottle()

http_configurations = HttpConfigurations()
site_paths = SitePath(hostname=hostname, port=port, apache_dir=apache_dir)

# Load configurations from http_configuration_directory.py
for configuration in configurations_dictionary.keys():
	http_configurations.add_configuration(
		HttpConfiguration(
			name=configuration,
			url=configurations_dictionary[configuration]['url'],
			root_path=configurations_dictionary[configuration]['root_path'],
			local_path=configurations_dictionary[configuration]['local_path'],
			is_removable=configurations_dictionary[configuration]['is_removable'],
			limit_per_site=limit_per_site
		)
	)


# FILE MANAGEMENT:

# # Handling uploading file.
@app.route(f'/{site_paths.apache_dir}/upload', method='POST')
@app.route('/upload', method='POST')
@jinja2_view('upload_confirm.html')
def do_upload():
	path = request.forms.get('path')
	configuration_url = request.forms.get('configuration')
	file = HttpFile(
		configuration=http_configurations.get_configuration_by_url(configuration_url),
		path=path)
	uploads = request.files.getall('upload')
	file.set_site_properties()
	messages = []
	for upload in uploads:
		try:
			file_path = f"{file.full_path()}/{upload.filename}"
			upload.save(file_path)
			messages.append(f"File successfully saved to '{file.configuration.name}{file.url_path}, [file={upload.filename}].")
		# File overwriting exception handler.
		except OSError as exception:
			messages.append(f"Could not upload file {upload.filename} at {file.configuration.name}{file.url_path}. Exception: [{exception}]")
		except AttributeError as exception:
			messages.append("File not specified.")

	return {
		'site_paths': site_paths,
		'messages': messages,
		'file': file,
	}


@app.route(f'/remove_files', method='POST')
@app.route(f'/{site_paths.apache_dir}/remove_files', method='POST')
@jinja2_view('upload_confirm.html')
def remove_many():
	path = request.forms.get('path')
	configuration_url = request.forms.get('configuration')
	file = HttpFile(
		configuration=http_configurations.get_configuration_by_url(configuration_url),
		path=path)
	file.set_site_properties()
	messages = []

	if file.configuration.is_removable:
		remove_files = request.forms.getall('remove_files_list')

		for remove_file in remove_files:
			try:
				file_path = f"{file.full_path()}/{remove_file}"
				print(file_path)
				os.remove(f"{file_path}")
				messages.append(f"File successfully removed ['{file.configuration.name}{file.url_path}/{remove_file}'].")
			# File overwriting exception handler.
			except FileNotFoundError as exception:
				messages.append("Sorry, this file does not exist!")
			except OSError as exception:
				messages.append(f"Could not remove: [{remove_file}] already exists at {file.configuration.name}{file.url_path}.")
			except AttributeError as exception:
				messages.append("File not specified.")
	else:
		messages.append("Removing file is forbidden.")

	return {
		'site_paths': site_paths,
		'messages': messages,
		'file': file,
	}


@app.route('/download_files', method='POST')
@app.route(f'/{site_paths.apache_dir}/download_files', method='POST')
def do_download_many():
	print("DO")
	print(os.getcwd())
	path = request.forms.get('path')
	configuration_url = request.forms.get('configuration')
	file = HttpFile(
		configuration=http_configurations.get_configuration_by_url(configuration_url),
		path=path)
	file.set_site_properties()
	if request.forms.getall('download_files_list'):
		current_working_directory = os.getcwd()
		os.chdir(file.full_path())
		download_file_names = request.forms.getall('download_files_list')
		zip_file = 'download.zip'
		zip_file_directory = temp_apache_directory
		zip_file_path = os.path.join(zip_file_directory, zip_file)
		with ZipFile(zip_file_path, 'w') as zip:
			try:
				for file_path in download_file_names:
					zip.write(file_path)
			except Exception as exception:
				print(f"ERROR in compressing file {repr(exception)}")
		os.chdir(current_working_directory)
		return static_file(
			zip_file,
			root=zip_file_directory,
			download=zip_file)

# LIST VIEWS:


@app.route('/')
@app.route(f'/{site_paths.apache_dir}/')
@jinja2_view('home.html')
def home():
	return {'site_paths': site_paths, 'configurations': http_configurations}


# Handling uploading file.
# POST PAGES
@app.route(f"/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}>", method='POST')
@app.route(f"/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}><directory:path>", method='POST')
@app.route(f"/fs/<root:re:{http_configurations.urls_pattern()}>", method='POST')
@app.route(f"/fs/<root:re:{http_configurations.urls_pattern()}><directory:path>", method='POST')
@app.route(f"/{site_paths.apache_dir}/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}>", method='POST')
@app.route(f"/{site_paths.apache_dir}/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}><directory:path>", method='POST')
@app.route(f"/{site_paths.apache_dir}/fs/<root:re:{http_configurations.urls_pattern()}>", method='POST')
@app.route(f"/{site_paths.apache_dir}/fs/<root:re:{http_configurations.urls_pattern()}><directory:path>", method='POST')
# GET PAGES
@app.route(f"/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}>")
@app.route(f"/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}><directory:path>")
@app.route(f"/fs/<root:re:{http_configurations.urls_pattern()}>")
@app.route(f"/fs/<root:re:{http_configurations.urls_pattern()}><directory:path>")
# GET PAGES
@app.route(f"/{site_paths.apache_dir}/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}>")
@app.route(f"/{site_paths.apache_dir}/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}><directory:path>")
@app.route(f"/{site_paths.apache_dir}/fs/<root:re:{http_configurations.urls_pattern()}>")
@app.route(f"/{site_paths.apache_dir}/fs/<root:re:{http_configurations.urls_pattern()}><directory:path>")

@jinja2_view('list.html')
def path(root, directory='', page=1):
	file_mask = None

	if request.forms.get('mask'):
		file_mask = request.forms.get('mask')

	configuration = http_configurations.get_configuration_by_url(root)
	file = HttpFile(configuration=configuration, path=directory)

	if file_mask:
		file.mask = file_mask
	file.set_site_properties()

	if file.is_directory:
		file.set_files_from_directory()

	if file.is_file:
		return static_file(
			file.name,
			root=f"{file.configuration.local_path}{file.previous_path}",
			download=file.name)

	return {
		'site_paths': site_paths,
		'file': file,
		'page': page,
	}


@app.route(f"/remove/<root:re:{http_configurations.urls_pattern()}>")
@app.route(f"/remove/<root:re:{http_configurations.urls_pattern()}><directory:path>")
@app.route(f"/{site_paths.apache_dir}/remove/<root:re:{http_configurations.urls_pattern()}>")
@app.route(f"/{site_paths.apache_dir}/remove/<root:re:{http_configurations.urls_pattern()}><directory:path>")
@jinja2_view('redirect.html')
def remove(root, directory=''):
	configuration = http_configurations.get_configuration_by_url(root)
	file = HttpFile(configuration=configuration, path=directory)
	file.set_site_properties()

	try:
		if file.configuration.is_removable:

			if file.is_directory:
				message = "Removing directory is forbidden."
			else:
				os.remove(f"{file.full_path()}")
				file = HttpFile(
					configuration=configuration,
					path=file.previous_path)
				file.set_site_properties()
				message = "File was deleted successfully."

		else:
			message = "Removing file is forbidden."
			file = HttpFile(
				configuration=configuration,
				path=file.previous_path)
			file.set_site_properties()
	# Handling file not found exception.
	except FileNotFoundError as exception:
		message = "Sorry, this file does not exist!"

	return {
		'message': message,
		'site_paths': site_paths,
		'file': file
	}


# COMMON VIEWS.

@app.error(404)
@jinja2_view('page_404.html')
def mistake404(code):
	return {
		'message': "Page does not exist.",
		'site_paths': site_paths,
	}


application = app

