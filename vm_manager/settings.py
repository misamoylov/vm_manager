# coding=utf-8
import os

_boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                   '0': False, 'no': False, 'false': False, 'off': False}

# Path to VM images
IMAGES_PATH = os.environ.get("IMAGES_PATH")
