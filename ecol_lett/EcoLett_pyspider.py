#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-12-18 19:34:21
# Project: EcoLett_spider

from pyspider.libs.base_handler import *
import time
import sqlite3


class Handler(BaseHandler):
    # Initialize the database to sotre the paper data
    def __init__(self):
        self.db = sqlite3.connect("/home/zengdi/Documents/pythonProjects/data/papers.db")
        print("Intializing database successfully!")
        self.cursor = self.db.cursor()
        self.ID = 1

    # funtion to add data to database
    def add_Mysql(self, ID, url, year, month, title, authors, address, keywords, Pub_history, paper_type):
        try:
            sql = 'insert into ecology_letter(id, url, year, month, title, authors, address, keywords, Pub_history, paper_type) values (%d,"%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            ID, url, year, month, title, authors, address, keywords, Pub_history, paper_type);  # 插入数据库的SQL语句
            print(sql)
            self.cursor.execute(sql)
            print(self.cursor.lastrowid)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    crawl_config = {
        "user_agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "retries": 20,
        "itag": 'v50',
        "connect_timeout": 300,
        "timeout": 600
    }

    # start page crawl and call the volume parse function
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://onlinelibrary.wiley.com/loi/14610248', callback=self.index_volume)

    # parsing the volume page and call the issue parsing function
    @config(age=1 * 60)
    def index_volume(self, response):
        for each in response.doc('ul.loi__list li a').items():
            self.crawl(each.attr.href, callback=self.index_issue)

    # parsing each issue and call the doi page parsing function
    @config(age=1 * 60)
    def index_issue(self, response):
        for each in response.doc('div h4 a').items():
            self.crawl(each.attr.href, callback=self.doi)

    # obtaing each paper based on the doi and call the page detail parsing function
    @config(age=1 * 60)
    def doi(self, response):
        for each in response.doc('div .issue-item a.issue-item__title').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js',
                       js_script="""
                      function(){
                          setTimeout(2000)
                      }""")

    # parsing each paper page to get information of paper
    @config(priority=2)
    def detail_page(self, response):
        # write data to local database created by sqlite3
        url = ''
        title = ''
        address = ''
        paper_type = ''
        year = ''
        month = ''
        # obtaining the author list of the paper
        authors = []
        for author in response.doc(".accordion-tabbed a.author-name span"):
            authors.append(author.text)
        keywords = []
        for keyword in response.doc("div .active section .keywords a"):
            # print(keyword.text)
            keywords.append(keyword.text)
        pub_his = {}
        publication_history = response.doc("section .publication-history ul li").items()
        try:
            for each in publication_history:
                item = each.text().split(":")[0]
                date = each.text().split(":")[1]
                pub_his[item] = date
        except Exception as e:
            print(e)
            pub_his = {}

        paper_type = response.doc("div .primary-heading").text()
        if paper_type == "":
            paper_type = "original research"

        try:
            url = response.url
            title = response.doc('div .citation__title').text()
            authors = ','.join(authors)
            address = response.doc('div div#a1 p').text()
            keywords = ','.join(keywords)
            # Pub_history = pub_his
            # paper_type = paper_type
            year = response.doc('div.extra-info-wrapper p').eq(1).text().split(" ")[1]
            month = response.doc("div.extra-info-wrapper p").eq(1).text().split(" ")[0]
        except Exception as e:
            print(e)
        finally:
            self.add_Mysql(self.ID, url, year, month, title, authors, address, keywords, pub_his, paper_type)
            self.ID += 1

        # return the final information
        return {
            "url": url,
            "title": title,
            "authors": authors,
            "address": address,
            "keywords": keywords,
            "Pub_history": pub_his,
            "paper_type": paper_type,
            "year": year,
            "month": month
        }
