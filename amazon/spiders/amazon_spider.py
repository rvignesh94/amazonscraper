import scrapy
from ..items import AmazonItem



class AmazonSpider(scrapy.Spider):
    search_for = input("Enter the item to search: ")
    name = 'amazon'
    page_number = 2
    max_page_number = int(input("Enter the maximum pages to search: "))

    start_urls = [f'https://www.amazon.in/s?k={search_for}&page=1']


    def parse(self, response):
        items = AmazonItem()
        results = response.css('.s-border-bottom')   
        for result in results:
            name = result.css("span.a-text-normal").css("::text").extract_first()
            rating = result.css(".a-size-small .a-size-base").css("::text").extract_first()
            price = result.css(".a-price-whole").css("::text").extract_first()
            li = result.css(".a-text-normal::attr(href)").extract_first()
            link = f'https://www.amazon.in{li}'
            
            items["product_name"] = name
            items["product_rating"] = rating
            items["product_price"] = price
            items["product_link"] = link
            yield items
        

        next_page = f"https://www.amazon.in/s?k={AmazonSpider.search_for}&page={AmazonSpider.page_number}"

        if AmazonSpider.page_number <= AmazonSpider.max_page_number:
            AmazonSpider.page_number += 1
            yield response.follow(next_page, callback= self.parse)