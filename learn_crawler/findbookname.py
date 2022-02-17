import json
import requests
from bs4 import BeautifulSoup
import os

"""最关注的书籍保存到json文件中"""

def get_html(url, header, kv):
    """获取各类别url的html文本，存入列表"""
    request_list = kv['subcat']
    html_list = []
    for categray in request_list:
        kv['subcat']=categray
        try:
            r = requests.get(url, headers=header, params=kv)
            r.raise_for_status()
        except:
            print('encounter several problems!')
        else:
            r.encoding = r.apparent_encoding
            print(r.encoding)
            html_list.append(r.text.strip())
    return html_list


def generate_list(html_texts):
    """获取所有类别的最concern书籍名，返回一个存放列表的大列表"""
    all_books = {}
    for html_text in html_texts:
        books=[]
        soup = BeautifulSoup(html_text, 'html.parser')
        now_title = str(soup.find('span',class_='now').span.string)
        title_books = soup.find_all('h2',class_='clearfix')
        for each in title_books:
            # books.append(str(each.a.text.strip()))
            books.append(str(each.a.string))
        all_books[now_title] = books
    return all_books


def save_file(save_path, source):
    # try:
    #     if not os.path.exists(save_path):
    #         with open(save_path, 'w') as f:
    #             f.write(str(source))
    #             print('文件保存成功！')
    #     else:
    #         print('文件已存在')
    # except:
    #     print('保存失败！')
    '''
    json_str = json.dumps(source,indent=4)
    try:
        with open(save_path, 'w') as json_file:
            json_file.write(json_str)
            print('文件保存成功！')
    except:
        print('保存失败！')
    '''
    # json_str = json.dumps(source,indent=4)
    try:
        with open(save_path, 'w',encoding='utf-8') as f:
            json.dump(source,f)
            print('文件保存成功！')
    except:
        print('保存失败！')


def main():
    header = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://book.douban.com/chart'
    kv = {'subcat':['all','literary','novel','history','social','tech','art','drama','business','comics','suspense_novel','science_fiction']}
    #kv = {'subcat':'all'}
    html_texts = get_html(url, header, kv)
    #print(html_texts[0])
    # for html_text in html_texts:
        # print(html_text[:-100])
    # for books in generate_list(html_texts):
    #     print(books)
    booknames_dict = generate_list(html_texts)
    path = './concernig books.json'
    save_file(path, booknames_dict)
    print(booknames_dict)



if __name__ == '__main__':
    main()