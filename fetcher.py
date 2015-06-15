from BeautifulSoup import BeautifulSoup, SoupStrainer
import httplib2
import Queue

__author__ = 'tech'


class response:
    def __init(self, _response, _domain):
        self.response = _response
        self.domain = _domain # more flexible but may be need to be static

        def get_text(self):
            pass

        def is_right_domain():
            pass

        def get_links():
            for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
                 if link.has_attr('href') and self.is_right_domain(link):
                    yield link['href']
class fetcher:
    def __init__(self, _url, _top_n):
        self.url = _url
        self.top_n = _top_n
        self.words2count = {}

    def process(self):
        mapv = {} # need to be set - not time to lookup
        q = Queue.Queue()
        r = self.fetch_page()
        q.put(r)

        level = 0
        qty = 1
        while not q.empty():
            r = q.get()
            self.process_text(r.get_text())

            qty = qty - 1

            if qty is 0:
                level = level + 1

                if level is 3:
                    break

            for l in r.get_links():
                if l is not in mapv:
                    mapv.put(l, 1)
                    r1 = self.fetch_page(self.link2url(l))
                    q.put(r1)
                    qty = qty + 1

        self.select_and_dump_topn()

    def process_test(self, text):
        for word in self.split(text):
            if word in self.words2count.keys():
                self.words2count.put(word, 1)
            else:
                self.words2count.put(word, self.words2count.get(word) + 1) # there is much better way to do this

    def select_and_dump_topn(self):
        self.sort_by_value_and dump() # after result is dumped - interrupt sort

    def fetch_page(self, url):
        http = httplib2.Http()
        status, resp = http.request(url)
        # check status
        return response(resp, "www.wikipedia.com")
