import sys
from bs4 import BeautifulSoup
import urllib2
from urlparse import urlparse
import Queue
from collections import defaultdict
import string
from operator import itemgetter

class Result:
    def __init__(self, _text):
        self.dict = defaultdict(int)
        for i in [word.strip(string.punctuation) for word in _text.split()]:
            if len(i) > 0 and not i.isdigit():
                self.dict[i.lower()] += 1

    def merge(self, _result):
        for k in _result.dict.keys():
            self.dict[k] += _result.dict[k]

    def dump(self, _percentage):
        items = self.dict.items()
        qty = (len(items) / 100) * _percentage
        for i in sorted(items, key=itemgetter(1), reverse=True):
            print i
            qty -= 1
            if qty < 0:
                break


class Node:
    def __init__(self, _url, _level, _app):
        if _url.startswith('/'):
            self.url = _app.get_domain() + _url
        else:
            self.url = _url
        self.level = _level
        self.app = _app
        self.soup = None

    def get_url(self):
        return self.url

    def get_result(self):
        print("processing level: " + str(self.level) + " => " + self.url)
        data = urllib2.urlopen(self.url)
        html = data.read()
        data.close()

        self.soup = BeautifulSoup(html)

        for script in self.soup(["script", "style"]):
            script.extract()

        return Result(self.soup.get_text())


    def get_level(self):
        return self.level

    def get_descendants(self):
        if self.level < app.get_depth():
            for links in self.soup.find_all('a'):
                current = links.get('href')
                if current is not None and not current.startswith('//') and \
                   (current.startswith('/') or current.startswith(app.get_domain())):
                    yield Node(current, self.level + 1, app)


class Application:
    def __init__(self, _url, _depth, _percentage):
        self.url = _url
        self.depth = int(_depth)
        self.percentage = int(_percentage)
        parsed = urlparse(self.url)
        self.domain = parsed.scheme + "://" + parsed.netloc

    def get_depth(self):
        return self.depth

    def get_domain(self):
        return self.domain

    def run(self):
        s = set()
        q = Queue.Queue()
        q.put(Node(self.url, 0, app))

        res = Result("")

        while not q.empty():
            current = q.get()

            res.merge(current.get_result())

            for i in current.get_descendants():
                if i.get_url() not in s:
                    q.put(i)
                    s.add(i.get_url())

        res.dump(self.percentage)

    @staticmethod
    def usage():
        print("usage " + sys.argv[0] + " url depth percentage")
        print("for example " + sys.argv[0] + " www.wikipedia.com 3 5")

if __name__ == "__main__":
    if len(sys.argv) is not 4:
        Application.usage()
    else:
        app = Application(sys.argv[1], sys.argv[2], sys.argv[3])
        app.run()


