import logging
import re
from datetime import datetime

import scrapy

from ..items import Ad


class OlxSpider(scrapy.Spider):
    name = "olx_spider"
    start_urls = []
    template_initial_url = (
        "https://pe.olx.com.br/grande-recife/recife/imoveis/aluguel/apartamentos?o={}"
    )
    olx_date_pattern = re.compile(r"\d{2}/\d{2}")
    portal_id_pattern = re.compile(r"\d*")
    logger = logging.getLogger(__name__)

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": "8",
        "CONCURRENT_REQUESTS": "16",
        "ITEM_PIPELINES": {"olx.pipelines.PostgresPipeline": 300},
    }

    def __init__(self):
        start_urls = [self.template_initial_url]
        pages = [str(x) for x in range(0,102)]
        for page in pages:
            start_urls.append(self.template_initial_url.format(page))

        super().__init__(name=self.name, start_urls=start_urls)

    def parse(self, response):
        ads_urls = response.xpath('//a[@data-lurker-detail="list_id"]/@href').getall()

        # those are the ads which are actual ones
        for ad_item in ads_urls:
            yield response.follow(ad_item, callback=self.parse_ad)

    def parse_ad(self, response):
        ad_item = Ad()

        ad_item["portal_name"] = "olx"
        ad_item["updated_at"] = datetime.now()
        ad_item["portal_id"] = response.css("span.sc-16iz3i7-0::text").getall()[1]

        details_div = response.css("div[data-testid=ad-properties]")
        details_fields = {
            "Quartos": "bedrooms",
            "Vagas na garagem": "parking_spaces",
            "Área útil": "area",
            "Banheiros": "bathrooms",
            "CEP": "zip_code",
            "Categoria": "type",
        }

        ad_item["total_price"] = response.css("div.sc-1wimjbb-2 > h2::text").get()
        ad_item["url"] = response.url

        for detail_field_div in details_div.css("div.sc-1ys3xot-0"):
            categoria = detail_field_div.css(".sc-1f2ug0x-0::text").get()
            if categoria in details_fields.keys():
                text = detail_field_div.css(".sc-1f2ug0x-0 ~ dd::text").get()

                if text is None:
                    text = detail_field_div.css(".sc-1f2ug0x-0 ~ a::text").get()

                ad_item[details_fields[categoria]] = text

        yield ad_item
