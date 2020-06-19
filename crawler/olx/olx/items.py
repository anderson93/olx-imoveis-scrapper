import scrapy
from datetime import datetime

from .settings import db
from pony.orm import Optional, PrimaryKey, Required


class Ad(scrapy.Item):
    portal_name = scrapy.Field()
    updated_at = scrapy.Field()
    address = scrapy.Field()
    zip_code = scrapy.Field()
    bedrooms = scrapy.Field()
    parking_spaces = scrapy.Field()
    is_sold = scrapy.Field()
    area = scrapy.Field()
    price_per_sqt_meters = scrapy.Field()
    bathrooms = scrapy.Field()
    total_price = scrapy.Field()
    type = scrapy.Field()
    release_year = scrapy.Field()
    url = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    portal_id = scrapy.Field()


class AdEntity(db.Entity):
    portal_name = Required(str)
    updated_at = Required(datetime)
    address = Optional(str)
    zip_code = Optional(str)
    bedrooms = Required(str)
    parking_spaces = Optional(str)
    is_sold = Optional(bool)
    area = Optional(str)
    price_per_sqt_meters = Optional(str)
    bathrooms = Optional(str)
    total_price = Optional(str)
    type = Optional(str)
    release_year = Optional(str)
    url = Optional(str)
    lat = Optional(int)
    lng = Optional(int)
    portal_id = Required(str)
    PrimaryKey(portal_name, portal_id)
