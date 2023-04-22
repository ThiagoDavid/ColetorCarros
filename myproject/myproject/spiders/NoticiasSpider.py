# vou tentar atravez do sitemap do site extrair todas as notícias
import scrapy
from myproject.items import Noticia
import xml.etree.ElementTree as ET

class NoticiasSpider(scrapy.Spider):
    name = 'noticias'
    allowed_domains = ['quatrorodas.abril.com.br']
    start_urls = ['https://quatrorodas.abril.com.br/sitemap.xml']
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,        
        'ROBOTSTXT_OBEY': True
    }
    numPaginas = 0
    def parse(self, response):
        root = ET.fromstring(response.body)
        count = 0
        for child in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            if(count <= 2):
                url = child.text
                yield scrapy.Request(url, callback=self.parse_url_noticia)
                count+=1

    def parse_url_noticia(self, response):
        root = ET.fromstring(response.body)
        count=0
        for child in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            if(count<=1):
                url = child.text
                yield scrapy.Request(url, callback=self.parse_noticia)
                count+=1   

    def parse_noticia(self, response):
        item = Noticia()
        item['titulo'] = response.css('h1.title::text').get()  #tag h2 ou h3; classe title texto (inner text)
        item['descricao'] = response.css('h2.description::text').get()
        item['conteudo'] = response.css('section.content').get(),
        item['url'] = response.url
        self.numPaginas += 1        
        yield item

    def closed(self, reason):
        self.logger.info(f"Coletadas {self.numPaginas} páginas") 
       
