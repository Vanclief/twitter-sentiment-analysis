import sys
import os
import subprocess

def main(start_time, end_time):

    print("Processing Tweets")

    processor = subprocess.Popen([
        sys.executable,
        'tweet_processor.py',
        start_time,
        end_time])
    processor.wait()

    print("Finished processing Tweets")
    print("Analysing Tweets")

    analyser = subprocess.Popen([
        sys.executable,
        'tweet_sentiment.py',
        start_time,
        end_time])
    analyser.wait()

    print("Finished analysing Tweets")
    print("Graphing Tweets")

    grapher = subprocess.Popen([
        sys.executable,
        'grapher.py',
        start_time,
        end_time])
    grapher.wait()

    print("Finished graphing Tweets")

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print ("ERROR: Usage __main__.py <start date> <end date>")
    else:
        main(sys.argv[1], sys.argv[2])
