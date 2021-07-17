# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PsawcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    postId = scrapy.Field()
    keyword = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    subreddit = scrapy.Field()
    comments = scrapy.Field()
    pass
