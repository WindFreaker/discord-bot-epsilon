import os
import pymysql
from inspect import getframeinfo, stack


class database_connection:

    def __init__(self):
        host = os.getenv('DISCORD_DB_HOST')
        username = os.getenv('DISCORD_DB_USERNAME')
        password = os.getenv('DISCORD_DB_PASSWORD')
        database = os.getenv('DISCORD_DB_NAME')
        self.db = pymysql.connect(host, username, password, database)
        self.csr = self.db.cursor()

    def __enter__(self):
        return self.csr

    def __exit__(self, *exc_info):
        del exc_info
        self.db.commit()
        self.db.close()


# returns a list of all extensions enabled
def list_enabled_extensions():
    with database_connection() as csr:
        csr.execute(f'SELECT extension_name FROM global_extensions')
        db_results = csr.fetchall()
        extension_list = []
        for result in db_results:
            extension_list.append(result[0])
        return extension_list


# writes into the database if an extension is disabled or not
# this allows for the disabling/enabling or extensions to persist between restarts
def save_extension_state(name, new_state):
    with database_connection() as csr:
        list = list_enabled_extensions()
        if name in list and not new_state:  # extension enabled and new_state is disabled
            csr.execute(f'DELETE FROM global_extensions WHERE extension_name = "{name}"')
        elif name not in list and new_state:  # extension disabled and new_state is enabled
            csr.execute(f'INSERT INTO global_extensions (extension_name) VALUES ("{name}")')
        else:  # extension already in desired state (throw error?)
            print('A critical error with database_handler has been found! #8921986')


class GuildConfig:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.extension_name = os.path.split(getframeinfo(stack()[1][0]).filename)[1][0:-3]

    def set_value_for_key(self, key, value):
        print("something")

    def add_value_to_key(self, key, value):
        print("something again")

    def remove_value_from_key(self, key, value):
        print("not something")


"""
def modify_guild_config(guild_id, key, value):
    affected_rows = csr.execute(f'UPDATE guild_config SET value = "{value}" WHERE guild_id = {guild_id} '
                                f'AND extension_name = "{extension_name}" AND config_key = "{key}"')
    if affected_rows == 0:
        csr.execute(f'SELECT value FROM guild_config WHERE guild_id = {guild_id} AND '
                    f'extension_name = "{extension_name}" AND config_key = "{key}"')
        current_value = csr.fetchall()
        if len(current_value) == 0:
            csr.execute(f'INSERT INTO guild_config (guild_id, extension_name, config_key, value) VALUES '
                        f'({guild_id}, "{extension_name}", "{key}", "{value}")')
    db.commit()
"""

# TODO close the database (not an issue rn afaik but is important overall)
