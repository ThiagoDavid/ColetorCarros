# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

class SaveToFilePipeline:
    def __init__(self):
        self.filename = 'noticias.txt'

    def open_spider(self, spider):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.file = open(self.filename, 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write(f"{item['titulo']} | {item['descricao']} | {item['conteudo']} | {item['url']}\n")
        return item