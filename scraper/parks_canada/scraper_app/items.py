#! -*- coding: utf-8 -*-

"""
Web Scraper

Scrape data from parkscanada's website and save it to
a postgres database.

Defining a container here for scraped data
"""

from scrapy.item import Item, Field

class ParksCanada(Item):
  name = Field()
  summary = Field()
  about = Field()
  type = Field()
  lat = Field()
  long = Field()
  province = Field()
