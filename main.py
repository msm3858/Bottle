from bottle import route, request, run, template, error, static_file
import os, re

HOSTNAME = 'localhost'
PORT = 8080

home_site = f'http://{HOSTNAME}:{PORT}'
data_site = f'http://{HOSTNAME}:{PORT}/data/'
download_site = f'http://{HOSTNAME}:{PORT}/download/'
upload_site = f'http://{HOSTNAME}:{PORT}/upload/'
dirs = ['extra', 'db']

@route('/')
@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

@route('/upload', method='POST')
def do_upload():
    path = request.forms.get('path')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    # if ext not in ('.png', '.jpg', '.jpeg'):
    #     return "File extension not allowed."

    save_path = "/data/{path}".format(path=path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    
    return "File successfully saved to '{0}, [file={1}].".format(save_path, upload.filename)

@route('/hello')
def hello():
    return "Hello world!"

@route('/download/<filename:path>')
def download(filename):
    root, filename = '/data/' + '/'.join(filename.split('/')[:-1]), filename.split('/')[-1]
    return static_file(filename, root=root, download=filename)

@route('/data/<directory:path>')
def path(directory):
    try:

        dirs_to_check = '|'.join(dirs)
        if re.match(f'^{dirs_to_check}\S*', directory):

            directory = directory
            path = os.path.join('/data', directory)
            files = os.listdir(path)
            # temp = 'Path = {{path}}', path=path
            # for file in files:
            #     temp .= 'File = {{file}}', file
            temp = template('list_dir',
                            data_site=data_site,
                            download_site=download_site,
                            upload_site=upload_site,
                            current_directory=directory,
                            path=str(path),
                            files= files)
            # temp = template("Path =  {{path}}, Files = {{files}}.", path=str(path), files=str(files))
            return temp
        else:
            return 'This directory is not available!'
    except NotADirectoryError as exception:
        root, filename = '/data/' + '/'.join(directory.split('/')[:-1]), directory.split('/')[-1]
        return static_file(filename=filename, root=directory)
        # return "root = {}, filename = {}".format(root, filename)

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

run(host='localhost', port=8080, debug=True)

#
# @route('/todo')
# #
# # def todo_list():
# #
# #     c = conn.cursor()
# #     c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
# #     result = c.fetchall()
# #     c.close()
# #
# #     output = template('make_table', rows=result)
# #     return output
