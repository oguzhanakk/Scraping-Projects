from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.utils.project import get_project_settings
from cimri import CimriSpider
from flask import Flask 
import os, signal, sys, datetime,gunicorn, scrapy

def main(arg):
    process = CrawlerProcess(settings={'LOG_LEVEL': 'ERROR'})
    process.crawl(CimriSpider, page=arg)
    process.start()
    #CimriSpider(page=arg).postgre_insert()
    return "Success!"
if __name__=='__main__':
    try:
        arg = sys.argv[1]
    except:
        arg = 'None'
    print('Given argument:',arg)
    main(arg)