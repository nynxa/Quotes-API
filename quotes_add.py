import json
import sqlite3
import datetime
import pytz
from dotenv import load_dotenv
import requests
import os
load_dotenv()

# Environment variables
DATABASE_PATH = os.getenv('DATABASE_PATH')
SERVER_URL = os.getenv('LOCAL_SERVER')
TABLE_NAME = os.getenv('TABLE_NAME')

# Make API Call to local server running
def api_call(search_query: str | int, pages=1, start_page=1):
    r = requests.get(f"{SERVER_URL}/search/{search_query}/{pages}/{start_page}")
    result = r.json();
    write_scrape_history(search_query, pages, start_page)
    add_to_database(result)

def add_to_database(json: json):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    rows = []
    for i in json:
       author = i['author']
       quote_text = i['text']
       rows.append((quote_text, author))
    cur.executemany("INSERT OR IGNORE INTO ? (quote_text, author) VALUES(?, ?)", TABLE_NAME, rows)
    con.commit()
    lastrow = cur.lastrowid
    totalrows = cur.rowcount
    print(f"added {totalrows} out of {len(json)} quotes to database -> lastrow = {lastrow}")
    cur.close()
    con.close()

def write_scrape_history(query, pages, start_page):
    doc = open('scrape_history.txt', 'a')
    est = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
    localtime = est.strftime('%x %H:%M %p')
    doc.write(f"{localtime} - {query} - {pages} pages start_page = {start_page}\n")
    print(f"added {query} to scrape_history.txt")

def author_quote_count(author):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("SELECT rowid, author FROM newest_quotes WHERE author LIKE ? OR quote_text LIKE ?", (author, author))
    results = cur.fetchall()
    print(f"total quotes by {author} = {len(results)}, total pages likely = {len(results)/30:.2f}")
    cur.close()
    con.close()

# author_quote_count("%yogananda%")
api_call("autobiography of a yogi", 2, 4)