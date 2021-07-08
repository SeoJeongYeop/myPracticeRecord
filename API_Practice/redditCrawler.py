import praw
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
def scrap_subreddit(subreddit, limit, keyword):
    num = 0
    print("find keyword: ", keyword)
    scrapList = []
    reddit = create_reddit_object()
    subReddit = reddit.subreddit(subreddit).hot(limit = limit)
    for submission in subReddit:
        scrapDict = {}
        commentList = []
        num += 1
        scrapDict["keyword"] = keyword
        scrapDict["num"] = num
        scrapDict["title"] = submission.title
        scrapDict["selftext"] = submission.selftext
        if checkKeyword(scrapDict["title"], keyword) or checkKeyword(scrapDict["selftext"], keyword):
            
            date = datetime.fromtimestamp(submission.created_utc)
            scrapDict["date"] = str(date)
            
            for top_level_comment in submission.comments:
                commentList.append(top_level_comment.body.strip())

            scrapDict["comments"] = commentList
            # if (id*100 // limit) % 20  == 0 :
            #     print(id*100 // limit,"%...")
            scrapList.append(scrapDict)
        else :
            continue
    print("Done!")
    return scrapList
def checkKeyword(title, keyword) :
    if keyword in title :
        return True
    else :
        return False


subredditList = ['kpop', 'KDRAMA', 'koreanvariety','manhwa']
keywordDict ={}
keywordDict['kpop'] = ['K-pop', 'BTS', 'BLACKPINK', 'IU','PSY','TWICE','BoA']
keywordDict['KDRAMA'] = ['korean dramas', 'Crash Landing on You', "It's Okay to Not Be Okay", 'Itaewon Class','Flower of Evil','Kingdom','The Heirs']
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
    for keyword in keywordDict[subreddit]:
        # max limit = 1000
        data = scrap_subreddit(subreddit = subreddit, limit = 1000, keyword = keyword)

        keyword = keyword.replace(' ', '+')
        fileName = "data/reddit_hot_"+ subreddit +"_"+keyword+".json" 
        write_json(path = fileName, data = data)