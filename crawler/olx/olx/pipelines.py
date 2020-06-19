import os

from pony.orm import db_session
from .settings import db

from .items import AdEntity


class PostgresPipeline(object):
    table_name = "olx"

    def __init__(self, host, db_user, db_password, db_port):
        self.db_host = host
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=os.environ.get("DB_HOST"),
            db_user=os.environ.get("DB_USER"),
            db_password=os.environ.get("DB_PWD"),
            db_port=os.environ.get("DB_PORT"),
        )

    def open_spider(self, spider):
        self.db = db
        self.db.bind(
            provider="postgres",
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database='olxcrawler'
        )
        self.db.generate_mapping(create_tables=True)

    def close_spider(self, spider):
        self.db.disconnect()

    @db_session
    def process_item(self, item, spider):
        ad_entity = AdEntity.select(
            lambda n: n.portal_id == item["portal_id"]
            and n.portal_name == item["portal_name"]
        ).count()

        if ad_entity > 0:
            ad_entity = AdEntity[item["portal_name"], item["portal_id"]]
            ad_entity.set(**item)
        else:
            AdEntity(**item)

        return item
