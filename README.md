The main goal of this code base is to Create a Graph out of HashTags from tweets coming in from live streaming API of Twitter. It also calculates the average degree of each Node(or HashTag) over a 60-second sliding window.

To run the script use the shell script run.sh or run the python script average_degree.py with following syntax.

python ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/output.txt

Dependencies: networkx python package. 

Other python packages used: json, datetime, sys
