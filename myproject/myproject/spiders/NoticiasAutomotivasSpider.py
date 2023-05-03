# vou tentar atravez do sitemap do site extrair todas as notícias
import scrapy
from myproject.items import Noticia
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

class NoticiasAutomotivasSpider(scrapy.Spider):
    name = 'noticias_automotivas'
    allowed_domains = ['noticiasautomotivas.com.br']
    start_urls = ['https://www.noticiasautomotivas.com.br/sitemap-posttype-post.xml']
    custom_settings = {
        'DOWNLOAD_DELAY': 0.2
    }
    numPaginas = 0
    def parse(self, response):
        urls_noticias = response.css('a::attr(href)').getall()
        for url in urls_noticias:
            yield scrapy.Request(url, callback=self.parse_noticia)

    def parse_noticia(self, response):
        print(f"TFL - Callback - {response.url}")
        item = Noticia()
        item['titulo'] = response.css('h1.entry-title::text').get().replace('\n', '').strip()  #tag h2 ou h3; classe title texto (inner text)
        item['descricao'] = "-"
        textos = response.css('div.entry-content descendant-or-self::text').getall()
        texto_completo = ''.join(textos)
        texto_sem_espacos = texto_completo.strip().rstrip('ASSINE')
        item['conteudo'] = texto_sem_espacos.replace('\n', '').strip()
        #item['conteudo'] = response.css('section.content').get()
        item['url'] = urlparse(response.url).geturl()
        self.numPaginas += 1   
        yield item

    def closed(self, reason):
        self.logger.info(f"Coletadas {self.numPaginas} páginas") 
       
