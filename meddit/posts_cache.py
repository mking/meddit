from meddit.post import Post

class PostsCache:
    def __init__(self, cache, prefix):
        self.cache = cache
        self.prefix = prefix

    def create(self, id, author, gif_id, created, votes):
        self.cache.hset(f'{self.prefix}:posts:{id}', 'author', author)
        self.cache.hset(f'{self.prefix}:posts:{id}', 'gif_id', gif_id)
        self.cache.hset(f'{self.prefix}:posts:{id}', 'created', str(created))
        self.cache.hset(f'{self.prefix}:posts:{id}', 'votes', str(votes))
        self.cache.zadd(f'{self.prefix}:posts_created', str(created), id)

    def delete(self, id):
        self.cache.delete(f'{self.prefix}:posts:{id}')
        self.cache.zrem(f'{self.prefix}:posts_created', id)

    def update_votes(self, id, amount):
        self.cache.hincrby(f'{self.prefix}:posts:{id}', 'votes', amount)

    def get(self, id):
        post = self.cache.hgetall(f'{self.prefix}:posts:{id}')
        return Post(
            id=id,
            author=post['author'],
            gif_id=post['gif_id'],
            created=int(float(post['created'])),
            votes=int(post['votes']),
        )

    def exists(self, id):
        return self.cache.exists(f'{self.prefix}:posts:{id}')

    def recent(self, limit):
        ids = self.cache.zrevrangebyscore(f'{self.prefix}:posts_created', max=float('Inf'), min=float('-Inf'), start=0, num=limit)
        return [self.get(id) for id in ids]
