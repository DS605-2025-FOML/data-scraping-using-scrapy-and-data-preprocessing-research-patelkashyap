import scrapy
from ..items import BooksScrapperItem

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = [
        'https://books.toscrape.com/'
    ]
    
    def parse(self, response):
        all_article_books = response.css("article.product_pod")
        
        for book_article in all_article_books:
            items = BooksScrapperItem()
            
            title = book_article.css('h3 a::text').extract_first()
            
            price = book_article.css('div.product_price p.price_color::text').extract_first()
            
            rating = book_article.css('p.star-rating::attr(class)').extract()
            rating = rating[-1]
            rating = rating.split()[-1]
            
            stock_availability = book_article.css('div.product_price > p:nth-of-type(2)::text').extract()
            stock_availability = ''.join(stock_availability).strip()
            
            items['title'] = title
            items['price'] = price
            items['rating'] = rating
            items['stock_availability'] = stock_availability
            
            yield items
            
        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
