import praw
from praw.models import MoreComments
from psaw import PushshiftAPI
import os
import json
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from requests.models import Response

import scrapy
from .. import items
from scrapy.loader import ItemLoader

def write_json(path, data) :
        if path[-5:] != ".json":
            path = path +".json"
        with open(path, 'w', encoding = "utf-8") as outfile:
            outfile.write(json.dumps(data, ensure_ascii=False))

def create_reddit_object(json_file = "data/reddit_config.json", json_key = "reddit"):
        with open(json_file) as f:
            data = json.load(f)
        user_values = data[json_key]
        reddit = praw.Reddit(client_id = user_values['client_id'],
                            client_secret=user_values['client_secret'],
                            user_agent=user_values['user_agent'],
                            username=user_values['username'],
                            password=user_values['password'],)
        return reddit
    # 각 키워드가 텍스트 안에 있는지 확인하고 리턴한다.

class rdt(scrapy.Spider):
    name = 'reddit'
    def __init__(self) :
        try :
            self.reddit = create_reddit_object()
            self.set_timedelta("month")
        except :
            self.reddit = None

    def start_requests(self):
        
        start_url = 'http://quotes.toscrape.com/page/1/'

        self.set_timedelta("day")
        self.subreddit = "kpop"
        self.keywordList = ['K-pop', 'BTS', 'BLACKPINK', ' IU', 'PSY', 'TWICE', 'BoA']
        self.since = "2018-01-01"
        self.until = "2018-01-03"
        #subreddit, keywordList, since, until
       
        yield scrapy.Request(url = start_url, callback = self.scrap_subreddit)

    def set_reddit(self, client_id, client_secret, user_agent,username, password):
        try:
            self.reddit = praw.Reddit(client_id = client_id,
                            client_secret = client_secret,
                            user_agent = user_agent,
                            username = username,
                            password = password)
            print("Success!")
        except :
            print("Fail!")

    def set_timedelta(self, period):
        self.period = period
        if period == "day":
            self.timedelta = dt.timedelta(days=1)
        elif period == "week" :
            self.timedelta = dt.timedelta(weeks=1)
        elif period == "month" :
            self.timedelta = relativedelta(months=1)
        elif period == "quarter" :
            self.timedelta = relativedelta(months=3)
        elif period == "year" :
            self.timedelta = relativedelta(years=1)

    def checkKeyword(self, text) :
        findList = []
        for keyword in self.keywordList :
            if keyword in text :
                findList.append(keyword)
        if len(findList) == 0:
            return []
        else :
            return findList

    def scrap_subreddit(self, response):
        print("hello")
        self.loader = ItemLoader(item = items.PsawcrawlerItem(), response=response)
        print("world!")
        if self.reddit == None :
            print("Please set reddit api key")
            return
        
        api = PushshiftAPI(self.reddit)

        before = int(datetime.strptime(self.until, "%Y-%m-%d").timestamp())
        print("from ",self.since," to ", self.until)
        pivot = int(datetime.strptime(self.since, "%Y-%m-%d").timestamp())
        while True :
            
            if pivot >= before :
                break
            
            date = datetime.fromtimestamp(pivot)
            path = f"{self.period}/reddit_{self.subreddit}_{date.strftime('%Y-%m-%d')}.json"
            next_pivot = int((date + self.timedelta).timestamp())
            if next_pivot > before :
                next_pivot = before
            print("### ",datetime.now() ,"subreddit ", self.subreddit, " ###")
            self.submissionList = list(api.search_submissions(
                after = pivot,
                before = next_pivot,
                subreddit=self.subreddit,
                filter=['title','subreddit']
                ))
            print(date, " ~ ", datetime.fromtimestamp(next_pivot))
            self.analyze_submission()

            print("Done!")
            pivot = next_pivot
                
            # if not os.path.exists(self.period):
            #     os.makedirs(self.period)
            
            #write_json(path= path, data= scrapList)
        yield self.loader.load_item()
            
            

        

    def analyze_submission(self):
        num = 0
        previousTitle = ""
        total = len(self.submissionList)
        print("total ",total," results")
        
        for submission in self.submissionList :
            num += 1
           
            commentList = []
            if num % 500 == 0:
                print(f"Analyzing {num} results...",num*100//total,"%")
            if submission.selftext == "[deleted]" or submission.selftext == "[removed]" :
                # deleted or removed 상태의 글은 제외한다.
                continue
            #### 속도 이슈로 제외, 2분 분석이 1시간 분석으로 바뀌는 이상한 현상 발생
            # elif submission.selftext == "" and len(submission.comments) == 0 :
            #     # 본문과 댓글이 없는 글은 데이터 분석의 가치가 없으므로 제외한다.
            #     continue
            elif submission.title == previousTitle :
                # 샘플링 결과 이전 글의 제목과 같은 경우가 다수 발견되었다. 이 경우도 제외한다.
                continue
            else :
                checkTitle = self.checkKeyword(submission.title)
                checkText = self.checkKeyword(submission.selftext)
                checkText.extend(checkTitle)
                keyword = list(set(checkText))

            if  len(keyword) != 0 :
                # 키워드, 검색결과번호, 제목, 날짜, 내용, 댓글을 저장한다.
                self.loader.add_value('postId', submission.id)
                self.loader.add_value('keyword', keyword)
                self.loader.add_value('title', submission.title)
                previousTitle = submission.title


                self.loader.add_value('body', submission.selftext)
                date = datetime.fromtimestamp(submission.created_utc)
                self.loader.add_value('date', str(date))
                self.loader.add_value('subreddit', self.subreddit)
                
                
                for top_level_comment in submission.comments:
                    if isinstance(top_level_comment, MoreComments) :
                        # MoreComments는 무시한다.
                        continue
                    else :
                        commentDict = {}
                        commentDict["commentId"] = top_level_comment.id
                        commentDict["body"] = top_level_comment.body.strip()
                        date_comment = datetime.fromtimestamp(top_level_comment.created_utc)
                        commentDict["date"] = str(date_comment)
                        commentList.append(commentDict)
                self.loader.add_value('comments', commentList)

                continue

        
        
