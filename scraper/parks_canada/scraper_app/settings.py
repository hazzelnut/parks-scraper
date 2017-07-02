BOT_NAME = 'parkscanada'

SPIDER_MODULES = ['scraper_app.spiders']

ITEM_PIPELINES = {'scraper_app.pipelines.ParksCanadaPipeline': 100}

DATABASE = {
  'drivername': 'postgres',
  'host': 'localhost',
  'port': '5432',
  'username': 'ericchan',
  'password': '',
  'database': 'parks',
}

# Directory to store images
IMAGES_STORE = 'images'
