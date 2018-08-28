from flask import Response
import json

def define_error_handlers(app):
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
