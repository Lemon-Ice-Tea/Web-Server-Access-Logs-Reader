import codecs


with codecs.open('access_log.txt', 'rb', 'utf-8', errors='replace') as f:
    for line in f:
        print(line)