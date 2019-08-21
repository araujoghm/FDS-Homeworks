#!/usr/bin/env python
# coding: utf-8

# In[9]:


import sqlite3
import pandas as pd
from scrape_scholar import scrape


# In[10]:


def init_db(database):
    gs=sqlite3.connect(database)
    
    gs.cursor().execute("""
    CREATE TABLE author (
    "id" INTEGER PRIMARY KEY  NOT NULL ,
    "author_name" VARCHAR NOT NULL UNIQUE
    );
    
    """)
    
    gs.cursor().execute("""
    CREATE TABLE paper (
    "id" INTEGER PRIMARY KEY  NOT NULL ,
    "paper_name" VARCHAR NOT NULL UNIQUE
    );
    
    """)
    
    gs.cursor().execute("""                    
    CREATE TABLE author_paper (
    paper_id INTEGER,
    author_id INTEGER,
    FOREIGN KEY(paper_id) REFERENCES paper(id)
    FOREIGN KEY(author_id) REFERENCES author(id)
    );
    
    """)
    
    gs.commit()


# In[5]:


def insert_db(author_name):
    
    try:
        init_db('gsdb.db')
    except:
        pass
    
    try:
        gs=sqlite3.connect('gsdb.db')        
        
        df=pd.DataFrame(scrape(author_name))
        
        author_df = df['authors'].apply(pd.Series).stack(dropna=True).reset_index(drop=True, level=1).rename('author').to_frame()
        paper_df = df['title'].apply(pd.Series).stack(dropna=True).reset_index(drop=True, level=1).rename('paper').to_frame()
        author_paper_df= author_df.join(paper_df, how='outer')

        authors_unique = list(author_df['author'].unique())
        papers_unique = list(paper_df['paper'].unique())
        
        for i in range(0,len(authors_unique)):      
            try:
                gs.cursor().execute("""INSERT INTO author (author_name)
                VALUES(?)""",(authors_unique[i],))
            except:
                pass
    
        for i in range(0,len(papers_unique)):
            try:
                google_s.execute("""INSERT INTO paper (paper_name)
                VALUES(?)""", (papers_unique[i],))
            
                for k in range(0,len(papers_df[i].get('authors'))):
                    google_s.execute("""INSERT INTO author_paper (author_id, paper_id)
                    VALUES(?,?)
                    """, (author_paper_df[i],))
            except:
                pass
        gs.commit()
    
    except NameError:
            return print('Sua busca não encontrou nenhum autor com esse nome no Google Scholar.')


# In[13]:


def list_table(table):
    
    gs=sqlite3.connect('gsdb.db',timeout=1)
        
    gs.cursor().execute("""SELECT * FROM {0};""".format(table))
    
    return list(gs.cursor().fetchall())
    
    gs.commit()
    gs.close
