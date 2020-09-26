import tqdm

import subprocess
from scholarly import scholarly
from tor import TorInstance
from stem.control import Controller
from stem import Signal
import socks
import socket

# Import framework
from flask import Flask, jsonify
from flask_restful import Resource, Api, request

class Getter(object):
    def __init__(self, port):
        publications = []
        tor_instance = TorInstance(port, 'scholarly_password')
        self.port = int(port)

    def get(self, queries):

        publications = []
        with Controller.from_port(port = self.port) as controller:
            controller.authenticate('scholarly_password')
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            for query in queries:
                found = False
                limit = 1
                while not found:
                    try:
                        response = scholarly.search_pubs(query)
                        found = True
                    except Exception as e:
                        while True:
                            if controller.is_newnym_available():
                                print("Refreshing Tor Node...")
                                controller.signal(Signal.NEWNYM)
                                break

                elem = 1
                count = 0
                while (elem is not None) and (count < limit):
                    elem = next(response, None)
                    info = elem.bib
                    # pub = Publication(info)
                    print(type(info))
                    publications.append(info)

                    count += 1

        return publications


# Instantiate the app
app = Flask(__name__)
api = Api(app)

class Researcher(Resource):
    def get(self):
        queries= request.args.getlist('queries')

        getter = Getter('9051')

        pubs = getter.get(queries)

        response = {
            'publications': pubs
        } 
        return jsonify(response)

# Create routes
api.add_resource(Researcher, '/')

# Run the application
if __name__ == '__main__':
    # TODO: Remove on deployment 
    app.run(host='0.0.0.0', port=80, debug=True)