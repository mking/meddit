from meddit.constants import CACHE_PREFIX
from flask.json import JSONEncoder

class Post:
    def __init__(self, id, author, gif_id, created, votes):
        self.id = id
        self.author = author
        self.gif_id = gif_id
        self.created = created
        self.votes = votes

class PostCache:
    def __init__(self, cache):
        self.cache = cache

    def create(self, id, author, gif_id, created, votes):
        self.cache.hset(f'{CACHE_PREFIX}:posts:{id}', 'author', author)
        self.cache.hset(f'{CACHE_PREFIX}:posts:{id}', 'gif_id', gif_id)
        self.cache.hset(f'{CACHE_PREFIX}:posts:{id}', 'created', str(created))
        self.cache.hset(f'{CACHE_PREFIX}:posts:{id}', 'votes', str(votes))
        self.cache.zadd(f'{CACHE_PREFIX}:posts_created', str(created), id)

    def delete(self, id):
        self.cache.delete(f'{CACHE_PREFIX}:posts:{id}')
        self.cache.zrem(f'{CACHE_PREFIX}:posts_created', id)

    def update_votes(self, id, amount):
        self.cache.hincrby(f'{CACHE_PREFIX}:posts:{id}', 'votes', amount)

    def get(self, id):
        post = self.cache.hgetall(f'{CACHE_PREFIX}:posts:{id}')
        print(post)
        return Post(
            id=id,
            author=post['author'],
            gif_id=post['gif_id'],
            created=int(float(post['created'])),
            votes=int(post['votes']),
        )

    def exists(self, id):
        return self.cache.exists(f'{CACHE_PREFIX}:posts:{id}')

    def recent(self, limit):
        ids = self.cache.zrevrangebyscore(f'{CACHE_PREFIX}:posts_created', max=float('Inf'), min=float('-Inf'), start=0, num=limit)
        print(ids)
        return [self.get(id) for id in ids]

class PostJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Post):
            return {
                'id': obj.id,
                'author': obj.author,
                'gif_id': obj.gif_id,
                'created': obj.created,
                'votes': obj.votes,
            }
        return super().default(obj)
