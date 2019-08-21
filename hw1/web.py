import os
import sqlite3
from scrape_scholar import scrape
from db_scholar import insert_db
from db_scholar import list_table
from flask import Flask, render_template,request,g

DATABASE = 'C:/Users/guilh/Documents/GitHub/FDS-Homeworks/hw1/gsdb.db'

conn = sqlite3.connect(DATABASE)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html");

@app.route('/scrape',methods = ['GET','POST'])
def scraper():
    x = request.form['author'];
    insert_db(x);
    authors = list_table('author');
    papers = list_table('paper');
    disp = list(scrape(x))
    return render_template("index.html", message=disp);

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True);
