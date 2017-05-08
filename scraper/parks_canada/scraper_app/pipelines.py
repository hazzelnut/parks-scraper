from sqlalchemy.orm import sessionmaker
from models import Parks, db_connect, create_parks_table

class ParksCanadaPipeline(object):
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
