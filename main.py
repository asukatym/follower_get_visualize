import sqlite3
from dotenv import load_dotenv
load_dotenv()
import os
from bokeh.plotting import figure, output_file, show
import pandas as pd
from bokeh.models import DatetimeTickFormatter
from bokeh.io import export_png
from datetime import datetime
import requests
from selenium import webdriver
import follower_get        

class Mitoma:
    x=[]
    y=[]
    def __init__(self):
        pass
        
    def sqlite_select(self):
        dbname = os.getenv('DBPATH')
        con = sqlite3.connect(dbname)
        con.text_factory = lambda b: b.decode(errors = 'ignore')
        df = pd.read_csv('mitoma.csv',encoding='shift_jis')
        df.columns = ['date','followers']
        df['followers']=df['followers'].str.replace('万','')
        ##write into sql
        df.to_sql("mitoma",con=con,if_exists='replace',index=False)
        cur = con.cursor()
        cur.execute('SELECT date FROM mitoma')
        global x
        x = [(x[0]) for x in cur.fetchall()]
        ## extract day & hours
        x_list = []
        for i in range(len(x)):
            s = x[i]
            sep = ':'
            t = s.split(sep) 
            r = t[0]
            x_list.append(r)
        self.x = pd.to_datetime(x_list)
        cur.execute('SELECT followers FROM mitoma')
        global y
        y = [(y[0]) for y in cur.fetchall()]
        self.y =  y
        con.close()

    def graph_draw(self):
    # output to static HTML file
        output_file('HTMLPATH')
    # create a new plot with a title and axis labels
        self.p = figure(title="mitoma followers", width=1000, height=500,x_axis_type="datetime",x_axis_label='x', y_axis_label='y',x_range=[self.x[0],self.x[len(self.x)-1]])
        self.p.line(x=self.x, y=self.y,line_width=2)
        self.p.xaxis.formatter=DatetimeTickFormatter(
    
        hours=["%Y-%m-%d %H:%M:%S"],
        days=["%Y-%m-%d %H:%M:%S"],
        months=["%Y-%m-%d %H:%M:%S"],
        years=["%Y-%m-%d %H:%M:%S"],
)
        
        

        
    # show the results
        show(self.p)
        
    def export_graph(self):
        export_png(self.p,filename='output1.png')  
    
    # send to LINE App
    def send_line_notify2(self,message):
        files = {'imageFile': open("output1.png", "rb")}
        line_notify_token = os.getenv('TOKEN')
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {line_notify_token}'}
        data = {'message': f'message: {message}'}
        requests.post(line_notify_api, headers = headers,data = data,files=files)
   
mitoma = Mitoma()
mitoma.sqlite_select()
mitoma.graph_draw()
mitoma.export_graph()
message = 'フォロワー推移'
mitoma.send_line_notify2(message)
