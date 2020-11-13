import requests
from 网络爬虫.lxml import etree
import urllib

"""
爬取京东科颜氏产品信息
"""

#url探索
url = 'https://search.jd.com/Search?keyword=%E7%A7%91%E9%A2%9C%E6%B0%8F&enc=utf-8&wq=%E7%A7%91%E9%A2%9C%E6%B0%8F&pvid=60b0f2611eec4352bf314be60c6d1aae' #第一页
url_1 = 'https://search.jd.com/Search?keyword=%E7%A7%91%E9%A2%9C%E6%B0%8F&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E7%A7%91%E9%A2%9C%E6%B0%8F&ev=exbrand_%E7%A7%91%E9%A2%9C%E6%B0%8F%EF%BC%88Kiehl%27s%EF%BC%89%5E&stock=1&page=3&s=61&click=0' #第二页
url_2 = 'https://search.jd.com/Search?keyword=%E7%A7%91%E9%A2%9C%E6%B0%8F&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E7%A7%91%E9%A2%9C%E6%B0%8F&ev=exbrand_%E7%A7%91%E9%A2%9C%E6%B0%8F%EF%BC%88Kiehl%27s%EF%BC%89%5E&stock=1&page=5&s=121&click=0' #第3页
url_3 = 'https://search.jd.com/Search?keyword=%E7%A7%91%E9%A2%9C%E6%B0%8F&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E7%A7%91%E9%A2%9C%E6%B0%8F&ev=exbrand_%E7%A7%91%E9%A2%9C%E6%B0%8F%EF%BC%88Kiehl%27s%EF%BC%89%5E&stock=1&page=7&s=181&click=0' #第4页
urllib.parse.unquote('%E7%A7%91%E9%A2%9C%E6%B0%8F') #解码

url_0 = 'https://search.jd.com/Search?keyword=%E7%A7%91%E9%A2%9C%E6%B0%8F&page=7&s=181'

#请求
headers = {'Cookie': '__jdu=819895583; shshshfpa=fbf477ff-00ab-e486-eeae-1eb749476c75-1586325602; shshshfpb=aPOyqgEjrz6UWhFNKubl7ng%3D%3D; xtest=7928.cf6b6759; areaId=19; ipLoc-djd=19-0-0-0; unpl=V2_ZzNtbUcFQBF0D0JSLEoOB2JRR18SBENCdgoTVnNODA0yAEVVclRCFnQUR1FnGl0UZAMZX0RcRxxFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHIZVAxvBxZUQGdzEkU4dlR8H1sDYzMTbUNnAUEpDEZRfRpVSG4DGlRKU0ccdzhHZHg%3d; PCSYCityID=CN_440000_0_0; __jdv=209449046|baidu|-|organic|not set|1587389898687; RT="z=1&dm=jd.com&si=tdcvqtw9pip&ss=k98iyj1f&sl=3&tt=4ir&nu=3d2f85352c70c73af100bf1449967844&cl=17d&ld=9c5&ul=spr&hd=sq2"; __jda=122270672.819895583.1582624073.1587389899.1587627126.15; __jdc=122270672; shshshfp=7012e875a8a0a48f77c25cbb2f47535e; rkv=V0600; qrsc=3; wlfstk_smdl=a2ot19inzlz0ax679u586d9p271pzcda; TrackID=1AOIZLLQ8GlF5HC5V0H9auParl00-w8k41VLB9J5X0EeIhrYrubk3kXpk_6EV7vcZ0LON9ERM_r72UgsiK2EDTnA4EN7fa4Fb4UNuyQkf4-8; thor=848AD158122F10D1F460D6689A4A8A95B4E489891CB4CDF98464EEBAE364C6BC8CBBE467428C7BFD35704E207FDE9B8F7C24DC6E8B4E9D59CCD82CD5A2506105616A16DFC049AF15B6BE61E628536D92319D98A9FA4008693EA750E3DB1B9D87426971C1698CDD44B20483B1E125BCA1BECF3DBAA735973A9A69ED3EAF61163E40368D7D22D4D00EDAD781848DB1905D; pinId=pUYHaABGpJ6j_-6sMeIy8A; pin=aifan%E8%89%BE%E9%A5%AD; unick=aifan%E8%89%BE%E9%A5%AD; ceshi3.com=201; _tp=Iy9P%2BwUhLRjzwXB5E8B2oAWzaaFGz7gF63UINuPJGKQ%3D; _pst=aifan%E8%89%BE%E9%A5%AD; __jdb=122270672.4.819895583|15.1587627126; shshshsID=cfdddba376eb5baf8d9d7f2fc2a12947_2_1587627195514; 3AB9D23F7A4B3C9B=3WHLFDCFRMKXTCGZXMAJEQORVCXPD4XDQID2MCQGM4HNQST5FPREJG4F2UMQOAVO47FSGN7WNHUKTLYQBO5EJ7K4EE',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
         'Referer': 'https://search.jd.com/Search?keyword=%E7%A7%91%E9%A2%9C%E6%B0%8F&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E7%A7%91%E9%A2%9C%E6%B0%8F&ev=exbrand_%E7%A7%91%E9%A2%9C%E6%B0%8F%EF%BC%88Kiehl%27s%EF%BC%89%5E&stock=1&page=1&s=1&click=0'}
rs = requests.get('https://search.jd.com/Search?keyword=%E7%A7%91%E9%A2%9C%E6%B0%8F&page=7&s=181', headers = headers)

url = 'https://search.jd.com/Search?keyword=%E7%A7%91%E9%A2%9C%E6%B0%8F&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E7%A7%91%E9%A2%9C%E6%B0%8F&ev=exbrand_%E7%A7%91%E9%A2%9C%E6%B0%8F%EF%BC%88Kiehl%27s%EF%BC%89%5E&stock=1&page=1&s=1&click=0'
rs = requests.get(url, headers = headers)
rs.encoding = 'utf-8'
rs.content
rs.json()

html = etree.HTML(rs.text)
result = etree.tostring(html)
result.decode('utf-8')
html.xpath('//div[@class="ml-wrap"]/div[@id="J_goodsList"]/ul/li/text()')
html.xpath('//li')

"""
爬取新浪新闻呢
"""
import requests
from 网络爬虫.lxml import etree
from bs4 import BeautifulSoup

url = 'https://news.sina.com.cn/'
res = requests.get(url)

soup = BeautifulSoup(res.content)
html = etree.HTML(res.content)

from sklearn.metrics.pairwise import cosine_similarity
cosine_similarity([1, 0, 0, 0], [1, 0, 0, 0])
