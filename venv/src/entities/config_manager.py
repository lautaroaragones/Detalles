
import configparser
import sys
import os


class ConfigManager(object):

    dynamic_conf = {}

    @staticmethod
    def get_key():
        return "configmanager_config"

    @staticmethod
    def get_raw_config():
        key = ConfigManager.get_key()
        config = configparser.ConfigParser()

        if(os.getcwd().find("src") != -1):
            #Sirve para mi entorno local
            config.read(os.getcwd()+'/config.ini')
        else:
            # Sirve para la ejucion en el bat
            config.read(os.getcwd() + '/src/config.ini')
        return config

    @staticmethod
    def get_value(section,key):
        try:
            config = ConfigManager.get_raw_config()
            value = config.get(section, key)
        except:
            value = ''
        return value

    @staticmethod
    def set_dyn_value(key, value):
        ConfigManager.dynamic_conf[key] = value

    @staticmethod
    def get_dyn_value(key):
        return ConfigManager.dynamic_conf[key]
