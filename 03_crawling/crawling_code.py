import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import urllib.request

def extract_title(item):
    try:
        title = item.find('a', {'class': 'nclicks(fls.list)'}).find('img')['alt']
        print('[기사 제목]')
        print(title)
    except:
        title = 'No Title'
        print('No Title')
    return title

def extract_link(item):
    write = item.find('a')['href']
    print('[기사 링크]')
    print(write)
    return write

def extract_content(content_url):
    try:
        r = requests.get(content_url, headers={'User-Agent': 'Mozilla/5.0'})  # write는 url
        soup = BeautifulSoup(r.text, 'html.parser')

        content = soup.select_one('#articleBodyContents')

        for x in content.select("span"): x.extract()
        for x in content.select("strong"): x.extract()
        for x in content.select('script'): x.extract()  # <script>...</script> 제거
        for x in content(text=lambda text: isinstance(text, Comment)): x.extract()  # <!-- 주석 --> 제거
        for x in content.select("br"): x.replace_with("\n")  # <br>을 \n로 교체
        content = "".join([str(x) for x in content.contents])  # 최상위 태그 제거(=innerHtml 추출)
        content = content.strip()  # 앞뒤 공백 제거
        # content = item.find('span', {'class': 'lede'}).text
        print(['기사 본문'])
        print(content)
    except:
        content = 'No content'
        print('No Contents')
    return content

def page_get():
    x, y = map(str, input('가져올 뉴스의 시작 날짜와 종료 날짜를 입력하세요.(예 : 19980501 20200131) :').split())
    a, b = map(int, input('시작 페이지와 종료 페이지를 입력하세요.(예 : 1 15) :').split())
    print('\n' * 2)

    df = pd.DataFrame(columns=['title', 'content', 'url'])
    df_title = []
    df_content = []
    df_link = []

    for date in (pd.date_range(start=x, end=y).strftime("%Y%m%d").to_list()):
        for num in range(a, b + 1):
            # 속보 url
            url = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001&date=%s&page=%d' % (date, num)
            headers = {'User-Agent': 'Mozilla/5.0'}
            html = requests.get(url, headers=headers)
            # soup = BeautifulSoup(html.text)
            soup = BeautifulSoup(html.text,'html.parser')
            headline = soup.find_all('dl')

            for item in headline:
                # title 추출
                title = extract_title(item)
                df_title.append(title)

                # url 추출
                write = extract_link(item)
                df_link.append(write)

                # 본문 내용 추출
                content = extract_content(write)
                df_content.append(content)
                print('-' * 30)

    df['title'] = df_title
    df['content'] = df_content
    df['url'] = df_link

    df.drop_duplicates()
    df.to_csv('data/naver_news_multi_real.csv', encoding='utf-8-sig', index=False)

if __name__ == "__main__":
    print("크롤링 시작")
    page_get()
    print("크롤링 완료")
