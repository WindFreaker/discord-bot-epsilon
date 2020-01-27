import os
import dropbox
import sys
from dropbox import files

dbx = None
dropbox_switch = False

if os.getenv('DROPBOX_ACCESS_TOKEN') is not None:
    print('⚠ Dropbox access token found. Dropbox extension storage has been enabled. ⚠')
    dropbox_switch = True
    dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'))


def download_extension(name):
    if dropbox_switch:
        try:
            dbx.files_download_to_file('extensions/' + name + '.py', '/' + name + '.py')
        except FileNotFoundError:
            os.mkdir('extensions')
            download_extension(name)


def read_config(name):
    if dropbox_switch:
        metadata, f = dbx.files_download('/' + name + '.cfg')
        name_list = []
        for item in f.content.split():
            name_list.append(str(item)[2:-1])
        return name_list
    return []


def edit_config(file, item):
    if dropbox_switch:
        existing_lines = read_config(file)
        try:
            index = existing_lines.index(item)
            existing_lines.pop(index)
        except ValueError:
            existing_lines.append(item)
        new_lines = ''
        for line in existing_lines:
            new_lines += line + '\n'
        dbx.files_upload(str.encode(new_lines), '/' + file + '.cfg', mode=files.WriteMode.overwrite)
