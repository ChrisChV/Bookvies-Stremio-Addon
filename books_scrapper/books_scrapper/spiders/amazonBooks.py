# -*- coding: utf-8 -*-
import scrapy
import json
import sys
import time
from books_scrapper.items import AmazonBook
from scrapy.exceptions import CloseSpider

class AmazonbooksSpider(scrapy.Spider):
    name = 'amazonBooks'
    root_url = 'https://www.amazon.com/'
    allowed_domains = ['www.amazon.com']
    start_urls = [root_url]

    custom_settings = {
        'FEED_URI': "amazonBooks.json",
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

    amazonBooks = {}

    #headers = {
    #    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    #}
    
    def parse(self, response):
        book_title = ""
        book_author = ""
        titleId = ""
        jsonFile = open('outOTB_2.json')
        data = json.load(jsonFile)
        jsonFile.close()
        jsonFile = open('ab.json')
        abData = json.load(jsonFile)
        jsonFile.close()
        for item in abData:
            self.amazonBooks[item['titleId']] = True
        count = 0
        for item in data:
            count += 1
            book_title = item['bookName']
            book_author = item['bookAuthor']
            titleId = item['title_id']
            if titleId in self.amazonBooks:
                continue
            yield scrapy.Request(
                self.root_url + 's?k=' + book_title + '&i=stripbooks',
                callback=self.parseBook,
                headers=self.headers,
                meta={
                    'book_author': book_author,
                    'titleId': titleId
                }
            )
            time.sleep(1)

    def parseBook(self, response):
        check = response.xpath("//html//title/text()").extract()
        if len(check) != 0:
            check = check[0].strip()
            if check == "Robot Check":
                print("AHHH!! Robot Check")
                print("Aborting..")
                print("Last id: " + response.meta['titleId'])
                raise CloseSpider('bandwidth_exceeded')

        results = response.xpath("//div[@class='s-result-list s-search-results sg-row']")
        real_author = response.meta['book_author'].split(',')
        if len(real_author) != 2:
            return
        real_author[0] = real_author[0].strip()
        real_author[1] = real_author[1].strip()
        
        for div in results:
            author = div.xpath(".//div[@class='a-row a-size-base a-color-secondary']/a/text()").extract()
            if len(author) == 0:
                continue
            author = author[0].strip()
            if(author.find(real_author[0]) != -1 or author.find(real_author[1]) != -1):
                image = div.xpath(".//img")
                bookImageUrl = image.xpath("./@src").extract()[0]
                bookUrl = image.xpath("./parent::div/parent::a/@href").extract()[0]
                item = AmazonBook()
                item['titleId'] = response.meta['titleId']
                item['bookPosterUrl'] = bookImageUrl
                item['amazonBookUrl'] = self.root_url + bookUrl
                yield item
                break