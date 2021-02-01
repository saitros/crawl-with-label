import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from urllib.request import urlopen

import re
import requests
import time

class Crwal_sample:
    def __init__(self):
        self.chrome_opt = webdriver.ChromeOptions()
        self.chrome_opt.add_argument('--headless')
        self.chrome_opt.add_argument('--no-sandbox')
        self.chrome_opt.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome('/home/ubuntu/IIPL/Crawl/chromedriver', chrome_options=chrome_opt)
        self.driver.get(url='https://news.naver.com/')
        
        self.cate_dict = {'정치':'//*[@id="lnb"]/ul/li[3]/a',  
                        '속보' :'//*[@id="lnb"]/ul/li[2]/a/span',
                        '경제':'//*[@id="lnb"]/ul/li[4]/a/span',
                        '사회':'//*[@id="lnb"]/ul/li[5]/a/span',
                        '생활/문화':'//*[@id="lnb"]/ul/li[6]/a/span'}
        
        self.selector_dict = {'헤드라인':'#main_content > div > div._persist > div > div > div.cluster_body > ul > li > div.cluster_text > a',
                             '속보':'#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt > a',
                             '일반':'#section_body > ul.type06_headline > li > dl > dt > a'}
        
        #section_body > ul.type06_headline > li > dl > dt > a
        
    def common_crawl_news_title(self, cate=None, keyword=0):
#         if cate is None:
#             html = self.driver.page_source
#             soup = BeautifulSoup(html, 'html.parser')
#             crawl_list = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt > a')
        title_list = []
        link_list = []
    
    
        if cate is '속보':
        
            self.driver.find_element_by_xpath(self.cate_dict[cate]).click()
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            crawl_list = soup.select(self.selector_dict['속보'])
        
        else:
            self.driver.find_element_by_xpath(self.cate_dict[cate]).click()
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            crawl_list = soup.select(self.selector_dict['헤드라인'])
            
#         print(crawl_list)
        for i in crawl_list:
            if len(i.text.strip()) != 0:
#                 news_link = re.match(r'href="([^*])"', str(i))
#                 print(news_link)
                news_link = re.findall('http[s]?://(?:[a-zA-z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),;]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                       str(i))[0].replace('amp;','')
                if keyword:
#                     print(1)
                    if keyword in i.text.strip():
                        title_list.append(i.text.strip())
                        link_list.append(news_link)
                        
                else:
                    title_list.append(i.text.strip())
                    link_list.append(news_link)
                    
        return title_list, link_list
                    
    def common_crawl_news_context(self, cate=None, keyword=0):
        #articleBodyContents > br:nth-child(3)
        title_list, link_list = self.common_crawl_news_title(cate, keyword)
        print(link_list)
        for link in link_list:
            print(link)
            try:
                html = requests.get(link, headers={'User-Agent':'Mozilla/5.0'})
#                 print(html.text)    
            except:
                time.sleep(1)
                pass
                
            
            soup = BeautifulSoup(html, 'html.parser')
            print(soup.select('articleBodyContents > br'))
            
if __name__ == "__main__":
    test = Crwal_sample()
    test.common_crawl_news_title('정치', '국회')
