from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

# 크롬 드라이버를 가져온다.
# 속도향상을 위한 세팅
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR") 
options.add_argument('log-level=3')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54")
driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.implicitly_wait(1)
url = "https://www.youtube.com/watch?v=TpPwI_Lo0YY"
driver.get(url)

    
endPage = driver.execute_script("return document.documentElement.scrollHeight")

# 스크롤을 내려 유튜브 댓글이 로딩되도록 한다. 시간관계상 20번만 반복한다.
count = 20
for i in range(count) :
    if (i%5) == 0 or i+1 == count:
        print(i*100//count,"%...")
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3.0)
    updatePage = driver.execute_script("return document.documentElement.scrollHeight")

    if updatePage == endPage:
        break
    endPage = updatePage

# 소스코드를 가져와서 파싱한다.
html = driver.page_source
driver.close()
soup = BeautifulSoup(html, 'html.parser')
writers = soup.select('#author-text > span')
reples = soup.select('#content-text')

repleList = []

# 형식을 맞춰주고 글자수가 적은 노이즈 데이터는 제거한다.
for i in range(len(writers)):
    reple = reples[i].text.strip()
    if len(reple) < 8:
        continue
    else :
        writer = writers[i].text.strip()
        reple = reple.replace('\n', ' ')
        repleDict = {}
        repleDict['author'] = writer
        repleDict['reple'] = reple
        repleList.append(repleDict)

#json으로 저장한다.
output = json.dumps(repleList, ensure_ascii=False)

with open('output.json', 'w',encoding='utf=8') as file:
    file.write(output)
print(output)