from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag
from datetime import datetime

DATE_FORMAT = '%B %d, %Y at %l:%M%P IST'

class RTEParser(BaseParser):
    domains = ['www.rte.ie']

    feeder_pat   = '^http://www.rte.ie/news/'
    feeder_pages = ['http://www.rte.ie/news/']

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        self.meta = soup.findAll('meta')
        elt = soup.find('h1', {'itemprop':'name'})
        if elt is None:
            self.real_article = False
            return
        self.title = elt.getText()

        # No bylines in RTE News
        self.byline = ''

        datestr = soup.find('time', {'itemprop':'dateModified'}).getText()
        if datestr:
          datet = datetime.strptime(datestr, '%H:%M, %A, %d %B %Y')
          self.date = datet.strftime(DATE_FORMAT)
        else:
          self.date = ''

        if soup.find('section', 'body') is None:
            self.real_article = False
            return
        for section in soup.findAll('section', 'body'):
            sectiontext = '\n'.join(section.findAll(text=True))

        if soup.find('section', 'bodyExt') is None:
            self.body = '\n' + sectiontext 
        else:
            for section in soup.findAll('section', 'bodyExt'):
                extsectiontext = '\n'.join(section.findAll(text=True))
            self.body = '\n' + sectiontext + extsectiontext
