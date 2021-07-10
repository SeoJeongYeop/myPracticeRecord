import praw
from praw.models import MoreComments
from psaw import PushshiftAPI
import json
from datetime import datetime

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

def write_json(path, data) :
    if path[-5:] != ".json":
        path = path +".json"
    with open(path, 'w', encoding = "utf-8") as outfile:
        outfile.write(json.dumps(data, ensure_ascii=False))


def scrap_subreddit(subreddit, keywordList, startDate, endDate):
    num = 0
    scrapList = []
    reddit = create_reddit_object()
    api = PushshiftAPI(reddit)
    startTimestamp = int(datetime(startDate[0], startDate[1], startDate[2]).timestamp())
    endTimestamp = int(datetime(endDate[0], endDate[1], endDate[2]).timestamp())
    print("from ",datetime(startDate[0],startDate[1],startDate[2])," to ", datetime(endDate[0],endDate[1],endDate[2]))

    submissionList = list(api.search_submissions(
        after=startTimestamp,
        before = endTimestamp,
        subreddit=subreddit,
        filter=['title','subreddit']
        ))
    total = len(submissionList)
    print("total ",total," results")

    previousTitle = ""
    for submission in submissionList :
        num += 1
        scrapDict = {}
        commentList = []
        if num % 1000 == 0:
            print(f"Analyzing {num} results...",num*100//total,"%")

        ### TEST PRINT
        # print("title: ",submission.title,
        #     "\nselftext: ", submission.selftext,
        #     "\ndate: ", submission.created_utc)


        if submission.selftext == "[deleted]" or submission.selftext == "[removed]" :
            # deleted or removed 상태의 글은 제외한다.
            continue
        elif submission.title == previousTitle :
            # 샘플링 결과 이전 글의 제목과 같은 경우가 다수 발견되었다. 이 경우도 제외한다.
            continue
        else :
            checkTitle = checkKeyword(submission.title, keywordList)
            checkText = checkKeyword(submission.selftext, keywordList)
            checkText.extend(checkTitle)
            keyword = list(set(checkText))

        if  len(keyword) != 0 :
            # 키워드, 검색결과번호, 제목, 날짜, 내용, 댓글을 저장한다.
            scrapDict["keyword"] = keyword
            scrapDict["num"] = num
            scrapDict["title"] = submission.title
            previousTitle = submission.title
            date = datetime.fromtimestamp(submission.created_utc)
            scrapDict["date"] = str(date)
            scrapDict["selftext"] = submission.selftext
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments) :
                    # MoreComments는 무시한다.
                    continue
                else :
                    commentList.append(top_level_comment.body.strip())

            scrapDict["comments"] = commentList
            scrapList.append(scrapDict)
        else :
            continue
    print("Done!")
    return scrapList

# 각 키워드가 텍스트 안에 있는지 확인하고 리턴한다.
def checkKeyword(text, keywordList) :
    findList = []
    for keyword in keywordList :
        if keyword in text :
            findList.append(keyword)
    if len(findList) == 0:
        return []
    else :
        return findList


subredditList = ['kpop', 'KDRAMA', 'koreanvariety','manhwa']
keywordDict ={}
keywordDict['kpop'] = ['K-pop', 'BTS', 'BLACKPINK', ' IU', 'PSY', 'TWICE', 'BoA']
keywordDict['KDRAMA'] = ['korean drama', 'Crash Landing on You', "It's Okay to Not Be Okay", 'Itaewon Class','Flower of Evil','Kingdom','The Heirs']
keywordDict['koreanvariety'] = ['Variety','Running Man', 'Knowing Bros', '2 Days & 1 Night', 'New Journey To The West',
"Youn's Kitchen", "Youn's Stay"]
keywordDict['manhwa'] = ['The Remarried Empress', 'True Beauty', 'Men of the Harem','The First Night With the Duke', 'Like Wind on a Dry Branch',
'The Advanced Player of the Tutorial Tower',
'Omniscient Reader', 
"His Majesty's Proposal",
'My Gently Raised Beast',
"She's Hopeless",
'The Hip Guy',
'The Boxer',
"It's Mine",
'Shotgun Boy']

for year in [2018,2019,2020,2021] :
    for month in range(1,13):
        if year == 2021 and month >= 7 :
            break
        else :
            startDate = [year,month,1]
            if month != 12 :
                endDate = [year,month+1,1]
            else :
                endDate = [year+1,1,1]
        for subreddit in subredditList:
            print("### ",datetime.now() ,"subreddit ", subreddit, " ###")
            keywordList = keywordDict[subreddit]
            
            data = scrap_subreddit(subreddit = subreddit, keywordList = keywordList, startDate=startDate, endDate=endDate)
            if month < 10:
                strmonth = "0"+str(month)
            else :
                strmonth = str(month)
            fileName = f"monthly/reddit_{subreddit}_{year}_{strmonth}.json" 
            write_json(path = fileName, data = data)