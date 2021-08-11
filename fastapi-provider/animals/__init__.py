from .repository import TinyDbRepository
from . import config as conf
import json

repository = TinyDbRepository(conf.DATABASE_FILE)
