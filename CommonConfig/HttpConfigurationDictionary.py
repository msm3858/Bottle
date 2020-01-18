configurations_dictionary = {
	'Export': {
		'url': 'export',
		'root_path': '/data',
		'local_path': '/data/export/',
		'is_removable': True
	},
	'Import': {
		'url': 'import',
		'root_path': '/data',
		'local_path': '/data/Import/',
		'is_removable': False
	},
}

limit_per_site = 100

hostname = 'localhost'
port = 80
template_path = '/home/msm/PycharmProjects/BottleNew/Common/PythonLibraries/HttpFileManager/.views/'
apache_dir = 'WebApp'
# Directory where download.zip file is generated.
temp_apache_directory = '/data/apache_temp/'