#! /Library/Frameworks/Python.framework/Versions/3.10/bin/python3
# Virtual Env python - /Quotes-API/quotesapi/bin/python3.10
# Other python location - /usr/local/bin python3
import json
import sqlite3
import subprocess
import sys
import logging
# import datetime
# import mysql.connector

quotequery = "SELECT rowid, quote_text, author FROM newest_quotes WHERE used IS NULL ORDER BY random() LIMIT 1"
quotequery_rowid = "SELECT rowid, quote_text, author FROM newest_quotes WHERE rowid = ?"
TABLE_NAME = 'newest_quotes'
DATABASE_PATH = "/Library/Scripts/Ninxa Scripts/Get_Quotes/Show-Quotes/local/myQuotes.db"

# mysql = mysql.connector().connect(user='nynxa', password='', host='', database='')

def pull_quote(rowid=False): # Pass rowid to pull specific quote, or leave blank to get a random quote
    if len(sys.argv) > 2:
        query = quotequery_rowid
        rowid = sys.argv[2]
    else:
        query = quotequery
    # print("starting pull_quote") # Avoid print statements
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

    # applescript_command = f"osascript -e 'tell application \"Keyboard Maestro Engine\" to setvariable \"quote_json\" to \"{quote_dict}\"'"
    # tell application "Keyboard Maestro Engine" to setvariable "quote_author" to "{author}"
    # tell application "Keyboard Maestro Engine" to setvariable "quote_rowid" to "{new_rowid}"'

    # subprocess.run(applescript_command, shell=True)
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


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        globals()[sys.argv[1]]()
    elif len(sys.argv) > 2:
        globals()[sys.argv[1]](sys.argv[2])
