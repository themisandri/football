from algorith import algorithm, model_predict
from flask import Flask, jsonify, request, render_template
from data import get_data, create_features, transform_data
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
@app.route('/algorithm', methods=['GET'])
def recommendations():
    data = get_data()
    df = transform_data(data)
    results = algorithm(df)
    if results:
        telegram_bot_sendtext(results)
    return render_template("filtered.html", filtered=results)
    
#route for algorithm
@app.route('/model', methods=['GET'])
def model():
    data = get_data()
    df = create_features(data)
    results, match_to_bet = model_predict(data, df)
    #if results:
        #telegram_bot_sendtext(results)
    return render_template("model.html",column_names=match_to_bet.columns.values, row_data=list(match_to_bet.values.tolist()),
                            zip=zip, title="Live Matches", predictions=results)


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5555, debug = False)


