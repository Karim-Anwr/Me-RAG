# src/models/BaseDataModel.py

from helpers import config
from helpers.config import Settings, get_settings

class BaseDataModel:
    def __init__(self ,db_client: object):
        self.settings = config.get_settings()
        self.db_client = db_client
        self.app_settings = get_settings() 
