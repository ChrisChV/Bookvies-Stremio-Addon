# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Book(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    imageURL = scrapy.Field()
    downloadURLs = scrapy.Field()
    releaseDate = scrapy.Field()
    downloads = scrapy.Field()
    source = scrapy.Field()
    
