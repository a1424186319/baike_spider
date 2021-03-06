from html_downloader import HtmlDowndloader
from url_manager import UrlManager
from html_outputer import Htmloutputer
from html_parser import HtmlParser
import time


# 项目入口
class SpiderMain():
    def __init__(self):
        self.urls = UrlManager()
        self.downloader = HtmlDowndloader()
        self.parser = HtmlParser()
        self.outputer = Htmloutputer()

    def craw(self, root_url, page_amount=5, time_sleep=None):
        count = 1
        # 添加第一个待爬取url
        self.urls.add_new_url(root_url)
        # 如果集合中有url,那么就取出一个url请求,没有连接则跳出.
        while self.urls.has_new_url():
            try:

                # 开始爬取
                # 取一个待爬取的url
                new_url = self.urls.get_new_url()
                print(f'craw {count}:{new_url}')
                # 请求url,返回html
                html_content = self.downloader.download(new_url)
                # xpath解析,得到需要的数据
                new_urls, new_data = self.parser.parse(html_content)
                # 一个词条页面上关联的a连接列表加入到url管理器中待爬取
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_url, new_data)

                count += 1
                if count > page_amount:
                    break

                time.sleep(2)
            except Exception as e:
                print(f'craw failed {new_url}')

        self.outputer.output_html()
        print('done')


if __name__ == '__main__':
    ROOT_URL = 'https://baike.baidu.com/item/Python/407313'
    # 第一个要爬取的页面
    PAGE_AMOUNT = 5  # 总共请求多少页
    TIME_SLEEP = 2  # 每次请求间隔秒数
    spider = SpiderMain()
    spider.craw(ROOT_URL, PAGE_AMOUNT, TIME_SLEEP)
