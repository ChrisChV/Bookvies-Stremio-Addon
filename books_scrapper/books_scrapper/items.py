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


class BasedOnTheBook(scrapy.Item):
    bookName = scrapy.Field()
    bookAuthor = scrapy.Field()
    movieName = scrapy.Field()
    movieYear = scrapy.Field()


class IMDBMovie(scrapy.Item):
    titleId = scrapy.Field()
    posterUrl = scrapy.Field()
    cast = scrapy.Field()
    director = scrapy.Field()
    description = scrapy.Field()

class AmazonBook(scrapy.Item):
    titleId = scrapy.Field()
    bookPosterUrl = scrapy.Field()
    amazonBookUrl = scrapy.Field()