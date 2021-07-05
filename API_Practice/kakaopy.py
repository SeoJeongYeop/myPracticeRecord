import requests
import urllib.request
import json

header = {}

def setHeader(restAPI) :
    header['Authorization'] = "KakaoAK "+ restAPI

class doc:
    def help(self):
        print("setSort(sort): sort must be accuracy or recency in doc.")
        print("setPage(page): 1 <= page <= 50 in doc.")
        print("setSize(size): 1 <= size <= 50 in doc.")
        print("setData(sort, page, size): Set at once")
        print("search(query): Return search results in the form of json.")
        print("save(query, path): Save the search results as a json file. The 'path' is the file name or path to the file.")

    def setData(self, sort, page, size):
        self.setSort(self, sort)
        self.setPage(self, page)
        self.setSize(self, size)

    def setSort(self, sort):
        if sort == "accuracy" or sort == "recency":
            self.sort = sort
        else :
            print("sort must be accuracy or recency in doc.")

    def setPage(self, page):
        if 1 <= page and page <= 50:
            self.page = page
        else :
            print("1 <= page <= 50 in doc.")

    def setSize(self, size):
        if 1<= size and size <= 50 :
            self.size = size
        else :
            print("1 <= size <= 50 in doc.")

    def search(self, query:str):
        try :
            Text = urllib.parse.quote(query)
        except:
            print("There is a problem with the input query.")
            return
        
        queryString = "?query="+Text+"&sort="+self.sort+"&page="+str(self.page)+"&size="+str(self.size)

        r = requests.get(self.url + queryString, headers=header)
        return json.loads(r.text)


    def save(self, query:str, path:str):
        data = self.search(query)
        if ".json" not in path:
            path = path + ".json"
        with open(path, 'w', encoding = 'utf-8') as outfile:
            outfile.write(json.dumps(data, ensure_ascii = False))
            print("saved!")

    def __init__(self):
        self.query =""
        self.url = "https://dapi.kakao.com/v2/search/web"
        self.sort = "accuracy"
        self.page = 1
        self.size = 10


class video:
    
    def help(self):
        print("setSort(sort): sort must be accuracy or recency in video.")
        print("setPage(page): 1 <= page <= 15 in video.")
        print("setSize(size): 1 <= size <= 30 in video.")
        print("setData(sort, page, size): Set at once")
        print("search(query): Return search results in the form of json")
        print("save(query, path): Save the search results as a json file. The 'path' is the file name or path to the file.")

    def setData(self, sort, page, size):
        self.setSort(self, sort)
        self.setPage(self, page)
        self.setSize(self, size)
    
    def setSort(self, sort):
        if sort == "accuracy" or sort == "recency":
            self.sort = sort
        else :
            print("sort must be accuracy or recency in video.")

    def setPage(self, page):
        if 1 <= page and page <= 15:
            self.page = page
        else :
            print("1 <= page <= 15 in video.")

    def setSize(self, size):
        if 1<= size and size <= 30 :
            self.size = size
        else :
            print("1 <= size <= 30 in video.")

    def search(self, query:str):
        try :
            Text = urllib.parse.quote(query)
        except:
            print("There is a problem with the input query.")
            return
        
        queryString = "?query="+Text+"&sort="+self.sort+"&page="+str(self.page)+"&size="+str(self.size)

        r = requests.get(self.url + queryString, headers=header)
        return json.loads(r.text)

    def save(self, query:str, path:str):
        data = self.search(query)
        if ".json" not in path:
            path = path + ".json"
        with open(path, 'w', encoding = 'utf-8') as outfile:
            outfile.write(json.dumps(data, ensure_ascii = False))
            print("saved!")

    def __init__(self):
        self.query =""
        self.url = "https://dapi.kakao.com/v2/search/vclip"
        self.sort = "accuracy"
        self.page = 1
        self.size = 15

class image:
    
    def help(self):
        print("setSort(sort): sort must be accuracy or recency in image.")
        print("setPage(page): 1 <= page <= 50 in image.")
        print("setSize(size): 1 <= size <= 80 in image.")
        print("setData(sort, page, size): Set at once")
        print("search(query): Return search results in the form of json")
        print("save(query, path): Save the search results as a json file. The 'path' is the file name or path to the file.")

    def setData(self, sort, page, size):
        self.setSort(self, sort)
        self.setPage(self, page)
        self.setSize(self, size)
    
    def setSort(self, sort):
        if sort == "accuracy" or sort == "recency":
            self.sort = sort
        else :
            print("sort must be accuracy or recency in image.")

    def setPage(self, page):
        if 1 <= page and page <= 50:
            self.page = page
        else :
            print("1 <= page <= 50 in image.")

    def setSize(self, size):
        if 1<= size and size <= 80 :
            self.size = size
        else :
            print("1 <= size <= 80 in image.")

    def search(self, query:str):
        try :
            Text = urllib.parse.quote(query)
        except:
            print("There is a problem with the input query.")
            return
        
        queryString = "?query="+Text+"&sort="+self.sort+"&page="+str(self.page)+"&size="+str(self.size)

        r = requests.get(self.url + queryString, headers=header)
        return json.loads(r.text)

    def save(self, query:str, path:str):
        data = self.search(query)
        if ".json" not in path:
            path = path + ".json"
        with open(path, 'w', encoding = 'utf-8') as outfile:
            outfile.write(json.dumps(data, ensure_ascii = False))
            print("saved!")

    def __init__(self):
        self.query =""
        self.url = "https://dapi.kakao.com/v2/search/image"
        self.sort = "accuracy"
        self.page = 1
        self.size = 80

class blog:
    
    def help(self):
        print("setSort(sort): sort must be accuracy or recency in blog.")
        print("setPage(page): 1 <= page <= 50 in blog.")
        print("setSize(size): 1 <= size <= 50 in blog.")
        print("setData(sort, page, size): Set at once")
        print("search(query): Return search results in the form of json")
        print("save(query, path): Save the search results as a json file. The 'path' is the file name or path to the file.")

    def setData(self, sort, page, size):
        self.setSort(self, sort)
        self.setPage(self, page)
        self.setSize(self, size)
    
    def setSort(self, sort):
        if sort == "accuracy" or sort == "recency":
            self.sort = sort
        else :
            print("sort must be accuracy or recency in blog.")

    def setPage(self, page):
        if 1 <= page and page <= 50:
            self.page = page
        else :
            print("1 <= page <= 50 in blog.")

    def setSize(self, size):
        if 1<= size and size <= 50 :
            self.size = size
        else :
            print("1 <= size <= 50 in blog.")

    def search(self, query:str):
        try :
            Text = urllib.parse.quote(query)
        except:
            print("There is a problem with the input query.")
            return
        
        queryString = "?query="+Text+"&sort="+self.sort+"&page="+str(self.page)+"&size="+str(self.size)

        r = requests.get(self.url + queryString, headers=header)
        return json.loads(r.text)

    def save(self, query:str, path:str):
        data = self.search(query)
        if ".json" not in path:
            path = path + ".json"
        with open(path, 'w', encoding = 'utf-8') as outfile:
            outfile.write(json.dumps(data, ensure_ascii = False))
            print("saved!")

    def __init__(self):
        self.query =""
        self.url = "https://dapi.kakao.com/v2/search/blog"
        self.sort = "accuracy"
        self.page = 1
        self.size = 10

class book:

    def help(self):
        print("setSort(sort): sort must be accuracy or latest in book.")
        print("setPage(page): 1 <= page <= 50 in book.")
        print("setSize(size): 1 <= size <= 50 in book.")
        print("setTarget(target): target must be title, isbn, publisher or person")
        print("setData(sort, page, size, target): Set at once")
        print("search(query): Return search results in the form of json")
        print("save(query, path): Save the search results as a json file. The 'path' is the file name or path to the file.")
    
    def setData(self, sort, page, size, target):
        self.setSort(self, sort)
        self.setPage(self, page)
        self.setSize(self, size)
        self.setTarget(self,target)
    
    def setSort(self, sort):
        if sort == "accuracy" or sort == "latest":
            self.sort = sort
        else :
            print("sort must be accuracy or latest in book.")

    def setPage(self, page):
        if 1 <= page and page <= 50:
            self.page = page
        else :
            print("1 <= page <= 50 in book.")

    def setSize(self, size):
        if 1<= size and size <= 50 :
            self.size = size
        else :
            print("1 <= size <= 50 in book.")

    def setTarget(self, target):
        if target in ["title", "isbn", "publisher", "person"] :
            self.target = target
        else :
            print("target must be title, isbn, publisher or person")

    def search(self, query:str):
        try :
            Text = urllib.parse.quote(query)
        except:
            print("There is a problem with the input query.")
            return
        
        queryString = "?query="+Text+"&sort="+self.sort+"&page="+str(self.page)+"&size="+str(self.size)
        if self.target != "":
            queryString += "&target="+self.target

        r = requests.get(self.url + queryString, headers=header)
        return json.loads(r.text)

    def save(self, query:str, path:str):
        data = self.search(query)
        if ".json" not in path:
            path = path + ".json"
        with open(path, 'w', encoding = 'utf-8') as outfile:
            outfile.write(json.dumps(data, ensure_ascii = False))
            print("saved!")

    def __init__(self):
        self.query =""
        self.url = "https://dapi.kakao.com/v3/search/book"
        self.sort = "accuracy"
        self.page = 1
        self.size = 10
        self.target = ""

class cafe:
    def help(self):
        print("setSort(sort): sort must be accuracy or recency in cafe.")
        print("setPage(page): 1 <= page <= 50 in cafe.")
        print("setSize(size): 1 <= size <= 50 in cafe.")
        print("setData(sort, page, size): Set at once")
        print("search(query): Return search results in the form of json.")
        print("save(query, path): Save the search results as a json file. The 'path' is the file name or path to the file.")

    def setData(self, sort, page, size):
        self.setSort(self, sort)
        self.setPage(self, page)
        self.setSize(self, size)
    
    def setSort(self, sort):
        if sort == "accuracy" or sort == "recency":
            self.sort = sort
        else :
            print("sort must be accuracy or recency in cafe.")

    def setPage(self, page):
        if 1 <= page and page <= 50:
            self.page = page
        else :
            print("1 <= page <= 50 in cafe.")

    def setSize(self, size):
        if 1<= size and size <= 50 :
            self.size = size
        else :
            print("1 <= size <= 50 in cafe.")

    def search(self, query:str):
        try :
            Text = urllib.parse.quote(query)
        except:
            print("There is a problem with the input query.")
            return
        
        queryString = "?query="+Text+"&sort="+self.sort+"&page="+str(self.page)+"&size="+str(self.size)

        r = requests.get(self.url + queryString, headers=header)
        return json.loads(r.text)

    def save(self, query:str, path:str):
        data = self.search(query)
        if ".json" not in path:
            path = path + ".json"
        with open(path, 'w', encoding = 'utf-8') as outfile:
            outfile.write(json.dumps(data, ensure_ascii = False))
            print("saved!")

    def __init__(self):
        self.query =""
        self.url = "https://dapi.kakao.com/v2/search/cafe"
        self.sort = "accuracy"
        self.page = 1
        self.size = 10