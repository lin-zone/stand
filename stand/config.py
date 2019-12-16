import os


STAND_DIR = os.environ.get('STAND_DIR') or os.path.abspath(os.path.dirname(__name__))
STAND_DB = os.path.join(STAND_DIR, 'stand.db')
CRAWLER_LOG = os.path.join(STAND_DIR, 'crawler.log')
VALIDATOR_LOG = os.path.join(STAND_DIR, 'validator.log')