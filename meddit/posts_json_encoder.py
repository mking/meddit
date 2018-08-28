from flask.json import JSONEncoder
from meddit.post import Post

class PostsJSONEncoder(JSONEncoder):
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
