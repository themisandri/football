'''Create an api with flask'''

from algorith import algorithm
from flask import Flask, jsonify, request, render_template
from data import get_data, transform_data
from bot_message import telegram_bot_sendtext
import jsonpickle
import sys

app = Flask(__name__)

#hello world
@app.route('/', methods=['GET'])
def hello_world():
    return render_template("home.html", title="Bet 365 bot")
    


@app.route('/api', methods=['GET'])
def show_matches():
    data = get_data()
    df = transform_data(data)
    #print dataframe with flask
    #return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    results = algorithm(df)
    df = df[['id','date','timer','name_teamA','name_teamB','shoots_total','shoots_on_total','shoots_on_percentage','corners_total','red_cards_total','bet365_url']]
    return render_template("bootstrap_table.html", column_names=df.columns.values, row_data=list(df.values.tolist()),
                           link_column="bet365_url", zip=zip, title="Live Matches", filtered=results)
    

#route for algorithm
@app.route('/api/algorithm', methods=['GET'])
def recommendations():
    data = get_data()
    df = transform_data(data)
    results = algorithm(df)
    if results:
        telegram_bot_sendtext(results)
    return jsonpickle.encode(results)


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5555, debug = False)


