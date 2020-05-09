import requests
import urllib
import json
from fake_useragent import UserAgent


def getSougouImag(keywords, length, path, m):
    n = length
    urls = [] #用于保存链接
    imgs_url = []   #定义空列表，用于保存图片url
    # url = 'https://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?category='+cate + '&tag=%E5%85%A8%E9%83%A8&start=0&len='+str(n)
    for inx in range(n):
        url = "https://pic.sogou.com/pics?query={0}&mode=1&start={1}&reqType=ajax&reqFrom=result&tn=0".format(keywords, str(48*inx))
        # url = "https://pic.sogou.com/pics?query=%C8%FC%B3%B5%C5%DC%B5%C0&mode=1&start=" + str(48*inx) + "&reqType=ajax&reqFrom=result&tn=0"
        urls.append(url)

    for short_url in urls:
        headers = {'user-agent': UserAgent(verify_ssl=False).random}     # 设置UA
        f = requests.get(short_url, headers=headers)      # 发送Get请求
        js = json.loads(f.text)
        js = js['items']
        for j in js:
            imgs_url.append(j['thumbUrl'])
    for img_url in imgs_url:
        print('***** '+str(m)+'.jpg *****'+' Downloading...')
        urllib.request.urlretrieve(img_url, path+str(m)+'.jpg')    #下载指定url到本地
        m += 1
    print('Download complete!')


# 搜过的关键词：'竹林' '竹子' '竹子林' '大片竹子' '竹' '青竹' '青竹林' '竹叶' '龙鳞竹' '云南竹林' '贵州竹林' '竹手机壁纸'
# '竹壁纸' '竹摄影' '竹照片' '竹子手机壁纸' '竹子手机壁纸精美' '风景手机壁纸竹子' '旅行竹子' '竹海' '竹林景区'
# 蜀南竹海 '南山竹海' '中国大竹海' '重庆永川茶山竹海' '宜兴竹海'

# 雪山类：瑞士雪山、珠穆拉玛、张家口、俄罗斯雪山
# 玉龙雪山 雅拉雪山 南迦巴瓦峰
m = 2400 #表示图片开始保存的ID号
keywords = "%C4%CF%E5%C8%B0%CD%CD%DF%B7%E5"
getSougouImag(keywords, 50, r'F:/web_data/sougou2/', m)
