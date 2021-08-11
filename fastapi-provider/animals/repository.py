import abc
from tinydb import TinyDB, Query

class AbstractRepository(abc.ABC):

  @property
  def count(self):
    return len(self.list())

  @abc.abstractmethod
  def clear(self):
    pass

  @abc.abstractmethod
  def list(self):
    pass

  def search(self, predicate):
    result = filter(predicate, self.list())
    return list(result)

  def list_available(self):
    return self.search(lambda a: a['eligibility']['available'])

  @abc.abstractmethod
  def get(self, id):
    pass

  @abc.abstractmethod
  def add(self, entity):
    pass

class TinyDbRepository(AbstractRepository):

  @property
  def count(self):
    return len(self.animals)

  def __init__(self, db_path):
    self.db = TinyDB(db_path)
    self.animals = self.db.table('animals')
    self.query = Query()

  def clear(self):
    self.animals.truncate()

  def list(self):
    return self.animals.all()

  def get(self, id):
    return self.animals.get(self.query.id == int(id))

  def add(self, entity):
    data = dict(entity)
    data['id'] = self.count + 1
    data['location'] = dict(data['location'])
    data['eligibility'] = dict(data['eligibility'])
    self.animals.insert(data)
    return data



def import_all(animals, repository:AbstractRepository):
  repository.clear()
  id = repository.count
  for animal in animals:
    id += 1
    animal['id'] = id
    repository.add(animal)


