from bs4 import BeautifulSoup
import requests
import json
import threading
import time

"""
    Creates a dictionary of words associated with their word class.

    Example format --

    {
        {
            word: 'hello',
            type: 'interjection'
        },
        {
            word: 'world',
            type: 'noun'
        }
    }
"""

def process(id):
    global processed, remaining, arr
    begin = int((len(words) / thread_count) * id)
    end = int((len(words) / thread_count) * (id + 1) - 1)
    for i in range(begin, end):
        word = words[i]
        # print('Processing word %d -- %s' % (i, word))
        url = 'https://www.dictionary.com/browse/{}?s=t'.format(word)
        r  = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'lxml')
        type = soup.find('span', {'class': 'pos'})

        # Get lock to synchronize threads
        threadLock.acquire()
        processed += 1
        remaining -= 1
        # Get lock to synchronize threads
        threadLock.release()

        if type is None:
            continue

        entry = dict()
        entry['word'] = word
        entry['type'] = type.text

        threadLock.acquire()
        with open('data.dic', 'a') as f:
            json.dump(entry, f)
        # arr.append(entry)
        threadLock.release()

class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      print ("Starting " + self.name)
      process(self.threadID)
      print ("Exiting " + self.name)

words = []
arr = []
processed = 0
remaining = 0

if __name__ == '__main__':
    with open('web2', 'r') as f:
        for line in f:
            words.append(line.strip())

    remaining = len(words)

    threadLock = threading.Lock()
    thread_count = 15
    threads = []

    for i in range(thread_count):
        threads.append(myThread(i, 'Thread-%d' % i))

    for thread in threads:
        thread.start()

    print()
    while remaining > 0:
        print('\rProgress - %.2f%% ( %d / %d )' % (processed / len(words) * 100, remaining, len(words)), end='')
        time.sleep(1)

    print('Complete -- 100%')

    for thread in threads:
        thread.join()


# with open ('dict.dat', 'w') as f:
#     json.dump(arr, f)
