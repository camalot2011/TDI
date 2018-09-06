from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import pandas as pd

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template('index2.html')
    else:
        symbol = request.form["symbol"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        serviceurl = 'https://www.quandl.com/api/v3/datasets/WIKI/'
        symboljs = symbol+'.json'
        serviceurl_symbol = serviceurl+symboljs
        req = {'start_date':start_date,'end_date': end_date}
        data = requests.get(serviceurl_symbol,params = req)
        js = json.loads(data.content)
        df = pd.DataFrame(js['dataset']['data'],columns = js['dataset']['column_names'])
        df['Date'] = pd.to_datetime(df['Date'],format = "%Y-%M-%d").dt.date
        df.set_index(['Date'],drop = True, inplace=True)
        return render_template('about.html')


@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
