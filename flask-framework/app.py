from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE

app = Flask(__name__)

@app.route('/',methods=["GET"])
def index():
    return render_template('index2.html')
          
@app.route('/index',methods=["POST"])
def about():
    #download data from quandl server
    symbol = request.form["symbol"]
    if len(symbol) < 1: symbol = 'AAPL'
    start_date = request.form["start_date"]
    if len(start_date) < 1: start_date = '2017-01-01'
    end_date = request.form["end_date"]
    if len(end_date) < 1: end_date = '2017-01-31'
    serviceurl = 'https://www.quandl.com/api/v3/datasets/WIKI/'
    symboljs = symbol+'.json'
    serviceurl_symbol = serviceurl+symboljs
    api_key = 'QQjndsVJFRSLguryrfA2'
    req = {'start_date':start_date,'end_date': end_date,'api_key': api_key}
    data = requests.get(serviceurl_symbol,params = req)
    js = json.loads(data.content)
    #prepare data in pandas dataframe
    df = pd.DataFrame(js['dataset']['data'],columns = js['dataset']['column_names'])
    df['Date'] = pd.to_datetime(df['Date'],format = "%Y-%m-%d").dt.date
    df.set_index(['Date'],drop = True, inplace=True)
    #making the bokeh figure
    p = figure(width=900,height=600,x_axis_type="datetime")
    #get the lists of selections
    features=request.form.getlist('features')
    if not features:
        features = ['Close']
    colors = {'Open':'blue',
          'Low':'green',
          'High':'red',
          'Close':'black'}
    for selection in features:
        p.circle(df.index,df[selection],size=5,alpha=0.2,fill_color=colors[selection],legend=selection)
        p.line(df.index,df[selection],color=colors[selection],line_width=3,legend=selection)
    
    
    #adjust figure properties
    p.title.text = "Quandl WIKI Stock Price"
    p.legend.location = "top_left"
    p.legend.label_text_font_size = '18pt'
    p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    p.xaxis.axis_label_text_font_size = '18pt'
    p.xaxis.major_label_text_font_size = '14pt'
    p.yaxis.axis_label = 'Price'
    p.yaxis.axis_label_text_font_size = '18pt'
    p.yaxis.major_label_text_font_size = '14pt'
    p.ygrid.band_fill_color = "olive"
    p.ygrid.band_fill_alpha = 0.1
    #resources are needed to replace the head section in boilerplate
    resources = INLINE.render()
    script,div = components(p)
    return render_template('about.html',ticker=symbol,script=script,div=div,\
                           resources=resources,start_date=start_date,end_date=end_date,\
                          features=features)
    
if __name__ == '__main__':
  app.run(port=33507)
