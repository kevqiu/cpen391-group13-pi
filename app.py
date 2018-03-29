import sys
from server import server
from server.setup import init_db, nuke_server

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-db':
            init_db()
        elif sys.argv[1] == '-nuke':
            nuke_server()
    else:
        server.create_app().run(host='0.0.0.0')
