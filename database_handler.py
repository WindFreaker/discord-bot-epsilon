import os
import pymysql
from critical_errors import dm_error_report

host = os.getenv('DISCORD_DB_HOST')
username = os.getenv('DISCORD_DB_USERNAME')
password = os.getenv('DISCORD_DB_PASSWORD')
database = os.getenv('DISCORD_DB_NAME')
db = pymysql.connect(host, username, password, database)
csr = db.cursor()


# returns a list of all extensions enabled
def list_enabled_extensions():
    csr.execute(f'SELECT extension_name FROM global_extensions')
    db_results = csr.fetchall()
    extension_list = []
    for result in db_results:
        extension_list.append(result[0])
    return extension_list


# writes into the database if an extension is disabled or not
# this allows for the disabling/enabling or extensions to persist between restarts
def save_extension_state(name, new_state):
    list = list_enabled_extensions()
    if name in list and not new_state:  # extension enabled and new_state is disabled
        csr.execute(f'DELETE FROM global_extensions WHERE extension_name="{name}"')
        db.commit()
    elif name not in list and new_state:  # extension disabled and new_state is enabled
        csr.execute(f'INSERT INTO global_extensions (extension_name) VALUES ("{name}")')
        db.commit()
    else:  # extension already in desired state (throw error?)
        print('A critical error with database_handler has been found! #8921986')


# TODO close the database (not an issue rn afaik but is important overall)
