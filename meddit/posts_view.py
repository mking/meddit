from flask_classy import FlaskView, route
from flask import request, jsonify, abort
from uuid import uuid4
from meddit.globals import get_post_cache
from datetime import datetime

class PostsView(FlaskView):
    route_base = '/posts/'

    def post(self):
        id = str(uuid4())
        author = request.get_json()['author']
        gif_id = request.get_json()['gif_id']
        created = int(datetime.now().timestamp())
        votes = 1
        get_post_cache().create(id, author, gif_id, created, votes)
        return jsonify({
            'success': True,
        })

    def delete(self, id):
        if not get_post_cache().exists(id):
            abort(404, 'Missing post')

        get_post_cache().delete(id)
        return jsonify({
            'success': True,
        })

    @route('/<id>/votes', methods=['PUT'])
    def update_votes(self, id):
        amount = request.get_json()['amount']
        if amount not in [-1, 1]:
            abort(400, 'Invalid amount')

        if not get_post_cache().exists(id):
            abort(404, 'Missing post')

        get_post_cache().update_votes(id, amount)
        return jsonify({
            'success': True,
        })

    def get(self, id):
        if not get_post_cache().exists(id):
            abort(404, 'Missing post')

        post = get_post_cache().get(id)
        return jsonify(post)

    @route('/recent')
    def recent(self):
        limit = request.args.get('limit', 10)
        posts = get_post_cache().recent(limit)
        return jsonify(posts)
