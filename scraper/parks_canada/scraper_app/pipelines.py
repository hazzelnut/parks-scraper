from sqlalchemy.orm import sessionmaker
from models import Parks, db_connect, create_parks_table

from scrapy.pipelines.images import ImagesPipeline 
from scrapy.http import Request
from scrapy.exceptions import DropItem

# TODO Figure out how to put a separate pipeline for images only

class ParksCanadaPipeline(object):

  """ Download images from url - goes to item_completed"""
  def get_media_requests(self, item, info):
    for image_url in item['image_urls']:
      yield scrapy.Request(image_url)

  def item_completed(self, results, item, info):
    image_paths = [x['path'] for ok, x in results if ok]
    if not image_paths:
      raise DropItem("Item contains no images")
    item['image_paths'] = image_paths
    return item

  """ParksCanada pipeline for storing scraped items in the database"""
  def __init__(self):
    """
    Initializes database connection and sessionmaker.
    """
    engine = db_connect()
    create_parks_table(engine)
    self.Session = sessionmaker(bind=engine)

  def process_item(self, item, spider):
    """Save parks in the database.
    
    This method is called for every item pipeline component.
    
    """
    session = self.Session()
    park = Parks(**item)
    
    try:
      session.add(park)
      session.commit()
    except:
      session.rollback()
    finally:
      session.close()

    return item
