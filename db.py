import sqlite3
from typing import List

from parse import NewsDetails

INIT_SQL = [
    'create table posts(id number not null primary key, title text, description text, content text, images text, time timestamp);',
    'create table views(id number, count number, time timestamp);',
]


def submit_views(news: List[NewsDetails]):
    with sqlite3.connect('data/storage.sqlite') as con:
        cur = con.cursor()

        for n in news:
            cur.execute('insert into views values (?, ?, current_timestamp)', (n.id, n.views))

        con.commit()
        cur.close()


def save_post(post_id, title, description, content, images, published):
    with sqlite3.connect('data/storage.sqlite') as con:
        cur = con.cursor()

        cur.execute('insert or ignore into posts values (?, ?, ?, ?, ?, ?)',
                    (post_id, title, description, content, images, published))

        con.commit()
