import flask
from flask import jsonify

from .. import settings
from ..dkr import dkr


def container_api(app: flask.app.Flask):

    @app.route('/containers', methods=["GET"])
    def list_containers():
        containers = dkr.list_containers()
        #mapped = list(map(lambda x: x.attrs, containers))

        mapped = list()
        for container in containers:
            mapped.append(container.attrs)

        return jsonify(mapped)


    @app.route('/container/<string:key>', methods=["GET"])
    def describe_container(key):
        return jsonify(dkr.get_container(key).attrs)


    @app.route('/containers/restart', methods=["POST"])
    def restart_all_containers():
        return jsonify(dkr.restart_all_containers())


    @app.route('/container/start/<string:key>', methods=["POST"])
    def start_container(key):
        return jsonify(dkr.start_container(key).attrs)


    @app.route('/container/stop/<string:key>', methods=["POST"])
    def stop_container(key):
        return jsonify(dkr.stop_container(key).attrs)


    @app.route('/container/remove/<string:key>', methods=["POST"])
    def remove_container(key):
        if settings.AGENT_ENABLE_DELETE:
            return jsonify(dkr.remove_container(key).attrs)

        return jsonify(dkr.remove_container(key).attrs)


    @app.route('/container/restart/<string:key>', methods=["POST"])
    def restart_container(key):
        return jsonify(dkr.restart_container(key).attrs)
