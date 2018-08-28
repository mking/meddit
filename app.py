from flask import Flask, jsonify, request, abort, Response
import logging
import http.client
from redis import StrictRedis
from uuid import uuid4
from datetime import datetime
from meddit.posts import PostCache, PostJSONEncoder
import json

http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)

cache = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
post_cache = PostCache(cache)
app = Flask(__name__)
app.json_encoder = PostJSONEncoder

@app.errorhandler(400)
def bad_request(e):
    return Response(
        response=json.dumps({
            'success': False,
            'message': e.description,
        }),
        status=400,
        mimetype='application/json'
    )

@app.errorhandler(404)
def not_found(e):
    return Response(
        response=json.dumps({
            'success': False,
            'message': e.description,
        }),
        status=404,
        mimetype='application/json'
    )

@app.route('/posts', methods=['POST'])
def create():
    id = str(uuid4())
    author = request.get_json()['author']
    gif_id = request.get_json()['gif_id']
    created = int(datetime.now().timestamp())
    votes = 1
    post_cache.create(id, author, gif_id, created, votes)
    return jsonify({
        'success': True,
    })

@app.route('/posts/<id>', methods=['DELETE'])
def delete(id):
    if not post_cache.exists(id):
        abort(404, 'Missing post')

    post_cache.delete(id)
    return jsonify({
        'success': True,
    })

@app.route('/posts/<id>/votes', methods=['PUT'])
def update_votes(id):
    amount = request.get_json()['amount']
    if amount not in [-1, 1]:
        abort(400, 'Invalid amount')

    if not post_cache.exists(id):
        abort(404, 'Missing post')

    post_cache.update_votes(id, amount)
    return jsonify({
        'success': True,
    })

@app.route('/posts/<id>', methods=['GET'])
def get(id):
    if not post_cache.exists(id):
        abort(404, 'Missing post')

    post = post_cache.get(id)
    return jsonify(post)

@app.route('/posts/recent', methods=['GET'])
def recent():
    limit = request.args.get('limit', 10)
    posts = post_cache.recent(limit)
    return jsonify(posts)
