import bottle
import functools
import os

from bottle import jinja2_view, redirect, route, request, run, template, error, static_file

from http_configuration_dictionary import configurations_dictionary, limit_per_site
from fileManagerConfig import HttpConfiguration, HttpConfigurations, SitePath
from http_file import HttpFile

view = functools.partial(jinja2_view, template_lookup=['templates'])

app = bottle.Bottle()

http_configurations = HttpConfigurations()
site_paths = SitePath()

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

@app.route('/upload', method='POST')
@view('redirect.html')
def do_upload():
	path = request.forms.get('path')
	configuration_url = request.forms.get('configuration')
	file = HttpFile(
		configuration=http_configurations.get_configuration_by_url(configuration_url),
		path=path)
	upload = request.files.get('upload')
	file.set_site_properties()

	try:
		file_path = f"{file.full_path()}/{upload.filename}"

		upload.save(file_path)
		message = f"File successfully saved to '{file.configuration.name}{file.url_path}, [file={upload.filename}]."
	# File overwritting exception handler.
	except OSError as exception:
		message = f"File already exists. {file.configuration.name}{file.url_path}"
	except AttributeError as exception:
		message = "File not specified."

	return {
		'site_paths': site_paths,
		'message': message,
		'file': file,
	}


# LIST VIEWS:


@app.route('/')
@view('home.html')
def home():
	return {'site_paths': site_paths, 'configurations': http_configurations}

# Handling uploading file.
# POST PAGES
@app.route(f"/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}>", method='POST')
@app.route(f"/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}><directory:path>", method='POST')
@app.route(f"/fs/<root:re:{http_configurations.urls_pattern()}>", method='POST')
@app.route(f"/fs/<root:re:{http_configurations.urls_pattern()}><directory:path>", method='POST')
# GET PAGES
@app.route(f"/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}>")
@app.route(f"/fs/p<page:int>/<root:re:{http_configurations.urls_pattern()}><directory:path>")
@app.route(f"/fs/<root:re:{http_configurations.urls_pattern()}>")
@app.route(f"/fs/<root:re:{http_configurations.urls_pattern()}><directory:path>")
@view('list_dir.html')
def path(root, directory='', page=1):
	file_mask = None
	if request.forms.get('mask'):
		file_mask = request.forms.get('mask')
	configuration = http_configurations.get_configuration_by_url(root)
	file = HttpFile(configuration=configuration, path=directory)
	if file_mask:
		file.mask = file_mask
	file.set_site_properties()
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
@view('redirect.html')
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
@view('page_404.html')
def mistake404(code):
	return {
		'message': "Page does not exist.",
		'site_paths': site_paths,
	}
