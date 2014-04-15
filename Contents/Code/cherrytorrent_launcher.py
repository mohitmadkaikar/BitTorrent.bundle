###############################################################################
import cherrytorrent
import urllib2

###############################################################################
HTTP_PORT = 8042

###############################################################################
def start_cherrytorrent():
    Thread.Create(thread_proc)

###############################################################################
def thread_proc():
    class CustomLoggerStream:
        def __init__(self, port):
            self.port = port

        def write(self, str):
            Log.Info('[BitTorrent][cherrytorrent][{0}] {1}'.format(self.port, str.rstrip()))

        def flush(self):
            pass

    while True:
        if not get_server_status(HTTP_PORT):
            http_config = {
                            'port': HTTP_PORT
                          }

            torrent_config = {
                                'port':                 int(Prefs['INCOMING_PORT']),
                                'max_download_rate':    int(Prefs['MAX_DOWNLOAD_RATE']),
                                'max_upload_rate':      int(Prefs['MAX_UPLOAD_RATE']),
                                'keep_files':           Prefs['KEEP_FILES']
                             }
            
            server = cherrytorrent.Server(http_config, torrent_config, CustomLoggerStream(HTTP_PORT))
            server.run()

###############################################################################
def get_server_status(port):
    try:
        status_json = JSON.ObjectFromURL('http://{0}:{1}'.format(Network.Address, port), cacheTime=0)
        return status_json
    except urllib2.URLError as exception:
        Log.Error('[BitTorrent][cherrytorrent][{0}] Server unreachable: {1}'.format(port, exception.reason))
    except Exception as exception:
        Log.Error('[BitTorrent][cherrytorrent][{0}] Unhandled exception: {1}'.format(port, exception))

    return None