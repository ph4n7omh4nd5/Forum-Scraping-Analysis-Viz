import scrapy
from  ..items import PostcrawlerItem
from pprint import pprint

class ForumSpiderSpider(scrapy.Spider):
    name = 'forum_spider'
    start_urls = ['https://forums.lotro.com/forums/showthread.php?695979-Minstrel-Changes-and-Feedback']
    page_number = 2

    def parse(self, response):
        items = PostcrawlerItem()
        blocks = response.css('li.postcontainer')
        for info in blocks:
            # print(info)
            author = info.css('div.username_container img.onlinestatus::attr(alt)').extract_first()
            # pprint(author[0:author.index(' ')])
            items['author'] = author[0:author.index(' ')]
            post = info.css('div blockquote.restore::text').extract()
            # # print(authors)
            # #
            # for line in post:
            #     line.replace('\r', '')
            #     line.replace('\t', '')
            #     line.replace('\n', '')
            #     pprint(line)
            items['post'] = post
            date = info.css('div.posthead span.date::text').extract_first()
            items['date'] = date
            yield items

        next_page = 'https://forums.lotro.com/forums/showthread.php?695979-Minstrel-Changes-and-Feedback/page' + str(ForumSpiderSpider.page_number)
        if ForumSpiderSpider.page_number <= 8:
            yield response.follow(next_page, callback=self.parse)
            ForumSpiderSpider.page_number += 1
