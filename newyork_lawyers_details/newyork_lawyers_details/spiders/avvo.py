
import scrapy
from urllib import parse



class AvvoSpider(scrapy.Spider):
    name = 'avvo'
    allowed_domains = ['www.avvo.com/all-lawyers/ny/new_york.html']
    start_urls = ['https://www.avvo.com/find-a-lawyer/all-practice-areas/ny/new_york']



    def parse(self, response):

        #Get the links of all practice areas of lawyers
        # print("\n\n\n\n\n", response)

        area_titles =response.xpath("//*[@id='areas-of-law']/div/div[*]/h3/a//@href | //*[@id='areas-of-law']/div/div[*]/ul/li[*]/a//@href").extract()

        # print("\n \n \n practice areas" , area_titles)
        for area_title in area_titles:
            area_url = response.urljoin(area_title)
            yield scrapy.Request(url= area_url, callback = self.parse_area_urls,dont_filter = True)
            break


    def parse_area_urls(self,response):
        # print("response: \t ", response)
        lawyers = response.xpath("/html/body/div[1]/div/div/div[5]/div[2]/section[1]/div[2]/div[5]/ul/li/div/div/div/div[1]/div[2]/div[1]/div[1]/a//@href").extract()

        print("\n \n \n \n ........................" , lawyers)
        for lawyer in lawyers:
            url = response.urljoin(lawyer)
            print(url)
            yield scrapy.Request(url, callback=self.parse_lawyer_page, dont_filter=True)
            break
        next_page = response.xpath("//li[@class='pagination-next']//@href").extract_first()

        if next_page:
            next_page_url = response.urljoin(next_page)
            # print("\n \n \n", next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_area_urls, dont_filter=True)
    
