import requests
from bs4 import BeautifulSoup


def get_html(url, header, kv):
    """获取url的html文本"""
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
            html_list.append(r.text)
    return html_list


def generate_list(html_texts):
    titles = []
    for html_text in html_texts:
        soup = BeautifulSoup(html_text, 'html.parser')
        titles.append(str(soup.a.string))
    return titles
        # for li in soup.



def main():
    header = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://book.douban.com/chart'
    kv = {'subcat':['all','literary','novel','history','social']}
    html_texts = get_html(url, header, kv)
    # for html_text in html_texts:
        # print(html_text[:-100])
    book_stitle_list = generate_list(html_texts)
    print(book_stitle_list)


if __name__ == '__main__':
    main()