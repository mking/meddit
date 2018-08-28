import logging
import http.client
from flask import Flask
from meddit.posts_json_encoder import PostsJSONEncoder
from meddit.posts_view import PostsView
from meddit.error_handlers import define_error_handlers

http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.json_encoder = PostsJSONEncoder
PostsView.register(app)
define_error_handlers(app)
