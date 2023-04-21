import scrapy
from myproject.items import Noticia


class NoticiasSpider(scrapy.Spider):
    name = "noticias"
    allowed_domains = ["quatrorodas.abril.com.br"]
    start_urls = ["https://quatrorodas.abril.com.br/noticias/"]

    def parse(self, response):
        for noticia in response.css('div.card'):
            item = Noticia()
            item['titulo'] = noticia.css('h2.title, h3.title::text').get()  #tag h2 ou h3; classe title texto (inner text)
            item['categoria'] = noticia.css('span.category::text').get()
            item['img_alternative'] = noticia.css('img::attr(alt)').get()
            item['image_link'] = noticia.css('img::attr(data-src)').get()
            item['link'] = noticia.css('a::attr(href)').get() #tag a; atribuot href
            item['descricao'] = noticia.css('p.description::text').get()
            yield item
        
        #Paginacao
        proxima_pagina = response.css('a.proxima::attr(href)').get()
        if proxima_pagina is not None:
            yield response.follow(proxima_pagina, callback = self.parse)
