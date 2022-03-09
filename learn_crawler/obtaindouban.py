#-*- coding:utf-8 -*-
from selenium.webdriver import Chrome, ChromeOptions

import json 
import os

def obtainbooks():
    with open(r"D:\code\data_manager\learn_crawler\urls copy.json",'r', encoding='UTF-8') as f:
        load_dict = json.load(f)
    print(load_dict)
    option = ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--no-sandbox")

    browser = Chrome(options=option, executable_path=r'D:\DesktopFile\code\test\chromedriver')
    category={}
    
    for (title,url) in load_dict.items():
        browser.get(url)
        booknames = browser.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[2]/h3')
        details = browser.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div/div[2]/div[1]')
        # 逻辑不对
        s = [[bookname.text,detail.text] for bookname in booknames for detail in details]
        dict_s = dict(s)
        category[title]= dict_s
    print(category)

def save_file(save_path, source):
    try:
        with open(save_path, 'w',encoding='utf-8') as f:
            json.dump(source,f,ensure_ascii=False)
            print('文件保存成功！')
    except:
        print('保存失败！')


if __name__ =='__main__':
    category = obtainbooks()
    save_file('learn_crawler/details.json',category)
    