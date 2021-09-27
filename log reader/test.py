import codecs


with codecs.open('access_log.txt', 'rb', 'utf-8', errors='replace') as f:
    for line in f:
        #if len(line) != 0:
        print(line.strip())