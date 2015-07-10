# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    def toDict(self):
        return self._values
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()#年份
    type = scrapy.Field()#电影or电视
    genres = scrapy.Field()#标签 类型
    areas = scrapy.Field()#地区
    author = scrapy.Field()#片方
    languages = scrapy.Field()
    pubTime = scrapy.Field()#上映时间
    enName = scrapy.Field()
    alias = scrapy.Field()#别名
    screenwriters = scrapy.Field()#编剧
    directors = scrapy.Field()#导演
    actors = scrapy.Field()
    imdbId = scrapy.Field()
    imdbScore = scrapy.Field()
    introduction = scrapy.Field()
    runtime=scrapy.Field()
    poster  = scrapy.Field()#海报
    download = scrapy.Field()
    site = scrapy.Field()
    siteId = scrapy.Field()
    siteScore = scrapy.Field()#10分制
    siteStars = scrapy.Field()#5 4 3 2 1
    siteVoteCount = scrapy.Field()#评分人数
    pass
