import os.path
import json

import pdb


# Get config
config_file = file(os.path.join(os.path.dirname(__file__),
                                'config.json'),
                    'r')
config = json.loads(config_file.read())
config_file.close()
