from flask import Flask, jsonify, request
import logging
import http.client
from redis import StrictRedis
from uuid import uuid4
from datetime import datetime
from meddit.posts import PostCache

http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)

cache = StrictRedis(host='localhost', port=6379, db=0)
post_cache = PostCache(cache)
app = Flask(__name__)

@app.route('/posts', methods=['POST'])
def create_post():
    id = str(uuid4())
    author = request.get_json()['author']
    created = datetime.now().timestamp()
    votes = 1
    post_cache.create(id, author, created, votes)
    return jsonify({
        'success': True,
    })

@app.route('/posts/:id', methods=['DELETE'])
def delete_post():
    id = request.args.get('id')
    post_cache.delete(id)
    return jsonify({
        'success': True,
    })

@app.route('/posts/:id', methods=['PUT'])
def update_post():
    id = request.args.get('id')
    votes = request.get_json()['votes']
    post_cache.update_votes(id, votes)
    return jsonify({
        'success': True,
    })

@app.route('/posts/:id', methods=['GET'])
def get_post():
    id = request.args.get('id')
    post = post_cache.get(id)
    return jsonify(post)

@app.route('/posts/recent', methods=['GET'])
def get_recent():
    posts = post_cache.get_recent()
    return jsonify(posts)
