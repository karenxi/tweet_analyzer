from operator import itemgetter
import sys

class StreamWordsCounter:
    out_file = None

    # using dict to keep each word and its counts
    words_count ={}

    def __init__(self, output_filename):
        self.out_file = open(output_filename, 'w')

    def read_tweets(self, filename):
        f = open(filename, 'r')
        tweets = f.readlines()
        for tweet in tweets:
            self.update_word_count(tweet)

    def update_word_count(self,tweet):
        text = []
        text = tweet.split()
        for word in text:
            if word not in self.words_count:
                self.words_count[word] = 1
            else:
                 self.words_count[word] += 1

    def output_file(self):
        # sort the words_count by key for output
        sortedMap = sorted(self.words_count.items(), key=itemgetter(0))
        for word, num in sortedMap:
            self.out_file.write("{:<30}{:<5}\n".format(word,num))
        self.out_file.close()

def main(argv):
    filename = sys.argv[1]
    output_filename = sys.argv[2]
    computer = StreamWordsCounter(output_filename)
    computer.read_tweets(filename)
    computer.output_file()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python words_tweeted.py 'input_file' 'output_file'"
    else:
        main(sys.argv)
