import json
from . import repository
from .repository import import_all
from . import config as conf

class FixtureManager:

  def __init__(self):
    self.state_handlers = {
      'Has some animals': self.set_sample_data,
      'Has no animals': self.set_empty_data,
      'Has an animal with ID 1': self.set_sample_data,
      'Is not authenticated': self.set_not_authenticated,
    }

  def set_sample_data(self):
    repository.clear()
    with open(conf.SAMPLE_DATA_FILE, 'r') as f:
      import_all(json.load(f), repository)
    conf.valid_tokens = ['token']
    return "Sample data loaded"

  def set_empty_data(self):
    repository.clear()
    conf.valid_tokens = ['token']
    return "Set to empty data"

  def set_not_authenticated(self):
    conf.valid_tokens = []
    return "Set to not authenticated"

  def set(self, state):
    if state not in self.state_handlers:
      return f"'{state}' is not a valid state."
    return self.state_handlers[state]()
  
manager = FixtureManager()
