from typing import Dict, List, Optional

import redis

from strideutils.stride_config import config

redis_dbs = {}  # stores the redis dbs so we don't have to keep reconnecting


def get_redis_db(redis_db_name: str) -> redis.Redis:
    """
    Returns the redis db specified by redis_db_name.

    Currently supports 'public', 'frontend', and 'backend' dbs.
    """
    if redis_db_name not in redis_dbs:
        if redis_db_name == 'public':
            r = redis.Redis(
                host='usw1-certain-beagle-33773.upstash.io',
                port=33773,
                password=config.UPSTASH_PUBLIC_PASSWORD,
            )

        elif redis_db_name == 'frontend':
            r = redis.Redis(
                host='usw1-hot-bat-33320.upstash.io',
                port=33320,
                password=config.UPSTASH_STRIDE_FRONTEND_PASSWORD,
                ssl=True,
            )

        elif redis_db_name == 'backend':
            r = redis.Redis(
                host='usw1-mutual-mule-33971.upstash.io',
                port=33971,
                password=config.UPSTASH_STRIDE_BACKEND_PASSWORD,
                ssl=True,
            )
        elif redis_db_name == 'dydx':
            r = redis.Redis(
                host='us1-diverse-dog-39216.upstash.io',
                port=39216,
                password=config.UPSTASH_STRIDE_DYDX_PUBLIC_PASSWORD,
                ssl=True,
            )
        elif redis_db_name == 'dydx_airdrop':
            r = redis.Redis(
                host='pleasant-pipefish-54904.upstash.io',
                port=6379,
                password=config.UPSTASH_STRIDE_DYDX_AIRDROP_PASSWORD,
                ssl=True,
            )
        elif redis_db_name == "milestones":
            r = redis.Redis(
                host='adapting-snail-56076.upstash.io',
                port=6379,
                password=config.UPSTASH_STRIDE_MILESTONES_PASSWORD,
                ssl=True,
            )
        else:
            raise ValueError(f'Invalid Redis DB: {redis_db_name}')

        redis_dbs[redis_db_name] = r

    return redis_dbs[redis_db_name]


def get(redis_key: str, db_name='frontend') -> Optional[str]:
    """
    This function will read the given Redis key and return the value.

    Pulls from the specified redis db.
    """
    db = get_redis_db(db_name)
    value = db.get(redis_key)

    return value.decode('utf-8') if value is not None else None


def get_multiple_keys(redis_keys: List[str], db_name='frontend') -> List[Optional[str]]:
    """
    This function will read multiple keys in at once.
    Value will be "None" if the key does not exist.

    Pulls from the specified redis db.
    """
    db = get_redis_db(db_name)
    values = db.mget(redis_keys)

    return [value.decode('utf-8') if value is not None else None for value in values]


def get_all_keys(db_name='dydx_airdrop') -> List[str]:
    """
    This function will return all keys in the redis db specified.
    """
    db = get_redis_db(db_name)

    out = []

    cursor = '0'
    while cursor != 0:
        cursor, keys = db.scan(cursor, count=1000)
        if keys:
            out.extend(keys)
    return [key.decode('utf-8') for key in out]


def set(redis_key: str, redis_val: str, db_name='frontend'):
    """
    This function will set the given key to value in the redis_db specified.
    """
    db = get_redis_db(db_name)
    db.set(redis_key, redis_val)


def set_keys(dict_to_upload: Dict[str, str], db_name='frontend', prefix=''):
    """
    Loops through all values in dict_to_upload and sets the keys+values in the redis db

    Will append "prefix" to all keys in the dict.
    """
    db = get_redis_db(db_name)
    pipe = db.pipeline()
    for k, v in dict_to_upload.items():
        pipe.set(prefix + k, v)
    pipe.execute()
