import json

class Configuration(object):
    def __init__(self, fileName):
        self.__dict__ = json.load(open(fileName))

def Main():
    pass

if __name__ == "__main__":
    Main()