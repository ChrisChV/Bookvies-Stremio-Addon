# -*- coding: utf-8 -*-
import scrapy
import json
from books_scrapper.items import IMDBMovie


class PosterscarpySpider(scrapy.Spider):
    name = 'posterScarpy'
    root_url = 'https://www.imdb.com/title/'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com']

    custom_settings = {
            'FEED_URI': "posters.json",
            'FEED_FORMAT': 'json'
        }

    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip', 
        'DNT' : '1',
        'Connection' : 'close'
    }

    def parse(self, response):
        jsonFile = open('outOTB.json')
        data = json.load(jsonFile)
        titleId = ''
        for item in data:
            titleId = item['title_id']
            if titleId is None:
                continue
            yield scrapy.Request(
                self.root_url  + titleId,
                callback = self.parsePoster,
                headers=self.headers,
                meta={'titleId': titleId}
            )
        jsonFile.close()


    def parsePoster(self, response):
        poster = response.xpath("//div[@class='poster']/a/img/@src").extract()
        if len(poster) != 0:
            poster = poster[0]
            item = IMDBMovie()
            item['titleId'] = response.meta['titleId']
            item['posterUrl']  = poster
            yield item
        