import requests
import os
import zipfile

from mod.pull import pull_data
from mod.json import update_data


def update_config(pull, update):
    if pull:
        pull_data()

    if update:
        update_data()
