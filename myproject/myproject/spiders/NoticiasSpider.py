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
        for child in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            url = child.text
            yield scrapy.Request(url, callback=self.parse_url_noticia)

    def parse_url_noticia(self, response):
        root = ET.fromstring(response.body)
        for child in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            url = child.text
            self.numPaginas += 1    
            if self.numPaginas <= 10000 :
                yield scrapy.Request(url, callback=self.parse_noticia)

    def parse_noticia(self, response):
        item = Noticia()
        item = Noticia()
        item['titulo'] = response.css('h1.title::text').get()  #tag h2 ou h3; classe title texto (inner text)
        item['descricao'] = response.css('h2.description::text').get()
        textos = response.css('section.content p span::text').extract()
        texto_completo = ''.join(textos)
        texto_sem_espacos = texto_completo.strip().rstrip('ASSINE')
        item['conteudo'] = texto_sem_espacos
        #item['conteudo'] = response.css('section.content').get()
        item['url'] = response.url    
        yield item

    def closed(self, reason):
        self.logger.info(f"Coletadas {self.numPaginas} páginas") 
       
