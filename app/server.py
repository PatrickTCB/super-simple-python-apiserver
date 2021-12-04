# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import version as python_version
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
import time
import sys
import json
import locale
import os
import base64
from datetime import date, datetime

class APIEndPoint:
    method = ""
    getParams = {}
    postParams = {}
    path = ""
    server = ""
    
def getParamsFromPath(path) :
    getParamsDict = {}
    if "?" in path:
        pathSplit = path.split("?", 1)
        print(str(pathSplit))
        if "&" in pathSplit[1]:
            paramsRaw = pathSplit[1].split("&")
            for pRaw in paramsRaw:
                pSplit = pRaw.split("=")
                if len(pSplit) == 2:
                    getParamsDict[str(pSplit[0])] = str(pSplit[1])
        elif "=" in pathSplit[1]:
            pSplit = pathSplit[1].split("=")
            if len(pSplit) == 2:
                getParamsDict[str(pSplit[0])] = str(pSplit[1])
    return getParamsDict

serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond("GET")
    def do_POST(self):
        self.respond("POST")
    def respond(self, method):
        endpoint = APIEndPoint()
        endpoint.method = method
        endpoint.path = self.path.split("?")[0]
        endpoint.server = os.environ["FQDN"]
        endpoint.getParams = {}
        endpoint.postParams = {}
        print("Trying to build " + endpoint.path + " as an json response page. After " + endpoint.method + " request.")
        endpoint.getParams = getParamsFromPath(self.path)
        if endpoint.method == "POST":
            ctype, pdict = parse_header(self.headers['content-type'])
            if ctype == 'multipart/form-data':
                postvars = parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers['content-length'])
                postvars = parse_qs(
                        self.rfile.read(length), keep_blank_values=1)
            else:
                postvars = {}
            if len(postvars) > 0:
                for key in postvars.keys():
                    pvlist = postvars[key]
                    if len(pvlist) == 1:
                        endpoint.postParams[key.decode("utf-8")] = postvars[key][0].decode("utf-8")
                    else:
                        pvstringlist = []
                        for pv in postvars[key]:
                            pvstringlist.append(pv.decode("utf-8"))
                        endpoint.postParams[key.decode("utf-8")] = pvstringlist
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Time to build the json response. Our basic plan here is to build a nice little dictionary, then in the last step
        # we turn it into json and that's our response body. 
        responseDict = {}
        # A bunch of dictionary build ing junk happens here
        responseDict["example"] = True
        responseDict["fun"] = "fun"
        responseDict["GetParametersReceived"] = endpoint.getParams
        responseDict["PostParametersReceived"] = endpoint.postParams
        # Now that our response dictionary has been built, we can give it back to the requester.
        self.wfile.write(bytes(json.dumps(responseDict), "utf-8"))
        #Done :)

if __name__ == "__main__":        
    webServer = HTTPServer(("", serverPort), MyServer)
    print("Server started http://localhost:%s" % (serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
