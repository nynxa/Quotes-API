from time import sleep
from bs4 import BeautifulSoup
import requests
import random


class GoodReads:
    def __init__(self):
        pass

    @staticmethod
    def extract(url):
        results = []
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        nextpage = soup.find("a", class_="next_page")
        lastpage = nextpage.find_previous_sibling("a").text
        for quote in soup.find_all("div", class_= "quote"):
            squote = {}
            squote['text'] = quote.find("div", class_ = "quoteText").text.replace('\n', ' ').rsplit("\u2015", 1)[0].strip()
            author_title = quote.find_all("span", "a", class_ = "authorOrTitle", limit = 2)
            squote['author'] = author_title[0].text.replace('\n', ' ').strip()
            if len(author_title) > 1:
                title = author_title[1].text.replace('\n', ' ').strip()
                squote['author'] = f"{squote['author']}, {title}"
            leftAlignedImage = quote.find("a", {"class": "leftAlignedImage"})
            image = leftAlignedImage.img['src'] if leftAlignedImage else None
            squote['image'] = image
            if image:
                squote["image"] = image.replace("p2", "p8") 
            quoteFooter = quote.find("div", {"class": "quoteFooter"})
            squote['tags'] = [tag.text.strip() for tag in quoteFooter.find_all("a") if tag and "likes" not in tag.text]
            squote['lastpage'] = lastpage
            results.append(squote)
        return results

    @property
    def random(self):
        ran_pageNo = random.randint(1, 99)
        baseUrl = f"https://www.goodreads.com/quotes?format=html&mobile_xhr=1&page={ran_pageNo}"
        results = GoodReads.extract(baseUrl) 
        return results[random.randint(0, len(results))]
        
        
    @staticmethod
    def search_all(search_query, pages=1, start_page=1):
        res = []
        pagerange = range(start_page, start_page + pages)
        for page in pagerange:
            rangeindex = pagerange.index(page)
            print(f"scraping page {page}, range index = {pagerange.index(page)}")
            if type(search_query) == int: # Can enter the author ID (get from author URL)
                baseUrl = f"https://www.goodreads.com/author/quotes/{search_query}?page={page}" #Allows use of specific URL from Goodreads
                print(f"search_query = int -> baseUrl = {baseUrl}")
            else: 
                baseUrl = f"https://www.goodreads.com/quotes/search?commit=Search&page={page}&q={search_query.replace(' ', '+')}&utf8=%E2%9C%93"
                print(f"search_query = str -> baseUrl = {baseUrl}")
                
            results = GoodReads.extract(baseUrl)
            res.extend(results)

            if rangeindex > 9 and pages > 10 and (rangeindex + 1) % 5 == 0:
                cont = input(f"finished scraping {rangeindex + 1} pages, CONTINUE? (y/n)")
                if (cont == "n"):
                    break
            if page > start_page:
                wait = random.randint(3, 10)
                print(f"scraped page {page}, waiting {wait} seconds...")
                sleep(wait);
        return res

    @staticmethod
    def search_one(search_query, pages=1, start_page=1):
        res = []
        print(f"calling search_one -> search_query = {search_query}")
        print(f"search_one params: page = {pages}, type = {type(pages)}")
        if type(search_query) == int: # Can enter the author ID (get from author URL)
            baseUrl = f"https://www.goodreads.com/author/quotes/{search_query}?page={start_page}" #Allows use of specific URL from Goodreads
            print(f"search_query = int -> baseUrl = {baseUrl}")
        else:
            baseUrl = f"https://www.goodreads.com/quotes/search?commit=Search&page={start_page}&q={search_query.replace(' ', '+')}&utf8=%E2%9C%93"
            print(f"search_query = str -> baseUrl = {baseUrl}")
        
        results = GoodReads.extract(baseUrl)
        res.extend(results)
        print(f"from search_one -> lastpage = {results[0]['lastpage']}")
        return res
