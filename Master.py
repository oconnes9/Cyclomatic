from socket import *
import requests
from collections import deque
from flask import Flask
from flask_restful import Resource, Api, request
import shutil

trees = []
blobUrlList = []
githubUrl = 'https://api.github.com/repos/oconnes9/Distributed_System/commits'
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

def getHeader(): #function to return the
    print("1")
    with open('token.txt', 'r') as tmpFile:
        token = tmpFile.read()     # get the token from a text file in current directory
    payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    
    return (payload, headers)

def getTrees(githubUrl):
    print("2")
    
    headers = getHeader()

    resp = requests.get(githubUrl,   params=headers[0], headers=headers[1])
    
    for item in resp.json():
        trees.append(item['commit']['tree']['url'])
    
    return trees


def blobList(githubUrl, trees):
    print("3")
    headers = getHeader()
    for blobUrl in trees:
        resp = requests.get(blobUrl,   params=headers[0], headers=headers[1])
        
        tree = resp.json()['tree']
        
        for item in tree:
            fileUrl = item['url']
            filename = item['path']
            urlFilename = fileUrl + '|' + filename
            blobUrlList.append(urlFilename)

    blobListLength = len(blobUrlList)


def main():

    trees = getTrees(githubUrl)      #Get list of tree URLs
    blobList(githubUrl, trees)    #Get blob URL for each tree
    app.run(host = 'localhost', port = 1111, debug=False)




api.add_resource(Master, '/')

if __name__ == "__main__":
    main()
