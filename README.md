# Bookvies-Stremio-Addon

![cover_image](https://i.imgur.com/5RaLI1d.png)

If you are a book lover and want to see what book your favorite movies were based on, you will love this.
This Addon collect all movies that are based on a Book and adds the link to Amazon books of that book. Also adds some books to your Books catalogue from Gutenberg.org.

## Features

- Adds Amazon Books links to movies based on a book.
- Adds additional metadata to movies based on a book.
- Adds a new Book catalogue with books from Gutenberg.org.

## Deploy and Test Addon

1. Run the addon:

 ```bash
 > python3 addon.py
 ```

2. Open Stremio, go to the Addons tab add the manifest http://127.0.0.1:5000/manifest.json
3. You can see the bookvie catalog on Discover > Movies > Bookvies. On each movie, the Addon add the link `Bookvie` to the Amazon book.
4. You can see the book catalog on Discover > Books > Gutenberg Books

### How to generate books_catalog.json

All scripts are running on `books_scrapper` directory.

1. Craw the books with the prefer letter:

 ```bash
 > scrapy runspider books_scrapper/spiders/gutenberg.py -a letter=c
 ```

On the example above, I will crawl the books by the letter `c`. It will generate a `out.json` file.

2. Change `out.json` to the letter name `c.json`.
3. Generate the files with the letters you want.
4. Open the `genCatalog.py` and edit the `_letter` list with your generated letters.
5. Join add files:

 ```bash
 > python3 genCatalog.py
 ```

It will generate the `catalog.json` file. This is the book catalog file.

6. Copy and rename the file:

 ```bash
 > cp catalog.json ../books_catalog.json
 ```

### How to generate bookvies_catalog.json

All scripts are running on `books_scrapper` directory.

1. Crawl the On the Book (OTB) information:

 ```bash
 > scrapy runspider books_scrapper/spiders/basedOnTheBook.py 
 ```

It will generate the `basedOTB.json` file.

2. Download the IMBD databases:

 ```bash
 > wget https://datasets.imdbws.com/title.basics.tsv.gz
 > wget https://datasets.imdbws.com/title.ratings.tsv.gz
 ```

3. Link the movies with the books:

 ```bash
 > python3 linkBooksAndMovies.py
 ```

It will generate the `outOTB.json` file.

4. Crawl posters and movie data from IMBD page:

 ```bash
 > scrapy runspider books_scrapper/spiders/posterScrapy.py
 ```
    
It will generate the `posters.json` file.

5. Link the OTB data with the posters and movie data:

 ```bash
 > python3 addPosterToOTB.py
 ```

It will generate the `outOTB_2.json` file.

6. Crawl the links to Amazon books:

 ```bash
 > scrapy runspider books_scrapper/spiders/amazonBooks.py
 ```

It will generate the `amazonBooks.json` file.

7. Link the OTB data with the amazon books links:

 ```bash
 > python3 linkWithAmazon.py
 ```
    
It will generate the `outOTB_3.json` file. This file is the bookvie catalog.

8. Copy and rename the file:

 ```bash
 > cp outOTB_3.json ../bookvies_catalog.json
 ```






