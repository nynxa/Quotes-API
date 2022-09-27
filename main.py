from flask import Flask, jsonify
from goodreads import GoodReads

api = Flask(__name__)

@api.route('/')
def index():
    res = {
      'status': 200,
      'about': 'Quotes api by nynxa (forked from github.com/W4RR10R/Quotes-API',
      'usage': [
         '/random',
         '/search/query',
         '/search/query/num_of_pages',
         '/search/query/num_of_pages/start_page'
       ],
       'options': [
           'num_of_pages (optional) defaults to 1',
           'if num_of_pages = -1, will scrape all pages',
           'query can be either a keyword or the author code (found in author profile URL)'
       ]
    }
    return jsonify(res)
 
@api.route('/random')
def random_quotes():
    return jsonify(GoodReads().random)

@api.route('/search')
def search():
    res = {
       "error": {
          'status': 400,
          'detail': 'No search query found'
       }
    }
    return jsonify(res)
 # Flask Routing -> https://flask.palletsprojects.com/en/2.2.x/quickstart/#routing
@api.route('/search/<query>')
@api.route('/search/<query>/<pages>')
@api.route('/search/<query>/<pages>/<start_page>')
def search_quotes(query, pages=1, start_page=1):
    results = []
    print(f"pages = {pages} and is type {type(pages)}")
    if query.isdigit():
        query = int(query)
    if int(pages) == -1:
        print(f"pages = -1, calling search_one")
        results = GoodReads.search_one(query, int(1), int(start_page))
        totalpages = results[0]['lastpage']
        results = GoodReads.search_all(query, int(totalpages), int(start_page) + 1)
    else:
        results = GoodReads.search_all(query, int(pages), int(start_page))

    # results = GoodReads.search_one(query, 1, int(start_page))

    return jsonify(results)
       
if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000, debug=True)