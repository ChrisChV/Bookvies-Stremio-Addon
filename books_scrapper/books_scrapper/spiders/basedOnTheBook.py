# -*- coding: utf-8 -*-
import scrapy
from books_scrapper.items import BasedOnTheBook

class BasedonthebookSpider(scrapy.Spider):
    name = 'basedOnTheBook'
    allowed_domains = ['apps.mymcpl.org']
    start_urls = ['https://apps.mymcpl.org']

    root_url = "https://apps.mymcpl.org/"

    custom_settings = {
        'FEED_URI': "basedOTB.json",
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

    abc = ['a','b','c','d','e','f','g','h','i','j','k',
            'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0-9']

    def parse(self, response):
        for letter in self.abc:
            url = self.root_url + 'botb/book/browse/' + letter
            yield scrapy.Request(
                url,
                callback = self.parseLetter,
                headers = self.headers)


    def parseLetter(self, respose):
        for row in respose.xpath("//table//tr"):
            tds = row.xpath(".//td")
            if len(tds) == 0:
                continue
            bookName = tds[0].xpath("./text()").extract()[0]
            bookName = bookName.replace('/', '').strip()
            bookAuthor = tds[0].xpath("./a/text()")
            if len(bookAuthor) != 0:
                bookAuthor = bookAuthor.extract()[0]
            else:
                bookAuthor = ''
            movieName = tds[1].xpath("./text()").extract()[0]
            movieName = movieName.replace('(', '').strip()
            movieYear = tds[1].xpath("./a/text()").extract()[0]
            item = BasedOnTheBook()
            item['bookName'] = bookName
            item['bookAuthor'] = bookAuthor
            item['movieName'] = movieName
            item['movieYear'] = movieYear
            yield item
            



    
