from pathlib import Path

BASE_PATH = Path(__file__).parent.parent

DATABASE_URL = 'sqlite:///db.sqlite3'

DATABASE_FILE = BASE_PATH / '..' / 'db.json'
SAMPLE_DATA_FILE = BASE_PATH / '..' / 'e2e' / 'data' / 'animalData.json'

valid_tokens = []
