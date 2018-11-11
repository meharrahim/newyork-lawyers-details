
import scrapy
from urllib import parse
from newyork_lawyers_details.items import NewyorkLawyersDetailsItem



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
        # print("\n \n \n \n ........................" , lawyers)
        for lawyer in lawyers:
            url = response.urljoin(lawyer)
            # print(url)
            yield scrapy.Request(url, callback=self.parse_lawyer_page, dont_filter=True)
            break

    def parse_lawyer_page(self, response):
        item = NewyorkLawyersDetailsItem()

        # name 
        item["name"] = response.xpath("//span[@itemprop='name']/text()").extract_first()

        print("\n\n\n ..................",item["name"] )

        # area
        practice_areas = response.xpath("//*[@id='practice_areas']/div/div[2]/ol/li/a/text() | //*[@id='js-chart-legend-hidden']/li[*]/a/text()").extract()
        if practice_areas[-1] == 'More\xa0':
            practice_areas.pop()
        practice_areas_dict = [practice_area.split(':\xa0')[0] for practice_area in practice_areas]
        item["practice_areas"] = practice_areas_dict

        print(item["practice_areas"])

        
        # year of license

        item["license"] = response.xpath("//time[@data-timestupletamp='years-active']/text()").extract_first()
        print(item["license"])

        # photo

        item["image"] = response.xpath("//img[@itemprop='image']/@src").extract_first()
        print(item["image"])
        # rating
        item["avvo_rating"] = response.xpath("//span[@class='avvo-rating-modal-info']//@data-rating").extract_first() 
        print(item["avvo_rating"])
        
        # client rating and reviews
        reviews, rating  = response.xpath("//*[@id='client_reviews']/div/div/div/div/div[1]/div[1]/span[2]/span/span/text() | //*[@id='client_reviews']/div/div/div/div/div[1]/div[1]/span[1]/text()").extract()
        reviews = reviews.split('(')[-1].split(')')[0]
        rating = rating.split()[0]
        item["client_rating"] = {'rating': rating, 'reviews': reviews}
        print(item["client_rating"])

        # about the lawyer
        about_me = response.xpath("//*[@id='js-truncated-aboutme']/p/text() | //*[@id='js-truncated-aboutme']/text()").extract()
        about_me = "".join(about_me).replace('\xa0', "").replace("\r", "")
        about_me = " ".join(about_me.split(" "))
        item["about_me"] = about_me
        print(item["about_me"])

        # payment modes

        item["payment_types"] = response.xpath("//*[@id='payments']/div/div/div/div/div/div[2]/p/small/text()").extract()
        print(item["payment_types"])

        # address
        
        company_name = response.xpath("//*[@id='js-v-full-resume']/div[2]/table/tbody/tr[1]/td[1]/text()").extract_first()
        full_address = response.xpath("//*[@id='contact']/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[1]/div/address/span/p[1]/span/text()").extract()
        street_address, address_locality, _, address_region, _, postal_code = full_address
        item["address"] = {'name': company_name, 'street_address': street_address, 'address_locality': address_locality, 'address_region': address_region, 'postal_code': postal_code}
        print(item["address"] )

        # phone numbers
        phone_names = response.xpath("//*[@id='contact']/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[1]/div/address/span/div/span/text()").extract()
        phone_numbers = response.xpath("//*[@id='contact']/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[1]/div/address/span/div/span/a/span/text()").extract()
        phone_numbers = [number.strip() for number in phone_numbers]
        item["phone"] = dict(zip(phone_names, phone_numbers))
        print(item["phone"])

        # location
        
        latitude = response.xpath("//div[@class='v-lawyer-address']//@data-latitude").extract_first()
        longitude = response.xpath("//div[@class='v-lawyer-address']//@data-longitude").extract_first()
        item["geo_details"] = {'latitude': latitude, 'longitude': longitude}

        # url

        item["url"] = response.url

        yield item
        

