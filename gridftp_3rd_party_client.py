import os

import cherrypy

class ImgTransfer(object):

    back = " <a href='index'>Back to the index page</a>"   
    not_connect_notify = "There is no connection. Please connect a server.<br>"
 
    @cherrypy.expose
    def index(self):
        if "server" not in cherrypy.session or cherrypy.session['server'] == "":
            server_notify = "<h3>No server is connected</h3>"
        else:
            server_notify = "<h3>Server is connected: " + cherrypy.session['server'] + "</h3>"
        
        return """<html>
        <head><title>Image Transfer</title></head>
        <body>""" + server_notify + """
          <button type="button" onclick="location.href='send'">Send</button>
          <button type="button" onclick="location.href='receive'">Receive</button>
          <button type="button" onclick="location.href='connect'">Connect</button>
        </body></html>"""

    @cherrypy.expose
    def send(self):
        if 'server' not in cherrypy.session:
            return self.not_connect_notify + self.back
        else:
            return """<html>
        <head><title>Image Send</title></head>
        <body>
          <form method="get" action="command">
            Client:<br>
            ftp://<input type="text" name="_file"><br>
            Server:<br>
            ftp://{}<input type="text" name="_dest"><br>
            <input type="hidden" name="action" value="send">
            <input type="submit" value="send">
          </form>
        </body>
        </html>""".format(cherrypy.session['server'])

    @cherrypy.expose
    def receive(self):
        if 'server' not in cherrypy.session:
            return self.not_connect_notify + self.back
        else:
            return """<html>
        <head><title>Image Receive</title></head>
        <body>
          <form method="get" action="command">
            Server:<br>
	    ftp://{}<input type="text" name="_file"><br>
            Client:<br>
            ftp://<input type="text" name="_dest"><br>
            <input type="hidden" name="action" value="receive">
            <input type="submit" value="receive">
          </form>
        </body>
        </html>""".format(cherrypy.session['server'])

    @cherrypy.expose
    def connect(self):
        return """<html>
        <head><title>Connect Server</title></head>
        <body>
          <form method="get" action="connecting">
            server:<br>
            <input type="text" name="_server"><br>
            port:<br>
            <input type="text" name="_port"><br>
            <input type="submit" value="Connect">
          </form>
        </body>
        </html>"""

    @cherrypy.expose
    def command(self, _file, _dest, action):
        if action == "send":
            if "server" not in cherrypy.session:
                _file = "ftp://" + _file
            else:
                _file = "ftp://" + _file
                
            _dest = "ftp://" + cherrypy.session["server"] + _dest
            
        elif action == "receive":
            _file = "ftp://" + cherrypy.session["server"] + _file
            
            if "server" not in cherrypy.session:
                _dest = "ftp://" + _dest
            else:
                _dest = "ftp://" + _dest

        else:
            return "error in action " + self.back

        cmd = "globus-url-copy -vb " + _file + " " + _dest
        os.system(cmd)
        return cmd

    @cherrypy.expose
    def connecting(self, _server, _port):
        response = os.system("nc -z -v " + _server + " " + _port)
        if response == 0:
            cherrypy.session['server'] = _server
            return "Successfully connected " + _server + " : " + _port + self.back
        else:
            return "Failed to connect " + _server + " : " + _port + self.back

if __name__ == "__main__":
    conf = {
        '/': {
            'tools.sessions.on': True
            }
        }
    cherrypy.server.socket_host = '192.168.0.161'
    cherrypy.quickstart(ImgTransfer(), '/', conf)

