# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NaverwebtoonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    titleID = scrapy.Field()
    title = scrapy.Field()
    genre = scrapy.Field()
    artist = scrapy.Field()
    description = scrapy.Field()
    pass
