import logging
logger = logging.getLogger('Redis')

import redis
from redis.retry import Retry
from redis.backoff import ExponentialWithJitterBackoff
from redis.cache import CacheConfig, CacheInterface
import os

HOST = os.getenv('REDIS_HOST')
if not HOST:
    raise RuntimeError('missing "REDIS_HOST" env var')

PORT = os.getenv('REDIS_PORT')
if not PORT:
    raise RuntimeError('missing "REDIS_PORT" env var')

DB = os.getenv('REDIS_DB')
if not DB:
    raise RuntimeError('missing "REDIS_DB" env var')

PORT = int(PORT)
DB = int(DB)

class Redis:
    _client: redis.Redis

    #use socket as connectionPool class
    #check if protocol 3 is better
    #adjust the retry policy
    #single connection client?
    #adjust retry on error
    #decode_response?

    #consistency on redis through pipeline (like db tx) or setup a lock/maplock with redis?

    #update the value after each execution of payment (lock, read, update, unlock)
    #or
    #after amount of times (local_counter += 1... then after x minutes update redis counter (lock, read, update, unlock))?
    #for this second option, we would have to stop reading and processing messages after the redis update and until before the summary check
    #and after the summary check, we can handle the messages again. The strategy would be using a lock for the summary-check
    #if the lock is off (summary checked), local_counter=0, we can handle messages, and when it's on (after current instance redis update and until before summary check happens), we wait.

    #make the API also use the redis lock/maplock to read?



    #singleton and on repo do 'from lib.redis import Redis' then 'Redis().get()' or 'Redis().execute()' or 'Redis.get()'?
    #or
    #dependency injection through a repo initializer receiving the instance of database to use, then 'self.redis.get()' or 'self.db.get()'

    def __init__(self) -> None:
        self._client = redis.Redis(
            host=HOST,
            port=PORT,
            db=DB,
            connection_pool=redis.ConnectionPool(
                connection_class=redis.UnixDomainSocketConnection(
                    host=HOST,
                    port=PORT,
                    db=DB,
                ),
            ),
            decode_responses=False,
            max_connections=None,
            single_connection_client=False,
            retry_on_timeout=False,
            retry_on_error=None,
            retry=Retry(
                backoff=ExponentialWithJitterBackoff(base=1, cap=10),
                retries=3,
            ),
            protocol=3,
        )

    def __del__(self):
        self._client.close()
