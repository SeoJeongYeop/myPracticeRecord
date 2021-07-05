import scrapy
import regex as re
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from . import items

### 크롤링 방법
# 1. https://www.fda.gov/news-events/fda-newsroom/press-announcements?page=0 에서 시작해서 page=85 까지의 뉴스기사 리스트를 읽는다.
# 2. 뉴스기사 리스트의 url을 이용해서 뉴스 기사를 읽는다. 일단은 기사 제목, 기사 날짜, 기사 내용 3가지만 긁는다.
# 3. 정리해서 json파일로 저장한다.

class FDASpider(scrapy.Spider):
    name = 'press'
    
    def start_requests(self):
        
        start_url = 'htquittps://www.fda.gov/news-events/fda-newsroom/press-announcements'
        yield scrapy.Request(url = start_url, callback = self.parseList)
        
    def parseList(self, response):
        seed_url = 'https://www.fda.gov'
        pressList = []
        for press in response.css('span.field-content a::attr(href)').getall():
            
            if press is not None:
                print(press)
                pressList.append(press)
                yield scrapy.Request(url =seed_url+ press, callback = self.parsePress)
        for page in response.xpath('//li[@class="pager__item"]/a/@href').getall():
            if page is not None:
                yield response.follow(page, callback=self.parseList)
        
        #
        print ({
            'List' : pressList,
        })
        #scrapy.Request(url = "", callback = self.parsePress) 
    def parsePress(self, response):
        item = items.FdaPressItem()
        item['title'] = response.xpath('.//h1[@class="content-title text-center"]/text()')
        #title = ''
        date = ''
        contents = []
        #title = response.css('h1.content-title.text-center::text').get()
        date = response.css("time::text").get()
        for content in response.css('div.col-md-8.col-md-push-2 p::text').getall() :
            content = content.strip()
            if len(content) > 10:
                contents.append(content)

        yield {
            'title' : item['title'],
            'date' : date,
            'contents' : contents,
        }
