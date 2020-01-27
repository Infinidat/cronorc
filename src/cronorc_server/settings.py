# load the base settings
from .base_settings import *

# load the custom settings
from . import PROJECTROOT
from os import path
from imp import load_source

LOCAL_SETTINGS_PATH = path.join(PROJECTROOT, 'data', 'settings.py')
try:
    load_source("local_settings_module", LOCAL_SETTINGS_PATH)
    from local_settings_module import *
except IOError as error:
    import logging
    logging.warning('Local settings not found at %s', LOCAL_SETTINGS_PATH)
