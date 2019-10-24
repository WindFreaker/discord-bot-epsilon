import os
import dropbox

dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'))


def download_extension(name):
    try:
        dbx.files_download_to_file('extensions/' + name + '.py', '/' + name + '.py')
    except FileNotFoundError:
        os.mkdir('extensions')
        download_extension(name)


def read_config(name):
    metadata, f = dbx.files_download('/' + name + '.cfg')
    return f.content.split()
