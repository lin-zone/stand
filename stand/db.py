from random import shuffle
from threading import Lock

from peewee import *

from stand.config import STAND_DB


class Cache(list):
    lock = Lock()

    def extend(self, iterable):
        self.lock.acquire()
        try:
            super().extend(iterable)
        except Exception as e:
            raise e
        finally:
            self.lock.release()

    def pop(self, index=-1):
        self.lock.acquire()
        try:
            return super().pop(index)
        except Exception as e:
            raise e
        finally:
            self.lock.release()


_proxies = Cache()       # 单例对象, 缓存从数据库获取的代理IP


class EmptyError(Exception):
    """代理池无有效IP"""


class ProxyPool(Model):
    proxy = CharField(max_length=30, unique=True)
    score = SmallIntegerField()


class SqliteDB:
    MIN_SCORE = 0
    INIT_SCORE = 2
    MAX_SCORE = 3
    model = ProxyPool

    def __init__(self):
        self._db = self.model._meta.database = SqliteDatabase(STAND_DB, check_same_thread=False)
        self.model.create_table()
    
    def add(self, proxy):
        try:
            self.model.create(proxy=proxy, score=self.INIT_SCORE)
        except IntegrityError:
            print(f'{proxy} dumplicate')

    def all(self):
        return self._get_proxies(self.MIN_SCORE + 1)

    def len(self, score=None):
        if score is None:
            score = self.MAX_SCORE
        else:
            score = int(score)
        return len(self._get_proxies(score))

    def max_score(self, proxy):
        self.model.update(score=self.MAX_SCORE).where(self.model.proxy == proxy).execute()

    def decrease_score(self, proxy):
        self.model.update(score=self.model.score - 1).where(self.model.proxy == proxy).execute()

    def clean(self):
        self.model.delete().where(self.model.score <= self.MIN_SCORE).execute()

    def close(self):
        self._db.close()

    def _get_proxies(self, min_score):
        result = (self.model
                      .select()
                      .where(self.model.score >= min_score)
                      .order_by(self.model.score.desc()))
        return [p.proxy for p in result]

    def random(self):
        global _proxies
        if len(_proxies) == 0:
            _proxies.extend(self._get_proxies(self.MAX_SCORE))
            shuffle(_proxies)
        try:
            return _proxies.pop()
        except IndexError:
            raise EmptyError('代理池无有效IP')


_db = None


def get_proxy():
    global _db
    if _db is None:
        _db = SqliteDB()
    return _db.random()