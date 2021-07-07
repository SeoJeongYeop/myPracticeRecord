import scrapy
import regex as re
import sys, os
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from .. import items
from scrapy.loader import ItemLoader

### 크롤링 방법
# 1. https://www.fda.gov/news-events/fda-newsroom/press-announcements?page=0 에서 시작해서 page=85 까지의 뉴스기사 리스트를 읽는다.
# 2. 뉴스기사 리스트의 url을 이용해서 뉴스 기사를 읽는다. 일단은 기사 제목, 기사 날짜, 기사 내용 3가지만 긁는다.
# 3. 정리해서 json파일로 저장한다.

class FDASpider(scrapy.Spider):
    name = 'press'
    
    def start_requests(self):
        
        start_url = 'https://www.fda.gov/news-events/fda-newsroom/press-announcements'
        yield scrapy.Request(url = start_url, callback = self.parseList)
        
    def parseList(self, response):
        seed_url = 'https://www.fda.gov'
        pressList = []
        
        for press in response.xpath('.//span[@class="field-content"]/a/@href').getall():        
            if press is not None:
                print(press)
                pressList.append(press)
                yield response.follow(press, callback=self.parsePress) # 기존의 scrapy.Request는 공백을 데이터로 넣는 문제점이 있었다.
                #scrapy.Request(url =seed_url+ press, callback = self.parsePress)
        for page in response.xpath('.//li[@class="pager__item"]/a/@href').getall():
            if page is not None:
                yield response.follow(page, callback=self.parseList)
        
        #print ({'List' : pressList,})
        #scrapy.Request(url = "", callback = self.parsePress) 

    def parsePress(self, response):
        item = items.FdaPressItem()
        loader = ItemLoader(item = items.FdaPressItem(), response=response)
        loader.add_xpath('title', './/h1[@class="content-title text-center"]/text()')
        loader.add_xpath('date', './/time/text()')
        #item['title'] = response.xpath('.//h1[@class="content-title text-center"]/text()').get()
        #item['date'] = response.xpath('.//time/text()').get()
       
        
        contents = ""
        for content in response.xpath('.//div[@class="col-md-8 col-md-push-2"]/p/text()').getall() :
            content = content.strip()
            if len(content) > 10:
                contents = contents + " "+ content
        for content in response.xpath('.//div[@class="col-md-8 col-md-push-2"]/ul/li/text()').getall() :
            content = content.strip()
            if len(content) > 10:
                contents = contents + " "+ content
        for content in response.xpath('.//div[@class="col-md-8 col-md-push-2"]/ul/li/ul/li/text()').getall() :
            content = content.strip()
            if len(content) > 10:
                contents = contents + " "+ content
        #item['contents'] = contents
        loader.add_value('contents', contents)
        #time.sleep(0.5)
        if item != None :
            yield loader.load_item()
            #yield item
