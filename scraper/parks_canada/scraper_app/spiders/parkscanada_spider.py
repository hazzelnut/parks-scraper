#! -*- coding: utf-8 -*-

from scrapy.spiders import Spider 
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose
from scrapy.http import FormRequest, Request
from scrapy.shell import inspect_response

from scraper_app.items import ParksCanada 

import urllib

class ParksCanadaSpider(Spider):
  """Spider for information from parkscanada location's page"""
  name = "parkscanada"
  allowed_domains = ["pc.gc.ca"]
  start_urls = [
    'http://www.pc.gc.ca/en/voyage-travel/recherche-tous-parks-all',
  ]

  # TODO: scrape pictures if possible?
  # TODO: scrape about hours of operation
  # TODO: scrape facilities, if available - icons?
  # TODO: scrape things to do, if available - icons? 
  # TODO: scrape contact info

  provinces = ['ab','bc','mb','nb','nl','nt','ns','nu','on','pe','qc','sk','ty']
  # provinces = ['mb']
  url = 'http://www.pc.gc.ca/api/sitecore/PageComponent/GroupSearchResults'
  head_url = 'http://www.pc.gc.ca'

  location_types = [
    'Parks',
    'Historic sites',
    'Marine conservation areas',
    'Others'
   ]

  def formdata_request(self, idx, type, province):
    keyval = {
      'SelectedGroupSearchSubCategoryValue': province,
      'GroupSearchCategories[0][Name]':'Parks',
      'GroupSearchCategories[0][Checked]':'false',
      'GroupSearchCategories[1][Name]':'Historic sites',
      'GroupSearchCategories[1][Checked]':'false',
      'GroupSearchCategories[2][Name]':'Marine conservation areas',
      'GroupSearchCategories[2][Checked]':'false',
      'GroupSearchCategories[3][Name]':'Others',
      'GroupSearchCategories[3][Checked]':'false'
    }
    # check off input box for the location type to scrape
    checked_key = 'GroupSearchCategories[%d][Checked]' % idx
    keyval[checked_key] = 'true'
    return keyval
    
  def parse(self, response):
    for idx, type in enumerate(self.location_types):
      for province in self.provinces:
        formdata = self.formdata_request(idx, type, province)
        request = FormRequest(url=self.url, formdata=formdata, callback=self.parse_results_page)
        request.meta['province'] = province
        request.meta['type'] = type
        yield request

  def parse_location_page(self, response):
    about_xpath = ('//main/div[@class="maintextblock"]/text()'
             '| //main/p[1]/text()'
             '| //main/div[1]/following-sibling::text()')
    about = response.xpath(about_xpath)
    about = ''.join(about.extract())

    hours_xpath = ('//main//section[contains(@class, "hours-of-operation")]//text()')
    hours = response.xpath(hours_xpath)
    hours = ''.join(hours.extract())
    # only 199 locations covered
    # select name from parks where hours is null;

    # inspect_response(response, self)
    loader = response.meta['loader']
    loader.add_value('about', about)
    loader.add_value('hours', hours or u'nope')
    yield loader.load_item()

  def parse_results_page(self, response):
    province = response.meta['province']
    type = response.meta['type']

    locations = response.xpath('//dl')
    for loc in locations:
      loader = ItemLoader(ParksCanada(), selector=loc)

      # processors
      loader.default_input_processor = MapCompose(unicode.strip)
      loader.default_output_processor = Join()

      loader.add_xpath('name', './/dt//text()')
      loader.add_xpath('summary', './/dd//text()')
      loader.add_value('type', unicode(type))
      loader.add_value('lat', u'lat')
      loader.add_value('long', u'long')
      loader.add_value('province', unicode(province))

      link = loc.xpath('.//dt/a[1]/@href').extract_first()

      if link is not None:
        # inspect_response(response, self)
        link = link.encode('ascii')
        loc_url = self.head_url + link
        request = Request(url=loc_url, callback=self.parse_location_page, dont_filter=True)
        request.meta['loader'] = loader
        yield request
      else:
        """ 
          If there's no link for a location, load give a dummy value to 'about'
          - Also means, no value for Hours of Operation
          - Pictures
          - Contact information
          # lower priority - coming soon
          - Things to do
          - Facilities
        """
        loader.add_value('about', u'nope')
        yield loader.load_item()
