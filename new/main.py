from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from db import BigData

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(BigData)
    process.start()