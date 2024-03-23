import os

from .base import BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, '.env'))
from .base import *
