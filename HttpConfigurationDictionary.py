import os


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

hostname = '192.168.1.108'
port = 80

app_name = 'mp'

www_content = '/var/www/BottleFramework/'
views_directory = 'views'

views_path = f"{os.path.join(www_content, views_directory)}/"
