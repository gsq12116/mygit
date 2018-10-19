import random
import re

import redis

from util.setting import DATABASES, REDIS


def is_graph(filename):
    res = r'.*\.(jpg|png|bmp|jpeg|emf|ico)'
    result = re.fullmatch(res, filename)
    if result:
        return True
    else:
        return False


def image_code():
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    image_code = ""
    for _ in range(4):
        image_code += random.choice(s)
    return image_code


def get_mysql_url():
    default_database = DATABASES['default']
    return '{}+{}://{}:{}@{}:{}/{}'.format(default_database['DRIVER'],
                                           default_database['DH'],
                                           default_database['USER'],
                                           default_database['PASSWORD'],
                                           default_database['HOST'],
                                           default_database['PORT'],
                                           default_database['NAME'])


def get_redis_url():
    result = redis.Redis(host=REDIS['HOST'], port=REDIS['PORT'])
    return result