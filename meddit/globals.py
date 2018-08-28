from flask import g
from meddit.posts_cache import PostsCache
from redis import StrictRedis

CACHE_PREFIX = 'meddit'

def get_cache():
    if not hasattr(g, 'cache'):
        g.cache = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    return g.cache

def get_post_cache():
    if not hasattr(g, 'post_cache'):
        g.posts_cache = PostsCache(get_cache(), CACHE_PREFIX)
    return g.posts_cache
