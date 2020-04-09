import os
import dropbox


dbx_token = os.getenv('DROPBOX_ACCESS_TOKEN')
dbx = None
dropbox_switch = False

if dbx_token is not None:
    print('DROPBOX_ACCESS_TOKEN found, extension storage has been enabled')
    dropbox_switch = True
    dbx = dropbox.Dropbox(dbx_token)


def download_extension(name):
    if dropbox_switch:
        try:
            dbx.files_download_to_file('extensions/' + name + '.py', '/' + name + '.py')
        except FileNotFoundError:  # should only trigger when the folder 'extensions' is missing
            os.mkdir('extensions')
            download_extension(name)


"""
def read_config(name, section):
    if dropbox_switch:
        metadata, file = dbx.files_download('/' + name + '.ini')
        config = configparser.ConfigParser()
        config.read(file)
        print(file)
        return config[section]
    return []


def edit_config(file, section, item, value):
    if dropbox_switch:
        config = read_config(file, section)
        print(config)
        config[item] = value
        print(config)
        # dbx.files_upload(str.encode(new_lines), '/' + file + '.ini', mode=files.WriteMode.overwrite)
"""