import requests
from bs4 import BeautifulSoup


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
            html_list.append(r.text.strip())
    return html_list


def generate_list(html_texts):
    """获取所有类别的最concern书籍名，返回一个存放列表的大列表"""
    all_books = []
    for html_text in html_texts:
        books=[]
        soup = BeautifulSoup(html_text, 'html.parser')
        # now_title = soup.find('span',class_='now').span.string
        title_books = soup.find_all('h2',class_='clearfix')
        for each in title_books:
            # books.append(str(each.a.text.strip()))
            books.append(str(each.a.string))
        all_books.append(books)
    return all_books


def main():
    header = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://book.douban.com/chart'
    # varieties = ['全部','文学','小说',]
    kv = {'subcat':['all','literary','novel','history','social','tech','art','drama','business','comics','suspense_novel','science_fiction']}
    html_texts = get_html(url, header, kv)
    #print(html_texts[0])
    # for html_text in html_texts:
        # print(html_text[:-100])
    for books in generate_list(html_texts):
        print(books)


if __name__ == '__main__':
    main()