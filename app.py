from flask import Flask, render_template, request, jsonify, session

from classes.grab import Parser
from classes.network import Network
import os

PORT  = int(os.environ.get('PORT', 8000))

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

def build_n(ticker):
    p = Parser()
    n = Network()
        
    df  = p.stock_parser(ticker)
    network_json = n.json_graph(df)  
    return network_json


@app.route("/", methods= ['GET', 'POST'])
def chrt():
    
    ticker = request.form.get('ticker')

    if ticker == None:
        ticker = 'SBER'
        
    session['current'] = ticker   
    return render_template('index.html', data = ticker)

@app.route("/data")
def static_proxy():

    network =  build_n(session.get('current'))
    return jsonify(network)

def main():  
    app.run(host="0.0.0.0", port = PORT, debug=True)
    
if __name__ == '__main__':
    main()