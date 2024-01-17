import requests # http 요청을 커맨드라인으로 보낼 수 있게 해주는 라이브러리
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungle

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://shinsegaemall.ssg.com/best/bestShop.ssg?dispCtgId=6000039159', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

items = soup.select('#bestNewarrivalItem > li')

for idx, item in enumerate(items):
  imgs = item.select('div > div.mnsditem_goods > div.mnsditem_thmb > a > div > img.i2')
  titles = item.select('div > div.mnsditem_goods > div.mnsditem_detail > div.mnsditem_maininfo > a > div.mnsditem_tit > span.mnsditem_goods_tit')
  prices = item.select('div > div.mnsditem_goods > div.mnsditem_detail > div.mnsditem_maininfo > a > div.mnsditem_pricewrap > div.mnsditem_price_row.mnsditem_ty_newpr > div.new_price > em')
  discounts = item.select('div > div.mnsditem_goods > div.mnsditem_detail > div.mnsditem_maininfo > a > div.mnsditem_pricewrap > div.mnsditem_price_row.mnsditem_ty_newpr > div.discount_rate > span:nth-child(2)')

  if (len(imgs) == 0 or len(titles) == 0 or len(prices) == 0 or len(discounts) == 0):
    continue # 아래를 skip하고 다음 반복으로

  img = 'https:' + imgs[0].get('src')
  title = titles[0].text
  price = prices[0].text
  discount = discounts[0].text

  data = {'img': img, 'title': title, 'price': price, 'discount': discount}
  db.items.insert_one(data)




