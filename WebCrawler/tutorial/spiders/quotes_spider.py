from urllib.parse import quote
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes' #spider 식별. 같은 이름 사용 불가
    # start_urls 목록으로 클래스 속성을 정의할 수 있다.
    # 기본구현에서 start_requests()스파이더에 대한 초기 요청을 만드는데 사용한다.
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
        ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield{
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags':quote.css('div.tags a.tag::text').getall(),
            }

        # 링크를 재귀적으로 따라가서 데이터를 추출하도록 수정한 것.

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # follow는 상대url 지원하여 urljoin을 호출할 필요가 없다.
            yield response.follow(next_page, callback=self.parse)
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)

            #문자열 대신 선택기
            # for href in response.css('ul.pager a::attr(href)'):
            ##yield response.follow(href, callback=self.parse)

            #iterable에서 여러 요청 생성 
            # anchors = response.css('ul.pager a')
            # yield from response.follow_all(anchors, callback=self.parse)
            # yield from response.follow_all(css='ul.pager a', callback=self.parse)




    # def start_requests(self):
    #     #스파이더가 크롤링을 시작할 반복 가능한 요청 반환
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback = self.parse)

    # def parse(self, response):
    #     # 각 요청에 대해 다운로드 된 응답을 처리하기 위해 호출되는 메소드
    #     page = response.url.split("/")[-2]
    #     filename = f'quotes-{page}.html'
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log(f'Saved file {filename}')

    
