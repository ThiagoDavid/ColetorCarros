# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Noticia(scrapy.Item):
    titulo = scrapy.Field()    
    descricao = scrapy.Field()
    conteudo = scrapy.Field()
    url = scrapy.Field()


