#! /Library/Frameworks/Python.framework/Versions/3.10/bin/python3
# Virtual Env python - /Quotes-API/quotesapi/bin/python3.10
# Other python location - /usr/local/bin python3
import sqlite3
import subprocess
import sys
import datetime
import mysql.connector

quotequery = "SELECT rowid, quote_text, author FROM newest_quotes WHERE used IS NULL ORDER BY random() LIMIT 1"
quotequery_rowid = "SELECT rowid, quote_text, author FROM newest_quotes WHERE rowid = ?"
TABLE_NAME = 'newest_quotes'
DATABASE_PATH = "/Library/Scripts/Ninxa Scripts/Get_Quotes/Show-Quotes/local/myQuotes.db"
DB_PASSWORD = ""

mysql = mysql.connector().connect(user='nynxa', password='', host='', database='')
if len(sys.argv) > 0:
    for arg in sys.argv:
        print(f"arg = {arg}")

def pull_quote():
    print("starting pull_quote")
    con = sqlite3.connect(
        DATABASE_PATH)
    cur = con.cursor()
    try:
        cur.execute(quotequery)
        rows = cur.fetchall()
        if len(rows) > 0:
            for row in rows:
                quoteDict = {
                    "rowid": row[0],
                    "quote": row[1],
                    "author": row[2]
                }
        else:
            return print("No rows found!")

        print(quoteDict)
        cur.close()

    except sqlite3.Error as error:
        print("Unable to update sqlite", error)

    finally:
        if con:
            con.close()

    applescript_command = f"""osascript -e 'tell application "Keyboard Maestro Engine" to setvariable "quote_text" to "{quoteDict['quote']}"
    tell application "Keyboard Maestro Engine" to setvariable "quote_author" to "{quoteDict['author']}"
    tell application "Keyboard Maestro Engine" to setvariable "quote_rowid" to "{quoteDict['rowid']}"'"""

    subprocess.run(applescript_command, shell=True)

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
    update = "UPDATE newest_quotes SET liked = 1, used = 1 WHERE rowid = ?"
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
    update = """UPDATE newest_quotes SET liked = 0, used = 1 WHERE rowid = ?"""
    cur = con.cursor()
    cur.execute(update, (rowid,))
    con.commit()
    cur.close()
    con.close()

    applescript_command = f"""osascript -e 'tell application "Keyboard Maestro Engine" to setvariable "lastUsedQuoteRow" to "{rowid}"'"""

    subprocess.run(applescript_command, shell=True)

def pull_quote_by_rowid(rowid):
    print(f"starting pull quote by rowid, rowid = {rowid}")
    for arg in sys.argv:
        print(f"arg from pull_quote_by_rowid = {arg}")
    if len(sys.argv) <= 2:
        print(f"you didnt pass a rowid!")
    else:
        rowid = sys.argv[2]
        con = sqlite3.connect(DATABASE_PATH)

    cur = con.cursor()
    try:
        cur.execute(quotequery_rowid, (rowid,))
        row = cur.fetchone()
        print(f"quote by rowid returned {row}")

        # for col in row:
        #     quoteDict = {
        #         "rowid": col[0],
        #         "quote": col[1],
        #         "author": col[2]
        #     }
        
        applescript_command = f"""osascript -e 'tell application "Keyboard Maestro Engine" to setvariable "quote_text" to "{row[0]}"
        tell application "Keyboard Maestro Engine" to setvariable "quote_author" to "{row[1]}"
        tell application "Keyboard Maestro Engine" to setvariable "quote_rowid" to "{row[2]}"'"""

        subprocess.run(applescript_command, shell=True)

    except sqlite3.Error as error:
        print("error getting quote by rowid ", error)
    finally:
        cur.close()
        con.close()


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        globals()[sys.argv[1]]()
    elif len(sys.argv) > 2:
        globals()[sys.argv[1]](sys.argv[2])
