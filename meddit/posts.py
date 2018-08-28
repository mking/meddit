from meddit.constants import CACHE_PREFIX

class Post:
    def __init__(self, id, author, created, votes):
        self.id = id
        self.author = author
        self.created = created
        self.votes = votes

class PostCache:
    def __init__(self, cache):
        self.cache = cache

    def create(self, id, author, created, votes):
        self.cache.hset(f'{CACHE_PREFIX}:posts:{id}', 'author', author)
        self.cache.hset(f'{CACHE_PREFIX}:posts:{id}', 'created', str(created))
        self.cache.hset(f'{CACHE_PREFIX}:posts:{id}', 'votes', str(votes))
        self.cache.zadd(f'{CACHE_PREFIX}:posts_created', str(created), id)

    def delete(self, id):
        self.cache.delete(f'{CACHE_PREFIX}:posts:{id}')
        self.cache.zrem(f'{CACHE_PREFIX}:posts_created', id)

    def update_votes(self, id, votes):
        self.cache.hset(f'{CACHE_PREFIX}:posts:{id}', 'votes', str(votes))

    def get(self, id):
        post_dict = self.cache.hgetall(f'{CACHE_PREFIX}:posts:{id}')
        return Post(
            id=id,
            author=post_dict['author'],
            created=int(post_dict['created']),
            votes=int(post_dict['votes']),
        )

    def get_recent(self, limit):
        ids = self.cache.zrevrangebyscore(f'{CACHE_PREFIX}:posts_created', num=limit)
        return [self.get(id) for id in ids]
