import heapq
import sys

class StreamMedianComputer:
    current_median = 0

    # max_heap: contains the smallest half of the numbers
    # min_heap: contains the largest half
    # the numbers in max_heap is less than or equal to the numbers in min_heap
    # the size of max_heap is equal to or 1 more than the size of min_heap
    # using Python heapq module to implemnt the min heap 
    max_heap = []
    min_heap = []

    # size: the total size of max_heap and min_heap
    # if size is odd, the median is the root of max_heap
    # if size is even, the median is the average of roots of max_heap and
    # min_heap
    size = 0
    out_file = None

    def __init__(self, output_filename):
        self.out_file = open(output_filename, 'w')

    def read_tweet(self, filename):
        f = open(filename, 'r')
        tweets = f.readlines()
        for tweet in tweets:
            self.update_median(tweet)

    def update_median(self, tweet):
        word_map = {}
        new_median = 0
        words = []
        words = tweet.split()
        for word in words:
            if word not in word_map:
                word_map[word] = 1
            else:
                word_map[word] += 1
        number = len(word_map)

        # insert number
        # if the total size is even, push number to the max_heap
        # since heapq module in python only provides min heap implementation,
        # multiply the number need to be inserted to max_heap by -1 to make a
        # min heap for the max_heap, and multiply the number in the max_heap
        # by -1 to get the original number.
        if self.size % 2 == 0:
            number_to_max_heap = number * -1
            heapq.heappush(self.max_heap, number_to_max_heap)
            self.size += 1

            # after insert, if there is only one number in both max_heap and
            # min_heap: output the number 
            if len(self.min_heap) == 0:
                self.current_median = number
                self.out_file.write("%.2f\n" %(number))
                return

            # compare the original value of root number in max_heap with the
            # root number in min_heap.
            # if the original value of root number in max_heap is larger than 
            # root number in min_heap:
            # pop the root number from max_heap, multiply by -1, 
            # and push it to min_heap.
            # Also, pop the root number from min_heap, multiply by -1, and push
            # it to max_heap to keep the size balance
            original_root_number_in_max = self.max_heap[0] * -1
            if original_root_number_in_max > self.min_heap[0]:
                number_to_min_heap = heapq.heappop(self.max_heap) * -1
                number_to_max_heap = heapq.heappop(self.min_heap) * -1
                heapq.heappush(self.max_heap, number_to_max_heap)
                heapq.heappush(self.min_heap, number_to_min_heap)

        # if the total size of max_heap and min_heap is odd:
        # push the number to max_heap
        # then, pop the root number from max_heap, 
        # multiply by -1 to get original value,
        # and push it to the min_heap
        else:
            number_to_max_heap = number * -1
            heapq.heappush(self.max_heap, number_to_max_heap)
            number_to_min_heap = heapq.heappop(self.max_heap) * -1
            heapq.heappush(self.min_heap, number_to_min_heap)
            self.size += 1

        if self.size % 2 == 0:
            new_median = (-1*self.max_heap[0] + self.min_heap[0])/2.0
        else:
            new_median = -1*self.max_heap[0]

        self.current_median = new_median
        self.out_file.write("%.2f\n" %(new_median))

    def close_file(self):
        self.out_file.close()

def main(argv):
    filename = sys.argv[1]
    output_filename = sys.argv[2]
    computer = StreamMedianComputer(output_filename)
    computer.read_tweet(filename)
    computer.close_file()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python median_unique.py 'input_file' 'output_file'"
    else:
        main(sys.argv)
