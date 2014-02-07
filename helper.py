import os.path
import json

import pdb


# Get config
config_file = file(os.path.join(os.path.dirname(__file__),
                                'config.json'), 'r')
CONFIG = json.loads(config_file.read())
config_file.close()


# Help functions

def HELP_snippet_trunc(text_string):
    return text_string[:30]
