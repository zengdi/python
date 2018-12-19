#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-12-18 19:34:21
# Project: EcoLett_spider

from pyspider.libs.base_handler import *
import time


class Handler(BaseHandler):
    crawl_config = {
    }

    # start page crawl and call the volume parse function
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://onlinelibrary.wiley.com/loi/14610248', callback=self.index_volume, retries=10)

    # parsing the volume page and call the issue parsing function
    @config(age=10 * 24 * 60 * 60)
    def index_volume(self, response):
        for each in response.doc('ul.loi__list li a').items():
            self.crawl(each.attr.href, callback=self.index_issue)

    # parsing each issue and call the doi page parsing function
    @config(age=10 * 24 * 60 * 60)
    def index_issue(self, response):
        for each in response.doc('div h4 a').items():
            self.crawl(each.attr.href, callback=self.doi)

    # obtaing each paper based on the doi and call the page detail parsing function
    @config(age=10 * 24 * 60 * 60)
    def doi(self, response):
        for each in response.doc('div .issue-item a.issue-item__title').items():
            self.crawl(each.attr.href, callback=self.detail_page)
            time.sleep(0.5)

    # parsing each paper page to get information of paper
    @config(priority=2)
    def detail_page(self, response):
        # obtaining the author list of the paper
        authors = []
        for author in response.doc(".accordion-tabbed a.author-name span"):
            authors.append(author.text)

        # return the final information
        return {
            # "url": response.url,
            "title": response.doc("div .citation__title").text(),
            "authors": ','.join(authors),
            "address": response.doc('div div#a1 p').text()
        }
