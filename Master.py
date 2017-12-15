from socket import *
import requests
from collections import deque
from flask import Flask
from flask_restful import Resource, Api, request
import shutil

trees = []
blobUrlList = []
githubUrl = 'https://api.github.com/repos/oconnes9/Cyclomatic/commits'
app = Flask(__name__)
api = Api(app)
blobUrlList = deque()
newCC = 0
CC = 0
blobListLength = 0

class Master(Resource):
    
    def get(self):
        global blobUrlList
        if blobUrlList:
            return blobUrlList.popleft()
        else:
            return "finished"


    def put(self):
        global CC
            
        newCC = int(request.form['cc'])
        CC = CC + newCC
        print("RECEIVED: " + str(newCC))

        aveCC = CC / blobListLength
        print("Average CC: " + str(aveCC))
        return '', 204

def getTrees(githubUrl):
    print("1")
    
    payloadHeaders = getParamHeaders()

    resp = requests.get(githubUrl,   params=payloadHeaders[0], headers=payloadHeaders[1])    # get the commit page of the github url
    
    for item in resp.json():
        trees.append(item['commit']['tree']['url']) # parse out the tree URL's from the commit page
    
    return trees


def blobList(githubUrl, trees):
    print("2")
    payloadHeaders = getParamHeaders()
    for blobUrl in trees:
        resp = requests.get(blobUrl,   params=payloadHeaders[0], headers=payloadHeaders[1])
        
        tree = resp.json()['tree']
        
        for item in tree:
            fileUrl = item['url']
            filename = item['path']
            urlFilename = fileUrl + '|' + filename
            blobUrlList.append(urlFilename)

    blobListLength = len(blobUrlList)

def getParamHeaders():
    print("3")
    with open('github-token.txt', 'r') as tmpFile:
        token = tmpFile.read()     # get the token from a text file in current directory
    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    
    return (payload, headers)

def main():

    print("Getting Tree URL list...")
    trees = getTrees(githubUrl)      # get the list of tree URL's from the project's commits
    print("Tree URL list received...")
    print("Gettng blob URL's...")
    blobList(githubUrl, trees)    # get blob URLs of each tree's
    print("Commenced sending of raw URL's to worker...")
    app.run(host = 'localhost', port = 1111, debug=False)




api.add_resource(Master, '/')
#    finished = False;
#    while finished is false:
#        connectionSocket, addr = manager_socket.accept()
#        recv_msg = connectionSocket.recv(1024)
#        recv_msg = recv_msg.decode()
#        
#        if "ready" in recv_msg:
#            print ("WORKER READY")
#            print("Commenced sending of raw URL's to worker...")
#            totalCC = send_work(blobUrlList, connectionSocket)     # send the raw URL's to the worker
#            finished = True
#            connectionSocket.close()
#    
#    
#    
#    total_cc = send_work(blobUrlList)     # send the raw URL's to the worker
#    
#    print("Total CC is: " + str(totalCC))
#    
#    avgCC = totalCC/len(blobUrlList)
#    print("Average CC is: " + str(avgCC))

if __name__ == "__main__":
    main()
