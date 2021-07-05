from urllib.parse import quote
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'moviesEX' #spider 식별. 같은 이름 사용 불가
    # start_urls 목록으로 클래스 속성을 정의할 수 있다.
    # 기본구현에서 start_requests()스파이더에 대한 초기 요청을 만드는데 사용한다.

    # 영화번호        
    start_urls = [
        # 187322: 크루엘라
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=187322&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 163788 알라딘
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=163788&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 169637 라이온킹
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=130850&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 130850 주토피아
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=130850&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 130849 모아나
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=130849&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 100931 겨울왕국
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=100931&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 136873 겨울왕국2
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=136873&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 109911 빅히어로
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=109911&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 184518 라야와 마지막 드래곤
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=184518&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 115622 인사이드 아웃
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=115622&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 97629 도리를 찾아서
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=97629&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 151728 코코
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=151728&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 184517 소울
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=184517&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 72363 어벤져스1
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=72363&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 98438 어벤져스2
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=98438&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 136315 어벤져스3
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=136315&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        # 136900 어벤져스4
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=136900&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1',
        ]
        

    def parse(self, response):
        for movie in response.css('div.score_result'):
            for i in range(0,10):
                num = str(i)
                reple = movie.css(f'span#_filtered_ment_{num}::text').get()

                reple = reple.strip()

                yield{
                    'reple': reple,
                }

        # 링크를 재귀적으로 따라가서 데이터를 추출하도록 수정한 것.

        for page in response.css('div.paging a::attr(href)').getall():
            #print(f"output page {page}")
            if page is not None:
            # follow는 상대url 지원하여 urljoin을 호출할 필요가 없다.
                yield response.follow(page, callback=self.parse)

