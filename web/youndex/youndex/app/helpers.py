import re

from app import redis_client


def get_search_is_running(user_id):
    v = redis_client.get('search_count' + user_id)
    return v and int(v) > 0


def set_search_is_running(user_id):
    redis_client.set('search_count' + user_id, 1)


def set_search_runned(user_id):
    redis_client.set('search_count' + user_id, 0)


def validate_url(url):
    bad = ['127.0.0', 'localhost', "::1", '0.0.0.0']
    for x in bad:
        if x in url:
            return False

    regexp = r'^https?:\/\/[\w.:\/]+'
    return re.match(regexp, url)
