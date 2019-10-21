import os
import dropbox

dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'))


def download_extension(name):
    dbx.files_download_to_file('extensions/' + name + '.py', '/' + name + '.py')


def read_config(name):
    metadata, f = dbx.files_download('/' + name + '.cfg')
    return f.content.split()
