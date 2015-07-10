# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient,errors,DESCENDING
import datetime
import hashlib
import datetime
class MoviesPipeline(object):
    def __init__(self):
        self.client = MongoClient('mongodb://127.0.0.1:27017/')
        self.db = self.client['movies']
        self.posts = self.db['douban']
    def process_item(self, item, spider):
        storeContent = item.toDict()
        storeContent['_id']=item['imdbId']
        storeContent['update_time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print storeContent
        try:
            post_id = self.posts.insert(storeContent)
            print 'store 2 mongo :',post_id
        except errors.DuplicateKeyError,e:
            raise Exception('err','DuplicateKeyError')
            pass
        return item
