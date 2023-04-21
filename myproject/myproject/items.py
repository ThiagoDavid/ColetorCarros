# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Noticia(scrapy.Item):
    titulo = scrapy.Field()
    categoria = scrapy.Field()
    img_alternative = scrapy.Field()
    image_link = scrapy.Field()
    link = scrapy.Field()
    descricao = scrapy.Field()


