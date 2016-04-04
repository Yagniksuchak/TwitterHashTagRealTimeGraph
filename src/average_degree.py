'''
This python script can be used to Calculate the average degree of a vertex in a Twitter hashtag graph
for the last 60 seconds, and update this each time a new tweet appears.
In short, this script calculates the average degree over a 60-second sliding window.
'''

import json
import networkx as nx
import matplotlib.pyplot as plt #In case we want to visualize the graph
import datetime
import sys



'''
Function to update the graph and calculate the average degree. This funciton also writes the output
to output.txt file
'''

def updateGraph():
    G = nx.Graph()
    runningAvg = 0
    for value in hashTagDic.values():
        for ls in value:
            if len(ls)<=1:
                continue
            for ele in ls:
                G.add_node(ele)
            for ele1 in ls:
                for ele2 in ls:
                    if ele1!=ele2 and not G.has_edge(ele1,ele2):
                        G.add_edge(ele1,ele2)
    degreeList = nx.degree(G).values()
    # nx.draw(G,with_labels=True)
    # plt.show()
    if degreeList:
        runningAvg = float(sum(degreeList))/len(degreeList)
    outputStr = "%.2f"% (int(runningAvg*100)/float(100))
    print(outputStr)
    outputFilePtr.write(outputStr+"\n")
    G.clear()
'''
Function to check if the newly received tweet is newer than all the tweets received so far.
'''
def aboveRange(created_at):

    if not hashTagDic:
        return False
    maxTimeStamp = max(hashTagDic.keys())
    if created_at > maxTimeStamp:
        return True

    return False
'''
Function to check if the new tweet is older than one minute of the newest tweet received so far.
'''

def belowRange(created_at):
    if not hashTagDic.keys():
        return False
    maxTimeStamp = max(hashTagDic.keys())
    if created_at < maxTimeStamp-datetime.timedelta(minutes=1):
        return True

    return False
'''
Function to check if the newly received tweet is withing range of maximum timeStamp so far
and one minute before that.
'''

def withinRange(created_at):
    if not hashTagDic.keys():
        return True
    maxTimeStamp = max(hashTagDic.keys())
    if created_at <= maxTimeStamp and created_at >= maxTimeStamp-datetime.timedelta(minutes=1):
        return True

    return False
'''
The newly received tweet is added to the graph.
'''
def addToHashTagDict(created_at,hashTags):
    if created_at in hashTagDic:
        hashTagDic.get(created_at).append(hashTags)
    else:
        hashTagDic[created_at] = [hashTags]

'''
The below function is called when we receive a tweet with timeStamp larger
than any previously received tweet.
'''

def filterHashTagDict(created_at):
    for key in hashTagDic.keys():
        if key<created_at-datetime.timedelta(minutes=1):
            hashTagDic.pop(key)

'''
processTweet extracts the created_at timeStamp and the list of HashTags.
Then a comparison is made between the present timeStamp and the timeStamps of the tweet
with which previous graph was created.
'''

def processTweet(tweet):
        hashTags = []
        created_at = tweet['created_at']
        created_at = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        # print(created_at)
        for tag in tweet['entities']['hashtags']:
            hashTags.append(tag['text'])
        # print hashTags
        if withinRange(created_at):
            addToHashTagDict(created_at,hashTags)
            updateGraph()
        elif belowRange(created_at):
            updateGraph()
        elif aboveRange(created_at):
            filterHashTagDict(created_at)
            addToHashTagDict(created_at,hashTags)
            updateGraph()

'''
It filters out the limit exceeded messages from twitter api
'''

def isValid(tweet):
    if 'contributors' in tweet:
        return True

'''
The entry point of the script.
#Input: The input file name which has tweets in json format
It processes the tweets one at a time.
'''
def startProcessing(fileName):
    tweets_file = open(fileName,'r')
    count = 0
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            # print tweet
            if isValid(tweet):
                processTweet(tweet)

        except:
            print("Some Error Occurred")
            continue


if __name__ == "__main__":
    if len(sys.argv)<3:
        print "!!! Usage: python ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/output.txt"
        sys.exit()

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    hashTagDic = {}
    outputFilePtr = open(outputFile,"w+")
    startProcessing(inputFile)
