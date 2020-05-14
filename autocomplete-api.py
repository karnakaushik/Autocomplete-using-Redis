from flask import Flask,request,jsonify
import redis

Redis = redis.StrictRedis(host='127.0.0.1',port=6597,db=0, charset="utf-8", decode_responses=True)

app = Flask(__name__)

@app.route("/")
def root():
    return "Hello world!"

@app.route("/add_word/word=<word>")
def insert(word):
    word = word.strip()
    for index in range(1,len(word)):
        substring = word[0:index]
        Redis.zadd("database",{substring:0})
        print(substring)
    Redis.zadd("database",{(word+'*'):0})
    
    return "add word"

@app.route("/autocomplete/query=<word>")
def find(word):
    word = word.strip()
    autocompleted_words = []
    starting_index = Redis.zrank("database",word)
    if not starting_index:
        return []
    
    range = Redis.zrange("database",starting_index,-1)
    if len(range) == 0 or not range:
        return []
    for data in range:
        data = data[2:-1]
        min_len = min(len(data),len(word))
        if data[0:min_len] != word[0:min_len]:
            return jsonify(autocompleted_words)
            
        if data[-1] == '*':

            autocompleted_words.append(data[0:-1])

    return jsonify(autocompleted_words)



    
if __name__ == "__main__":
    app.run(debug = True, use_reloader=True)