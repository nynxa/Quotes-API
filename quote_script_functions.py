#! "/Library/Scripts/Ninxa Scripts/Get_Quotes/Quotes-API/quotesapi/bin/python3"

import json
import sqlite3
import subprocess
import sys
import os
from dotenv import load_dotenv
load_dotenv()

TABLE_NAME = os.getenv('TABLE_NAME')
DATABASE_PATH = os.getenv('DATABASE_PATH')

new_quote_query = f"SELECT rowid, quote_text, author FROM {TABLE_NAME} WHERE used IS NULL ORDER BY random() LIMIT 1"
quotequery_rowid = f"SELECT rowid, quote_text, author FROM {TABLE_NAME} WHERE rowid = ?"
liked_quote_query = f"SELECT rowid, quote_text, author FROM {TABLE_NAME} WHERE liked = 1 AND used = 1 ORDER BY random() LIMIT 1"

def pull_new_quote(rowid=False): # Pass rowid to pull specific quote, or leave blank to get a random quote
    if len(sys.argv) > 2:
        query = quotequery_rowid
        rowid = sys.argv[2]
    else:
        query = new_quote_query
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    try:
        if rowid == False:
            cur.execute(query)
        else:
            cur.execute(query, (rowid, ))
        row = cur.fetchone()

        if len(row) > 1:
            quote_dict = {
                "rowid": row[0],
                "quote": row[1],
                "author": row[2]
                }
        else:
            return print("No rows found!")

        cur.close()

    except sqlite3.Error as error:
        print("Unable to update sqlite", error)

    finally:
        if con:
            con.close()

    quote_json = json.dumps(quote_dict)
    print(quote_json)

# Pass rowid to pull specific quote, or leave blank to get a random quote
def pull_liked_quote(rowid=False): 
    if len(sys.argv) > 2:
        query = quotequery_rowid
        rowid = sys.argv[2]
    else:
        query = liked_quote_query
    # print("starting pull_new_quote") # Avoid print statements
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    try:
        if rowid == False:
            cur.execute(query)
        else:
            cur.execute(query, (rowid, ))
        row = cur.fetchone()

        if len(row) > 1:
            quote_dict = {
                "rowid": row[0],
                "quote": row[1],
                "author": row[2]
                }
        else:
            return print("No rows found!")

        cur.close()

    except sqlite3.Error as error:
        print("Unable to update sqlite", error)

    finally:
        if con:
            con.close()

    quote_json = json.dumps(quote_dict)
    print(quote_json)

def update_liked(rowid):
    print(f"starting update_used -> rowid = {rowid}")
    for arg in sys.argv:
        if (len(sys.argv) <= 2):
            print(f"you didnt pass a rowid")
            for arg in sys.argv:
                print(f"arg from update_liked = {arg}")
        else:
            rowid = sys.argv[2]

    con = sqlite3.connect(
        DATABASE_PATH)
    update = "UPDATE newest_quotes SET liked = 1, used = used + 1 WHERE rowid = ?"
    cur = con.cursor()
    cur.execute(update, (rowid,))
    con.commit()
    cur.close()
    con.close()

    applescript_command = f"""osascript -e 'tell application "Keyboard Maestro Engine" to setvariable "lastUsedQuoteRow" to "{rowid}"
    tell application "Keyboard Maestro Engine" to setvariable "quote_liked_row" to "{rowid}"'"""

    subprocess.run(applescript_command, shell=True)


def update_disliked(rowid):
    print(f"starting update_used -> rowid = {rowid}")
    for arg in sys.argv:
            print(f"arg from update_disliked = {arg}")
    if len(sys.argv) <= 2:
        print(f"you didnt pass a rowid")
    else:
        rowid = sys.argv[2]
            
    con = sqlite3.connect(
        DATABASE_PATH)
    update = """UPDATE newest_quotes SET liked = 0, used = used + 1 WHERE rowid = ?"""
    cur = con.cursor()
    cur.execute(update, (rowid,))
    con.commit()
    cur.close()
    con.close()

    applescript_command = f"""osascript -e 'tell application "Keyboard Maestro Engine" to setvariable "lastUsedQuoteRow" to "{rowid}"'"""
    subprocess.run(applescript_command, shell=True)


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        globals()[sys.argv[1]]()
    elif len(sys.argv) > 2:
        globals()[sys.argv[1]](sys.argv[2])
