from bs4  import BeautifulSoup as bs
import requests

base_url = 'http://www.zsfdc.gov.cn'
index_url  = []
download_url = []
index_text = requests.get('http://www.zsfdc.gov.cn/ArticleList.aspx?id=32&c=100').text
soup = bs(index_text)

table = soup.find('table', class_='gridview')

rows = table.find_all('tr')

for row in rows:
	cols = row.find('a')
	index_url.append(base_url + '/' + cols.attrs['href'])

for url in index_url:
	content = requests.get(url).text
	soup = bs(content)
	download_url.append(
		base_url + soup.find(id='article-content').find('img').attrs['src'])
