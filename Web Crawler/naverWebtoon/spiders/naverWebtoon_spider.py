
import scrapy
import regex as re
### 크롤링 방법
# 1. https://comic.naver.com/webtoon/period.nhn?period=2021&view=list 에서 작품번호(TitleID) 긁어온다
# 2. https://comic.naver.com/webtoon/list.nhn?titleId={     } 에 titleID 넣어서 작품 제목, 장르, 작가이름, 작가 번호(artistID)를 긁어온다
# 2-1. 필요하면 작가의 다른 작품은 https://comic.naver.com/artistTitle.nhn?artistId={    }에서 긁어온다.

# 3. 성별, 연령별 인기웹툰의 경우 셀레늄이 필요할 듯 하다. 그나마 근접한 링크 https://comic.naver.com/recommandWebtoonRank.nhn
    
class WebtoonSpider(scrapy.Spider):
    name = 'naverWebtoon' #spider 식별. 같은 이름 사용 불가
    # start_urls 목록으로 클래스 속성을 정의할 수 있다.
    # 기본구현에서 start_requests()스파이더에 대한 초기 요청을 만드는데 사용한다.
    
    start_urls = [
            'https://comic.naver.com/webtoon/period.nhn?period=2021&view=list',
        ]
    webtoonURL = 'https://comic.naver.com/webtoon/list.nhn?titleId='
    

    

    def parse(self, response):

        # Parsing titleID 
        titleTable = response.xpath('/html/body/div/div[@id="container"]/div[@id="content"]/div[@class="list_area table_list_area"]/table/tbody/tr/td[@class="subject"]/a').getall()
        #print(titleTable)
        for titleData in titleTable:

            titleID = re.findall('=\d+',titleData)
            if len(titleID) == 1:
                titleID = titleID[0][1:] # '=' 제거
            else :
                print("The titleID has problem")
            yield scrapy.Request(url=self.webtoonURL + titleID, callback=self.parseWebtoon)
    
    def parseWebtoon(self, response):
        def arrangeList(li):
            # 중복값 제거는 set으로 바꿨다가 list로 바꾸는 방법도 있다.
            # return list(set(li)) 
            newList = []
            for i in li:
                i= i.strip()
                if i not in newList:
                    newList.append(i)
        
            return newList

        # Parsing title, artist, genre, description 
        commonPath = '/html/body/div[@id="wrap"]/div[@id="container"]/div[@id="content"]/div[@class="comicinfo"]/div[@class="detail"]'

        title = response.xpath(commonPath + '/h2/text()').get().strip()
        artist = response.xpath(commonPath + '/h2/span[@class="wrt_nm"]/text()').get().strip()
        genre = response.xpath(commonPath + '/p[@class="detail_info"]/span[@class="genre"]/text()').get().strip().split(', ')
        
        description = response.xpath(commonPath + '/p').get().strip()
        artist = re.sub('[/]', ',', artist).split(',')
        artist = arrangeList(artist)
        description = re.sub('[<br>|</p>|<p>]',' ',description).strip()

        yield {
            'title': title,
            'artist': artist,
            'genre': genre,
            'description': description,
        }

