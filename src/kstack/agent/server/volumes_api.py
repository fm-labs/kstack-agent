import flask
from flask import jsonify

from kstack.agent.docker.dkr import dkr

def volumes_api(app: flask.app.Flask):

    @app.route('/volumes', methods=["GET"])
    def list_volumes():
        """
        List all volumes

        Optional query parameters:
        - size: true/false (default: false) True to include size information
        - in_use: true/false (default: false) True to include in-use information

        :return:
        """
        query = flask.request.args
        check_size = query.get('size', 'true') == 'true'
        check_in_use = query.get('in_use', 'true') == 'true'

        volumes = dkr.list_volumes(check_in_use=check_in_use, check_size=check_size)
        mapped = list(map(lambda x: x.attrs, volumes))
        return jsonify(mapped)
