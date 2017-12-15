from socket import *
import os
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
import requests
from time import gmtime, strftime
import os.path
import sys
import shutil
from re import match

totalCC = 0


class Node():
    masterUrl = 'http://localhost:1111/'
    totalCC = 0
    ccConfig = Config(
                       exclude='',
                       ignore='venv',
                       order=SCORE,
                       no_assert=True,
                       show_closures=False,
                       min='A',
                       max='F',
                       )

    def __init__(self):
        self.blobUrl = requests.get(self.masterUrl).json()
        print(self.blobUrl)

    def getHeader(self):
        with open('github-token.txt', 'r') as tmp_file:
            token = tmp_file.read()     # get the token from a text file in current directory

        payload = {'access_token': token}
        headers = {'Accept': 'application/vnd.github.v3.raw'}
        
        #print(token)
        return (payload, headers)


    def checkPy(self, filename):
        return True if match('.*\.py', filename) is not None else False

    def calcCC(self, blobUrl):
        
        print(blobUrl)
        url = blobUrl.split('|')[0]
        filename = blobUrl.split('|')[1]
        
        payload_headers = self.getHeader()
        
        flag = self.checkPy(filename)
        
        if flag == True:
            
            resp = requests.get(url,   params=payload_headers[0], headers=payload_headers[1])
            
            sha = url.split('/blobs/')[1]
            
            filePath = filename + sha + '.py'
            
            with open(filePath, 'w') as tmpFile:
                tmpFile.write(resp.text)
            tmpFile.close()
            
            
            getFile = open(filePath, 'r')
            results = CCHarvester(filePath, self.ccConfig).gobble(getFile)
            getFile.close()
            os.remove(filePath)
            
            fileCC = 0
            
            for x in results:
                print (x.complexity)
                fileCC += int(x.complexity)
            
            print("Complexity of file: " + str(fileCC))
            return fileCC
        else:
            return 0

    def receiveWork(self):
        print("Blob: " + self.blobUrl)
        
        fileCC= self.calcCC(self.blobUrl)
        self.totalCC += fileCC
        
        self.blobUrl = requests.get(self.masterUrl).json()
        while self.blobUrl != "finished":
            fileCC = self.calcCC(self.blobUrl)
            self.totalCC += fileCC
            self.blobUrl = requests.get(self.masterUrl).json()


        print("Finished...")
        print("Total CC: " + str(self.totalCC))
        requests.put(self.masterUrl, data={'cc': self.totalCC})


def main():
    
    print("Worker is ready to receive...")
    node = Node()
    node.receiveWork()

if __name__ == "__main__":
    main()