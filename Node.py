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
manager_url = 'http://localhost:1111/'

class Node():
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

    def getHeader():
        with open('github-token.txt', 'r') as tmp_file:
            token = tmp_file.read()     # get the token from a text file in current directory

        payload = {'access_token': token}
        headers = {'Accept': 'application/vnd.github.v3.raw'}
        
        #print(token)
        return (payload, headers)


    def check_py(filename):
        return True if match('.*\.py', filename) is not None else False

    def calcCC(rawUrl, ccConfig):
        
        blobUrl = rawUrl.split('|')[0]
        filename = rawUrl.split('|')[1]
        
        payload_headers = self.getHeader()
        
        flag = self.check_py(filename)
        
        if flag == True:
            
            resp = requests.get(blobUrl,   params=payload_headers[0], headers=payload_headers[1])
            
            filePath = filename
            
            with open(filePath, 'w') as tmp_file:
                tmpFile.write(resp.text)
            tmpFile.close()
            
            
            getFile = open(file_path, 'r')
            results = CCHarvester(filePath, ccConfig).gobble(getFile)
            CC_file_get.close()
            os.remove(filePath)
            
            fileCC = 0
            
            for x in results:
                print (x.complexity)
                fileCC += int(x.complexity)
            
            print("Complexity of file: " + str(fileCC))
            return fileCC
        else:
            return 0

    def receiveWork():
        print("Blob: " + self.blobUrl)
        
        fileCC= self.calcCC(self.blobUrl)
        self.totalCC += fileCC
        
        self.blobUrl = requests.get(self.masterUrl).json()
        if self.blobUrl != "finished":
            self.receiveWork()
        else:
            print("Finished...")
            print("Total CC: " + str(self.totalCC))
            requests.put(self.masterUrl, data={'cc': self.totalCC})


def main():
    
    print("Worker is ready to receive...")
    node = Node()
    node.receive_work()

if __name__ == "__main__":
    main()