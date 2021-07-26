import requests
from bs4 import BeautifulSoup, Comment

url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=100&oid=001&aid=0012439508'
r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')

title = soup.select_one('h3#articleTitle').text
content = soup.select_one('#articleBodyContents')
subtitle = content.select_one('strong')
if subtitle is not None: subtitle = subtitle.extract().text

for x in content.select('script'): x.extract()                             # <script>...</script> 제거
for x in content(text=lambda text: isinstance(text, Comment)): x.extract() # <!-- 주석 --> 제거
for x in content.select("br"): x.replace_with("\n")                        # <br>을 \n로 교체
content = "".join([str(x) for x in content.contents])                      # 최상위 태그 제거(=innerHtml 추출)
content = content.strip()                                                  # 앞뒤 공백 제거

print('title=', title)       # 제목
print('subtitle=', subtitle) # 부제
print('content=', content)   # 본문