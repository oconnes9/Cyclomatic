# Cyclomatic

The master passes the github commits url into a function which retrieves the trees in the repository. This function uses python requests to gain access to the json file. The json file is parsed to retrieve the tree URLs and each URL is added to a list called trees.

This list, along with the github commits URL are passed into a function which retrieves the names of every file and their URLs. Each of these is added to a list called blobUrlList. The REST service is then started, utilizing the python Flask library. 

The nodes request the blobUrl from the Master. This is passed into a function which calculates the cyclomatic complexity, which temporarily downloads the file to do this. The total cyclomatic complexity for the file is updated and a new blobUrl is requested. This is done until the blobUrl is not equal to "finished". When the file is finished, the total cyclomatic complexity is available for the Master to retrieve. 

The Master adds this cyclomatic complexity to the total cyclomatic complexity and finds an average. I did not get to create a graph as none of my repositories were suitable for testing. My code is written in python 3.6 and my other repositories are in 2.7. I could not use the Cyclomatic complexity repository as one of the commits has a mistake in it which stops the complexity calculator from calculating. 

The code does, however, calculate the cyclomatic complexities up until these points where there are mistakes or discrepancies in python version conventions and the REST service works.
