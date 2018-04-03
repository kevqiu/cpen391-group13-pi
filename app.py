import sys
from server import server
from server.setup import init_db, nuke_server


"""
Entry point to the Server
Arguments: 
    -db
        initializes the database tables and inserts base data
    -nuke
        deletes all files in the images folder and resets the database 
"""
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-db':
            init_db()
        elif sys.argv[1] == '-nuke':
            nuke_server()
    else:
        server.create_app().run(host='0.0.0.0', threaded=True)
