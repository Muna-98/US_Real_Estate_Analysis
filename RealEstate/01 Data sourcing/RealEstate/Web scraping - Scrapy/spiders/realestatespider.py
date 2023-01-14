import scrapy
from urllib.parse import urlencode


#Inputting proxy
API_KEY='************************'

def get_proxy_url(url):
    payload = {'url': url, 'x-api-key': API_KEY}
    proxy_url = 'https://api.scrapingant.com/v2/general?' + urlencode(payload)
    return proxy_url 


class RealestatespiderSpider(scrapy.Spider):
    #The name of the spider
    name = 'realestatespider'
    states=['Chicago_IL', 'New-York_NY', 'Los-Angeles_CA', 'Houston_TX', 'Phoenix_AZ', 'Philadelphia_PA', 'San-Antonio_TX', 'San-Diego_CA', 'Dallas_TX', 'San-Jose_CA']
    
    #start_urls = ['https://www.realtor.com/realestateandhomes-search/Chicago_IL']

    def start_requests(self):
        start_url= 'https://www.realtor.com/realestateandhomes-search/San-Diego_CA'
        yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse)


    def parse(self, response):
        
        products=response.css('li[data-testid*="result-card"]') 

        for product in products:
            # Here we put the data returned into the format we want to output for our csv or json file
            yield {
                'address1' : product.css('div[data-label="pc-address"]::text').get(),
                'address2' : product.css('div[data-label="pc-address-second"]::text').getall(),
                'price' : product.css('span[data-label="pc-price"]::text').get(),
                'beds' : product.css('li[data-label="pc-meta-beds"] span[data-label="meta-value"]::text').get(),
                'baths' : product.css('li[data-label="pc-meta-baths"] span[data-label="meta-value"]::text').get(),
                'sqft' : product.css('li[data-label="pc-meta-sqft"] span[data-label="meta-value"]::text').get(),
                'sqftlot' : product.css('li[data-label="pc-meta-sqftlot"] span[data-label="meta-value"]::text').get()
            }
        
        next_page=response.css(' [aria-label="Go to next page"] ::attr(href)').get() 

        if next_page is not None:
            next_page_url = 'https://www.realtor.com'+next_page
            yield response.follow(get_proxy_url(next_page_url), callback=self.parse)
