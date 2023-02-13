from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.utils.project import get_project_settings
from yemeksepeti import YemeksepetiScrapy
from flask import Flask 
import os, signal, sys, datetime,gunicorn, scrapy

settings = get_project_settings()
#settings['DUPEFILTER_DEBUG'] = False
process = CrawlerProcess(settings)
process.crawl(YemeksepetiScrapy)
process.start()