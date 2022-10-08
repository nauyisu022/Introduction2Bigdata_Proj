from scrapy import Selector, Request
import re
from new import *


class BigData(scrapy.Spider):
    name = 'bili'
    allowed_domains = ['www.bilibili.com']  # 网站
    start_urls = ['https://www.bilibili.com/v/popular/rank/all']

    def parse(self, responce):
        items = []
        sel = Selector(responce)
        list_item = sel.css('#app > div > div.rank-container > div.rank-list-wrap > ul')
        rootPath = '//*[@id="app"]/div/div[2]/div[2]/ul'
        for index in range(1,101):
            item = NewItem()
            detail_url = list_item.css(f'li:nth-child({index}) > div > div.info a::attr(href)').extract_first()
            detail_url="https:"+detail_url
            namePath = rootPath + '/li[{}]/div/div[2]/a/text()'.format(index)
            viewPath = rootPath + '/li[{}]/div/div[2]/div/div/span[1]/text()'.format(index)
            item['name'] =''.join(responce.xpath(namePath).extract()).replace('\n', '').replace(' ','')
            item['view'] =float(''.join(responce.xpath(viewPath).extract()).replace('\n', '').replace(' ','').replace("万",""))*10000
            items.append(item)
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': item},dont_filter=True)
        return items

    def parse_detail(self, responce, **kwargs):
        item = kwargs['item']
        item['list']=[]
        sel = Selector(responce)
        res=sel.css('span[class="info-text"]::text').extract()
        item['thumb'] = float(res[0].replace("万",""))*10000 if "万" in res[0] else float(res[0])
        item['coin'] = float(res[1].replace("万",""))*10000 if "万" in res[0] else float(res[1])
        item['favor'] = float(res[2].replace("万",""))*10000 if "万" in res[0] else float(res[2])
        item['forward']=float(res[3].replace("万",""))*10000 if "万" in res[0] else float(res[3])
        lis=responce.xpath('//*[@id="v_tag"]/div/ul/li')[1:]
        for i in lis:
            topic=i.xpath('div/a/text()').extract()
            if len(topic)==0:
                topic = i.xpath('a/text()').extract()
                if len(topic)==0:
                    continue
                else:
                    topic = topic[0].replace('\n', '').replace(' ', '')
            else:
                topic=topic[0].replace('\n','').replace(' ','')
            item['list'].append(topic)
        yield item