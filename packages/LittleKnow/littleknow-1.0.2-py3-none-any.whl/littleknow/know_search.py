#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/20 1:48
# @Author  : 沈复
# @File    : know_search.py
# @Software: PyCharm
# @desc:
# 默认接入百度
import datetime
import time
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from gne import GeneralNewsExtractor
import  requests
from retrying import retry
from playwright.sync_api import sync_playwright

class BaiduSearch():

    def __init__(self):
        self.gne=GeneralNewsExtractor()
        self.domain_list={
            "澎湃新闻": "www.thepaper.cn",
            "搜狐新闻": "www.sohu.com",
            "网易新闻": "news.163.com",
            "腾讯新闻": "news.qq.com",
            "百度新闻": "news.baidu.com",
            "百度百家号": "baijiahao.baidu.com",
            "政府新闻": "ciss.tsinghua.edu.cn",
        }
        self.time_days=90



    def gen_time_frame(self,days):
        # 获取当前日期和时间
        current_date = datetime.datetime.now()

        # 减去传入的天数得到未来日期
        future_date = current_date - datetime.timedelta(days=days)

        # 将未来日期转换为Unix时间戳
        future_timestamp = int(time.mktime(future_date.timetuple()))


        current_time_stamp=str(int(time.time()))
        return str(f"{future_timestamp},{current_time_stamp}")

    # 测试函数
    # print(get_future_timestamp(7))  # 输出将是当前时间后7天的Unix时间戳

    def gen_url(self,query,time_frame=90,si="*",pn=0):
        gpc_time=self.gen_time_frame(time_frame)
        # rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&
        params = {
            "rtt": 4,
            "bsst": 1,
            "cl": 2,
            "tn": "news",
            "ie": "utf-8",
            "medium":0,
            "wd": query,
            "pn": pn,
            "oq": query,
            "si": self.domain_list.get(si,""),
            "ct": "2097152",
            "gpc": f"stf={gpc_time}|stftype=1"
        }
        # url="https://www.baidu.com/s?wd=%E5%8D%97%E6%B5%B7%E8%A1%8C%E5%8A%A8&oq=%E5%8D%97%E6%B5%B7%E8%A1%8C%E5%8A%A8&si=news.qq.com&ct=2097152&gpc=stf%3D1716628538%2C1719306937%7Cstftype%3D1"
        result = urlencode(params)
        # print(result)
        url = "https://www.baidu.com/s?" + result
        return url

    def download(self, url):
        """
        url: 需要渲染的页面地址
        timeout: 超时时间
        proxy：代理
        wait：等待渲染时间
        images: 是否下载，默认1（下载）
        js_source: 渲染页面前执行的js代码
        :param url:
        :return:
        """
        from playwright.sync_api import sync_playwright


        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)  # 启动浏览器，headless=False表示非无头模式
            page = browser.new_page()  # 创建新页面

            try:
                # 导航到页面，并设置加载状态等待
                page.goto(url, wait_until="networkidle")

                # 等待页面加载完成，这里设置超时时间为30秒
                page.wait_for_load_state("load", timeout=30000)  # load 表示等待 DOMContentLoaded 事件

                # 页面加载完成后的操作
                content = page.content()

                return  content
            except page.TimeoutError:
                print("页面加载超时，返回空")  # 如果超时，打印提示信息
                return ""

            finally:
                browser.close()  # 关闭浏览器



    def parse_list(self, content):
        doc = BeautifulSoup(content, features="lxml")

        eles = doc.select(".news-title_1YtI1")

        seeds = []
        for ele in eles:
            url=ele.select_one("a").get("href")
            seeds.append({"url":url})
        # print(seeds)
        return  seeds


    def parse(self, content):
        # doc=BeautifulSoup(content,features="lxml")
        article = self.gne.extract(content)
        return article


    def search(self,query,time_frame=90,si="*",pn=0):
        url=self.gen_url(query,time_frame,si,pn)
        # print(url)
        # 检索以后 解析数据
        search_content = self.download(url)

        articles=[]
        search_list = self.parse_list(search_content)
        for page_seed in search_list:
            try:
                content = self.download_content(page_seed["url"])
                article = self.parse(content)
                result={"title":article["title"],"content":article["content"],"publish_time":article["publish_time"]}
                if result["title"]=="百度安全验证":
                    continue
                result["url"] = page_seed["url"]
                articles.append(result)
            except:
                pass

        return articles

    @retry(stop_max_attempt_number=4)
    def download_content(self, url):
        headers = {
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        }

        res = requests.get(url,headers=headers)
        return res.content.decode()


if __name__ == '__main__':

    bs=BaiduSearch()
    result = bs.search("汽车")
    print(result)