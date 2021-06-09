import requests
from scrapy import Selector

from lxml import etree
import re

from fontTools.ttLib import TTFont

def start_request():
    item = {}
    url = "https://club.autohome.com.cn/frontapi/data/page/club_get_topics_list?page_num=2&page_size=50&club_bbs_type=c&club_bbs_id=18&club_order_type=1"
    response = requests.get(url)
    data = response.json().get("result", {}).get("items", [])
    i = data[0]
    # for i in data:
    item["title"] = i.get("title", "")
    item["summary"] = i.get("summary", "")
    item["get_date"] = i.get("publish_time", "")
    item["url"] = i.get("pc_url", "")
    print(item)


def parse(url="https://club.autohome.com.cn/bbs/thread/ac957fc71c01ee7c/96779411-1.html"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    # 匹配ttf font
    cmp = re.compile(",url\('(//.*.ttf)'\) format\('woff'\)")
    rst = cmp.findall(response.text)
    ttf = requests.get("http:" + rst[0], stream=True)
    with open("autohome.ttf", "wb") as pdf:
        for chunk in ttf.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
    # 解析字体库font文件
    font = TTFont('autohome.ttf')
    font = TTFont('autohome.ttf')  # 打开本地字体文件01.ttf
    font.saveXML('01.xml')  # 将ttf文件转化成xml格式并保存到本地，主要是方便我们查看内部数据结构

    uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()
    unicode_list = [eval(r"u'\u" + uni[3:] + "'") for uni in uni_list[1:]]
    # utf8List = [eval("u'\u" + uni[3:] + "'").encode("utf-8") for uni in uniList[1:]]
    wordList = ['一', '七', '三', '上', '下', '不', '中', '档', '比', '油', '泥', '灯',
                '九', '了', '二', '五', '低', '保', '光', '八', '公', '六', '养', '内', '冷',
                '副', '加', '动', '十', '电', '的', '皮', '盘', '真', '着', '路', '身', '软',
                '过', '近', '远', '里', '量', '长', '门', '问', '只', '右', '启', '呢', '味',
                '和', '响', '四', '地', '坏', '坐', '外', '多', '大', '好', '孩', '实', '小',
                '少', '短', '矮', '硬', '空', '级', '耗', '雨', '音', '高', '左', '开', '当',
                '很', '得', '性', '自', '手', '排', '控', '无', '是', '更', '有', '机', '来']
    # 获取发帖内容
    print(unicode_list)
    # note = response.cssselect(".tz-paragraph")[0].text_content().encode('utf-8')
    # for i in range(len(utf8List)):
    #     note = note.replace(utf8List[i], wordList[i])

    # src = Selector(text=response.text)
    #
    # data = src.xpath('//*[@id="js-reply-list-container"]//li')
    # for i in data:
    #     meta = {
    #         'replay': i.xpath('.//*[@class="reply-detail"]').get(),
    #         # 'date': i.xpath('string(.//*[@class="reply-top"])').get(),
    #         # 'user_name': i.xpath('.//div[@class="js-user-info-container"]').get(),
    #     }
    #     print(meta)


if __name__ == '__main__':
    # start_request()
    parse()
