import praw
from praw.models import MoreComments
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

# hot, new, controv, top, gilded
def scrap_subreddit(subreddit, limit, keywordList):
    num = 0

    scrapList = []
    reddit = create_reddit_object()
    subReddit = reddit.subreddit(subreddit).hot(limit = limit) # List형식으로 글의 id를 보관하고 있음

    for submission in subReddit:
        scrapDict = {}
        commentList = []
        num += 1

        checkTitle = checkKeyword(submission.title, keywordList)
        checkText = checkKeyword(submission.selftext, keywordList)
        if  len(checkTitle) != 0 or len(checkText) != 0:
            checkText.extend(checkTitle)
            keyword = list(set(checkText))
            scrapDict["keyword"] = keyword
            scrapDict["num"] = num
            scrapDict["title"] = submission.title
            date = datetime.fromtimestamp(submission.created_utc)
            scrapDict["date"] = str(date)
            scrapDict["selftext"] = submission.selftext
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments) :
                    continue
                else :
                    commentList.append(top_level_comment.body.strip())

            scrapDict["comments"] = commentList
            scrapList.append(scrapDict)


        else :
            continue
    print("Done!")
    return scrapList
def checkKeyword(text, keywordList) :
    findList = []
    for keyword in keywordList :
        if keyword in text :
            findList.append(keyword)
    if len(findList) == 0:
        return []
    else :
        return findList
subredditList = ['kpop']
#subredditList = ['kpop', 'KDRAMA', 'koreanvariety','manhwa']
keywordDict ={}
keywordDict['kpop'] = ['K-pop', 'BTS', 'BLACKPINK', ' IU','PSY','TWICE','BoA']
keywordDict['KDRAMA'] = ['korean drama', 'Crash Landing on You', "It's Okay to Not Be Okay", 'Itaewon Class','Flower of Evil','Kingdom','The Heirs']
keywordDict['koreanvariety'] = ['Variety','Running Man', 'Knowing Bros', '2 Days & 1 Night', 'New Journey To The West',
"Youn's Kitchen", "Youn's Stay"]
keywordDict['manhwa'] = ['The Remarried Empress', 'True Beauty', 'Men of the Harem',
'The First Night With the Duke', 'Like Wind on a Dry Branch',
'The Advanced Player of the Tutorial Tower',
'Omniscient Reader', 
"His Majesty's Proposal",
'My Gently Raised Beast',
"She's Hopeless",
'The Hip Guy',
'The Boxer',
"It's Mine",
'Shotgun Boy']


for subreddit in subredditList:
    print("### subreddit ", subreddit, " ###")
    keywordList = keywordDict[subreddit]
    
    # max limit = 1000
    data = scrap_subreddit(subreddit = subreddit, limit = 1000, keywordList = keywordList)

    fileName = "data/reddit_hot_"+ subreddit+".json" 
    write_json(path = fileName, data = data)