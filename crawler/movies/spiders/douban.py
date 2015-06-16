# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from movies.items import MovieItem
import re
# HEADERS = {
#     "Host": "movie.douban.com",
# "Connection": "keep-alive",
# "Cache-Control": "max-age=0",
# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
# "X-FirePHP-Version": "0.0.6",
# "Referer": "http://www.douban.com/search?source=suggest&q=%E7%9C%9F%E6%8E%A2",
# "Accept-Encoding":"gzip, deflate, sdch",
# "Accept-Language":"zh-CN,zh;q=0.8",
# "Cookie":'bid="aLN/Y+kI25E"; ll="118172"; ue="modongming91@126.com"; viewed="6845414_3930318_6959482"; ct=y; dbcl2=""44748146:"BYuRk+lR8vE"; ck="Pi4Y"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1434095444%2C%22http%3A%2F%2Fwww.douban.com%2Fsearch%3Fcat%3D1002%26q%3D%25E7%259C%259F%25E6%258E%25A2%22%5D; __utma=223695111.1040102943.1430726837.1434093610.1434095444.14; __utmc=223695111; __utmz=223695111.1434095444.14.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; _pk_id.100001.4cf6=bfebd73476e6546e.1430726838.14.1434096249.1434093610.; ap=1; push_noty_num=3; push_doumail_num=8; __utma=30149280.67824527.1420785980.1434095434.1434097788.42; __utmb=30149280.2.10.1434097788; __utmc=30149280; __utmz=30149280.1434097788.42.30.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=scrapy%20redis%20mongo; __utmv=30149280.4474'
# }
TV_RUNTIME_RE = re.compile(ur'单集片长: (\d+)')
LANGUAGES_RE = re.compile(ur"语言:</span> (.+?)<br>")
COUNTRIES_RE = re.compile(ur"制片国家/地区:</span> (.+?)<br>")
ALIAS_RE = re.compile(ur"又名:</span> (.+?)<br>")
IMDB_RE = re.compile(ur"http:\/\/www\.imdb\.com\/title\/\w+")
# SCREENWRITER_RE = re.compile(ur"编剧:</span> (.+?)<br>")
NUM_RE = re.compile(r"(\d+)")
NEXT_PAGE_RE=re.compile(r'\?start=\d+')
class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ['http://movie.douban.com/tag/']
    rules = (
        # Rule(LinkExtractor(allow=r"/subject/\d+/\S*"),
        #     callback="parse_item", follow=True),
        # Rule(LinkExtractor(allow=r"/tag/\S+/\?focus=movie"),
        #     callback="parse_list", follow=True),
        # Rule(LinkExtractor(allow=r"/tag/$"),
        #     callback="parse_type_list", follow=True)
        Rule(LinkExtractor(allow=r"/subject/\d+/($|\?\w+)"),
            callback="parse_item", follow=True),
    )
    # def __init__(self):
    #     self.headers =HEADERS
    #     self.cookies ={}

    # def start_requests(self):
    #     for i, url in enumerate(self.start_urls):
    #         yield FormRequest(url, meta = {'cookiejar': i}, \
    #                           headers = self.headers, \
    #                           cookies =self.cookies,callback=self.parse_type_list)

    def parse(self, response):
        yield Request(response.url,callback=self.parse_type_list)
        pass
    def parse_type_list(self,response):
        #$x('//*[@class="tagCol"]/tbody/tr/td/a/text()')
        for tag in response.xpath('//*[@class="tagCol"]/tbody/tr/td/a/text()').extract():
            log.msg('tag : '+tag)
            # yield Request('http://www.douban.com/link2/?url=http://www.douban.com/tag/'+tag.encode('utf8')+'/movie&type=tag_more&name='+tag.encode('utf8')+'&focus=&mod=movie',callback=self.parse_list)
            yield Request('http://movie.douban.com/tag/'+tag.encode('utf8'),callback=self.parse_list)
        pass
    def parse_list(self,response):
        #log.msg('crawle list : '+response.url)
        for link in response.xpath(('//*[@class="article"]/div/dl/dd/a/@href')).extract():
            yield Request(link,callback=self.parse_item)
        next = response.xpath('//link[@rel="next"]/@href').extract()
        #if next:yield Request(NEXT_PAGE_RE.sub(next,response.url),callback=self.parse_list)
        if next:yield Request(next[0],callback=self.parse_list)
        pass
    def parse_item(self,response):
        log.msg('crawle item : '+response.url)
        item = MovieItem()
        item['title']=response.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=self.get_year(response)
        item['type'] = self.get_type(response)
        item['genres'] = self.get_genres(response)
        item['areas'] = self.get_areas(response)
        item['author'] =""
        item['languages'] = self.get_languages(response)
        item['pubTime'] = self.get_pubTime(response)
        item['enName'] = ""
        item['alias'] =self.get_alias(response)
        item['screenwriters'] = self.get_screenwriters(response)
        item['directors']=self.get_directors(response)
        item['actors'] = self.get_actors(response)
        item['imdbId'] = self.get_imdbId(response)
        item['imdbScore'] = 0
        item['intoduction'] = self.get_introduction(response)
        item['runtime'] = self.get_runtime(response,item['type'])
        item['poster'] = ""
        item['site']="douban"
        item['siteId'] = self.getSiteId(response)
        item['siteScore'] = self.get_score(response)
        item['siteVoteCount'] =self.get_vote(response)
        item['siteStars'] = self.get_stars(response,item['siteVoteCount'])
        log.msg(item)
        yield  item
        pass
    def getSiteId(self,response):
        return response.url.split('/')[-2]
    def get_imdbId(self,response):
        S = "".join(response.xpath("//div[@id='info']").extract())
        M = IMDB_RE.search(S)
        return M.group(0)[26:] if M is not None else ""
    def get_screenwriters(self,response):
        screenwriters = response.xpath('//*[@id="info"]/span[2]/span[2]/a[1]/text()').extract
        return  screenwriters if screenwriters else []
    def get_alias(self,response):
        S = "".join(response.xpath("//div[@id='info']").extract())
        M = ALIAS_RE.search(S)
        return [ alias.strip() for alias in M.group(1).split("/") ] if M is not None else []
    def get_stars(self, response,vote):
        xpath = response.xpath("//div[@class='rating_wrap clearbox']/text()").extract()
        stars = "".join( map(unicode.strip, xpath ) ).split("%")[:-1]
        stars = [ int( round((float( "%.3f" % (float(star)/100))) * vote) )  for star in stars ]
        # item["stars"] = stars
        return stars
    def get_name(self, response):
        name = response.xpath("//title/text()").extract()
        # if name: item["name"] = name[0].replace(u" (豆瓣)", "").strip()
        return name[0].replace(u" (豆瓣)", "").strip() if name else ""
    def get_year(self, response):
        year = response.xpath("//span[@class='year']").re(NUM_RE)
        # if year: item["year"] = int( year[0] )
        return int( year[0] ) if year else 0
    def get_directors(self, response):
        directors = response.xpath("//a[@rel='v:directedBy']/text()").extract()
        # if directors: item["directors"] = directors
        return directors if directors else []
    def get_actors(self, response):
         actors = response.xpath("//a[@rel='v:starring']/text()").extract()
         # if actors: item["actors"] = actors
         return actors if actors else []
    def get_genres(self, response):
        genres = response.xpath("//span[@property='v:genre']/text()").extract()
        # if genres: item["type"] = genres
        return genres if genres else []
    def get_type(self,response):
        S = "".join( response.xpath("//div[@id='info']//text()").extract() )
        M = TV_RUNTIME_RE.search(S)
        if M is not None:
            return "tv"
        else:
            return "movie"

    def get_runtime(self, response,type):
        if type =='tv':
            S = "".join( response.xpath("//div[@id='info']//text()").extract() )
            M = TV_RUNTIME_RE.search(S)
            return int(M.group(1))
        elif type == 'movie':
            runtime = response.xpath("//span[@property='v:runtime']/text()").re(NUM_RE)
            return int( runtime[0] ) if runtime else 0
    def get_score(self, response):
        average = response.xpath("//strong[@property='v:average']/text()").extract()
        # if average and average[0] != "": item["average"] = float( average[0] ) + 0.0
        return float( average[0] ) + 0.0 if average and average[0] != "" else 0
    def get_vote(self, response):#投票人数
         votes = response.xpath("//span[@property='v:votes']/text()").extract()
         # if votes and votes[0] != "": item["vote"] = int( votes[0] )
         return int( votes[0] ) if votes and votes[0] != "" else 0
    def get_tags(self, response):
        T = []
        tags = response.xpath("//div[@class='tags-body']/a")
        for tag in tags:
            t = tag.xpath("text()").extract()
            if t: T.append(t[0])
        # if T: item["tags"] = T
        return T
    # def get_watched(self, response):
    #     spec = "//div[@class='subject-others-interests-ft']/a[re:test(@href, 'collections$')]/text()"
    #     collections = response.xpath(spec).re(NUM_RE)
    #     if collections: item["watched"] = int( collections[0] )
    #
    # def get_wish(self, response):
    #     spec = "//div[@class='subject-others-interests-ft']/a[re:test(@href, 'wishes$')]/text()"
    #     wishes = response.xpath(spec).re(NUM_RE)
    #     if wishes: item["wish"] = int( wishes[0] )

    def get_languages(self, response):
        S = "".join(response.xpath("//div[@id='info']").extract() )
        M = LANGUAGES_RE.search(S)
        # if M is not None:
        #     item["languages"] = [ lang.strip() for lang in M.group(1).split("/") ]
        return [ lang.strip() for lang in M.group(1).split("/") ] if M is not None else []

    def get_areas(self, response):
        S = "".join(response.xpath("//div[@id='info']").extract() )
        M = COUNTRIES_RE.search(S)
        # if M is not None:
        #     item["areas"] = [ country.strip() for country in M.group(1).split("/") ]
        return [ country.strip() for country in M.group(1).split("/") ] if M is not None else []

    def get_introduction(self, response):
        summary = response.xpath("//span[@property='v:summary']/text()").extract()
        # if summary: item["introduction"] = "<br/>".join( summary )
        return "<br/>".join( summary ) if summary else ""
    def get_image(self, response):
        image = response.xpath("//a[re:test(@href, 'all_photos$')]/text()").re(NUM_RE)
        # if image: item["image"] = int( image[0] )
        return int( image[0] ) if image else 0
    def get_comment(self, response):
        comment = response.xpath("//a[re:test(@href, '/comments$')]/text()").re(NUM_RE)
        # if comment: item["comment"] = int( comment[0] )
        return int( comment[0] ) if comment else 0
    def get_question(self, response):
        question = response.xpath("//a[re:test(@href, '/questions/\?from=subject$')]/text()").re(NUM_RE)
        # if question: item["question"] = int( question[0] )
        return int( question[0] ) if question else 0

    def get_review(self, response):
        review = response.xpath("//a[re:test(@href, '/reviews$')]/text()").re(NUM_RE)
        # if review: item["review"] = int( review[0] )
        return int( review[0] ) if review else 0

    def get_discussion(self, response):
         discussion =  response.xpath("//a[re:test(@href, 'discussion/')]/text()").re(NUM_RE)
         # if discussion: item["discussion"] = int( discussion[0] )
         return int( discussion[0] ) if discussion else 0

    def get_pubTime(self,response):
        pubTime = response.xpath('//span[@property="v:initialReleaseDate"]/text()').extract()
        # if pubTime:item['pubTime']=pubTime
        return pubTime if pubTime else ""
