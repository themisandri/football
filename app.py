'''Create an api with flask'''

from algorith import algorithm
from flask import Flask, jsonify, request, render_template
from data import get_data, transform_data
from telegram import telegram_bot_sendtext
import sys

app = Flask(__name__)

#hello world
@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


@app.route('/api', methods=['GET'])
def show_matches():
    data = get_data()
    df = transform_data(data)
    #print dataframe with flask
    return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    

#route for algorithm
@app.route('/api/algorithm', methods=['GET'])
def recommendations():
    data = get_data()
    df = transform_data(data)
    results = algorithm(df)
    if results:
        telegram_bot_sendtext(results)
    return results

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5555, debug = False)


