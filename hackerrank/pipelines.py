# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from hackerrank.items import ProblemDetail, ProblemList, Leader


class HackerrankPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("myhackerrank.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute(""" DROP TABLE IF EXISTS problemlist """)
        self.curr.execute(""" DROP TABLE IF EXISTS problemdetail """)
        self.curr.execute(""" DROP TABLE IF EXISTS leader """)

        self.curr.execute(""" create table problemlist(
                        id integer primary key,
                        name text,
                        success_ratio real,
                        max_score integer,
                        difficulty_name text
                        )""")

        self.curr.execute(""" create table problemdetail(
                        id integer primary key,
                        problem text,
                        sample_input text,
                        sample_output text,
                        pl_id integer,
                        FOREIGN KEY(pl_id) REFERENCES problemlist(id)
                        )""")

        self.curr.execute(""" create table leader(
                        username text,
                        rank integer,
                        score integer
                        )""")

    def process_item(self, item, spider):
        if isinstance(item, ProblemList):
            self.store_problemlist(item)

        if isinstance(item, ProblemDetail):
            self.store_problemdetail(item)

        if isinstance(item, Leader):
            self.store_leader(item)

        return item

    def store_problemlist(self, item):
        self.curr.execute(""" insert into problemlist values (?,?,?,?,?)""", (
            item['id'][0],
            item['name'][0],
            item['success_ratio'],
            item['max_score'],
            item['difficulty_name']
        ))

        self.conn.commit()

    def store_problemdetail(self, item):
        self.curr.execute(""" insert into problemdetail values (?,?,?,?,?)""", (
            item['id'],
            item['problem'],
            item['sample_input'][0],
            item['sample_output'][0],
            item['pl_id'][0]
        ))

        self.conn.commit()

    def store_leader(self, item):
        self.curr.execute(""" insert into leader values (?,?,?)""", (
            item['username'][0],
            item['rank'][0],
            item['score'][0]
        ))

        self.conn.commit()
