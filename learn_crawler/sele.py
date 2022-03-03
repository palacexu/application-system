from selenium.webdriver import Chrome, ChromeOptions
import time
import re

comp = re.compile(r'\（.*?\）')
url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2021-0-1-"
option = ChromeOptions()
option.add_argument("--headless")
option.add_argument("--no-sandbox")
browser = Chrome(options=option, executable_path=r'D:\DesktopFile\code\test\chromedriver')
list=[]
for i in range(1,2):
    browser.get(url+str(i))
    links = browser.find_elements_by_xpath('/html/body/div[3]/div[3]/div[2]/ul/li/div[3]/a')
    # print(links)
    for link in links:
        # link = link.text
        # link = link.replace("（", "{")
        # link = link.replace("）", "}")
        name = comp.sub('',link.text)
        print(name)
        list.append(name)
    print("---"*10)
    time.sleep(2)
print(list)