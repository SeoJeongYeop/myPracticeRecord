import scrapy

class NewsbotSpider(scrapy.Spider):
	name = 'newsbot'
	start_urls = ['http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001']

	def parse(self, response):
		titles = response.xpath('//*[@id="main_content"]/div[2]/ul/li/dl/dt[2]/a/text()').extract()
		authors = response.css('.writing::text').extract()
		previews = response.css('.lede::text').extract()

		for item in zip(titles, authors, previews):
			scraped_info = {
				'title' : item[0].strip(),
				'author' : item[1].strip(),
				'preview' : item[2].strip(),
			}
			yield scraped_info