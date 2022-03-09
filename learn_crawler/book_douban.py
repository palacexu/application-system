# -*- coding: utf-8 -*-
import requests 
from lxml import etree
import pandas as pd
import re

def get_data(html):
    xp = etree.HTML(html)
    print("1---------"*3,type(xp),xp)  # <class 'lxml.etree._Element'>
    result = etree.tostring(xp,encoding='utf-8')
    result = result.decode('utf-8')
    print("2---------"*3,type(result))   # str类型
    lis = xp.xpath('//*[@id="content"]/div/div[1]/div/table')
    
    # print(xp.xpath('//*[@id="content"]/div/div[1]/div/table/tr/td[2]/div[1]/a/@title')) ## 为空
    print("lis:",type(lis),lis)
    for li in lis:
        """'图书名称','作者','作者国籍?','出版社','出版时间','价格','评价分数','评价人数','导语'"""
        titles = li.xpath('./tr/td[2]/div[1]/a/@title')[0]
        links = li.xpath('./tr/td[2]/div[1]/a/@href')[0]
        img_url = li.xpath('./tr/td[1]/a/img/@src')[0]
        # print("titles:",type(titles),titles)  #<class 'list'>,[0]即取出字符串
        infos = li.xpath('./tr/td[2]/p[1]/text()')[0].split('/')
        # print("infos:",type(infos),infos)
        if len(infos) == 4:
            country = '中国'
            translator = None
            authors,presses,presstime,price = infos[0].strip(),infos[1].strip(),infos[2].strip(),infos[3].strip()[:-1]
            #print("unzip:",titles,authors,country,translator,presses,presstime,price)
        elif len(infos)==5:
            if infos[0].strip()=="J.K.罗琳 (J.K.Rowling)":
                country = '英'
                authors = infos[0].strip()[:infos[0].strip().find('(')-1]
            else:
                match_country = re.search(r'\[.+\]|\（.+\）',infos[0].strip())
                if match_country == None:
                    country = None
                    authors = infos[0].strip()
                else:
                    country = match_country.group(0)
                    country = country[1:len(country)-1]
                    match_authors = re.search(r'\].+|\）.+',infos[0].strip())
                    authors = match_authors.group(0)[1:len(match_authors.group(0))]
                    #print (f"{match_authors}———————{infos[0].strip()}____{match_authors.group(0)}****{authors}")
            translator,presses,presstime,price = infos[1].strip(),infos[2].strip(),infos[3].strip(),infos[4].strip()[:-1]
            #print("unzip:","----"*10,titles,authors,country,translator,presses,presstime,price)
        else:
            authors = None
            country = '中国'
            translator = None
            presses,presstime,price = infos[0].strip(),infos[1].strip(),infos[2].strip()[:-1]
        print("unzip:","----"*10,titles,authors,country,translator,presses,presstime,price,links,img_url)

        #scores = li.xpath('tbody/tr/td[2]/div[2]/span[2]/text()')
        #pollnumbers = li.xpath('tbody/tr/td[2]/div[2]/span[3]/text()')
        #intros = li.xpath('tbody/tr/td[2]/p[2]/span/text()')

        # 25个
        scores = li.xpath('.//div[@class="star clearfix"]/span[2]/text()')[0]
        print("debug:","__"*11,type(scores),scores)
        pollnumbers = li.xpath('.//div[@class="star clearfix"]/span[3]/text()')[0]
        match_pollnumbers = re.search(r'\d+',pollnumbers)
        pollnumbers = match_pollnumbers.group(0)
        intros = li.xpath('.//p[@class="quote"]/span/text()')
        if len(intros) == 0:
            intros = None
        else:
            intros = intros[0]
        df.append([titles,authors,country,translator,presses,presstime,price,scores,pollnumbers,intros,links,img_url])
        d = pd.DataFrame(df,columns=columns)
        d.to_excel('douban_book-250.xlsx',index=False)


def main():
    global df,columns,charset
    df = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Referer': 'https://book.douban.com/top250'}
    columns = ['图书名称','作者','国家','译者','出版社','出版时间','价格','评价分数','评价人数','导语','图书链接','书籍图片链接']
    for i in range(0,10):
        url = "https://book.douban.com/top250?start={}".format(str(i*25))
        try:
            print(url)
            res = requests.get(url,headers=headers)
            res.encoding = res.apparent_encoding
            charset = res.encoding
            res.raise_for_status()
        except:
            print("enounter an error")
        else:
            html = res.text
            get_data(html)


if __name__ =="__main__":
    main()

"""
(
                    362673人评价
                )
"""