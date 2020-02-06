# -*- coding: utf-8 -*-
import scrapy
import time
from books_scrapper.items import Book

class GutenbergSpider(scrapy.Spider):
    name = 'gutenberg'
    root_url = 'http://www.gutenberg.org'
    allowed_domains = ['www.gutenberg.org']
    start_urls = ['http://www.gutenberg.org']

    custom_settings = {
            'FEED_URI': "out.json",
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
            'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','other']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response):
        yield scrapy.Request(
            self.root_url + '/browse/titles/' + self.letter,
            callback = self.parseLetter,
            headers = self.headers)


    def parseLetter(self, response):
        books = response.xpath("//div[@class='pgdbbytitle']//h2/a")
        languages = response.xpath("//div[@class='pgdbbytitle']//h2/text()").extract()
        if(len(books) != len(languages)):
            yield "Erroooooorr algo anda mal"
        for i in range(0, len(books)):
            lang = languages[i].replace(" ", "")
            lang = lang.replace("(", "")
            lang = lang.replace(")", "")
            if(lang != 'English'):
                continue
            url = books[i].xpath('./@href').extract()[0]
            name = books[i].xpath('./text()').extract()[0]
            author = books[i].xpath("./parent::h2/following-sibling::p/a/text()").extract()
            yield scrapy.Request(self.root_url + url,
                                        callback=self.parseBook,
                                        meta={'name': name, 'author': author[0]},
                                        headers=self.headers)
    
    def parseBook(self, response):
        image = response.xpath("//div[@id='cover']/img/@src").extract()
        if(len(image) == 0):
            image = None
        else:
            image = image[0]
        downloadURLs = {}
        for tr in response.xpath("//table[@class='files']//tr"):
            nameKey = tr.xpath("./td[2]/a/text()").extract()
            url = tr.xpath("./td[2]/a/@href").extract()
            if(len(nameKey) == 0 or nameKey[0] == 'More Files…'):
                continue
            downloadURLs[nameKey[0]] = self.root_url + url[0]
        releaseDate = response.xpath("//table[@class='bibrec']//tr[@datatype='xsd:date']/@content").extract()[0]
        downloads = response.xpath("//table[@class='bibrec']//td[@itemprop='interactionCount']/text()").extract()
        downloads = downloads[0].split(' ')[0]
        item = Book()
        item['name'] = response.meta['name']
        item['author'] = response.meta['author']
        item['imageURL'] = image
        item['downloadURLs'] = downloadURLs
        item['releaseDate'] = releaseDate
        item['downloads'] = downloads
        item['source'] = self.root_url
        yield item

        


                
        
        
        