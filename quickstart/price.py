from bs4 import BeautifulSoup
import requests
import pprint


class PriceInvestigator():
    """docstring for PriceInvestigator

    Usage:
        from quickstart.price import PriceInvestigator
        a = PriceInvestigator()
        output = a.price(<book>)
    """
    def __init__(self, test=False):
        print('__init__')
        self.TAAZE = None
        if test:
            self.price()
            self.price('Python')
            self.clear()
            self.price()

    def clear(self):
        self.TAAZE = None
        print('Clear results')

    def askTAAZE(self, book, number=3):
        info = {}
        url = 'http://www.taaze.tw/search_go.html'
        payload = {'keyType[]': 0, 'keyword[]': book}
        r = requests.get(url=url, params=payload)
        soup = BeautifulSoup(r.text, "html.parser")
        div_searchresult_row = soup.find_all("div", "searchresult_row")
        results = {
            'default': [],
            '(二手書)': [],
            '(電子書PDF版)': [],
        }
        for tag in div_searchresult_row:
            case = tag.find("li", "linkC").text.split('\xa0')[1]
            if case == '':
                results['default'].append(tag.a)
            else:
                results[case].append(tag.a)
        print('querying books...')
        for a_tag in results['default'][:number]:
            r = requests.get(url=a_tag['href'])
            print("get(url=%s)" % a_tag['href'])
            if r.status_code != requests.codes.ok:
                info['status_code'] = r.status_code
                info['headers'] = r.headers
                info['text'] = r.text
                return info
            soup = BeautifulSoup(r.text, "html.parser")
            n = soup.find(id='prodInfo3')('li')
            label = ['網址', '作者', '定價', '優惠價', '現金回饋',
                     '優惠截止日', '運送方式', '銷售地區', '庫存',
                     '配送方式', '其他版本']
            value = [a_tag['href']] + [''] * (len(label) - 1)
            c = dict(zip(label, value))
            for x in n:
                text = x.text.replace('\n', '')
                if '：' in text:
                    key = text.split('：')[0]
                    c[key] = text
                elif text == '':
                    pass
                else:
                    key = '庫存'
                    c[key] = text
            info[a_tag.text] = c
        self.TAAZE = info

    def price(self, book=None):
        if book:
            print(book)
            self.askTAAZE(book)
        if self.TAAZE == None:
            msg = [
                'We can not find the price.',
                'Maybe you can try this:',
                "1) price('Python')",
                'or',
                "2) askTAAZE('Python')",
                '   price()',
            ]
            print('\n'.join(msg))
            return
        for x in self.TAAZE:
            #
            #  TODO  #
            #
            #check if those keys have exist
            print('書名：', x)
            print(self.TAAZE[x]['定價'])
            print(self.TAAZE[x]['優惠價'])
            print(self.TAAZE[x]['優惠截止日'])
            print(self.TAAZE[x]['庫存'])
            print(self.TAAZE[x]['網址'])

class ATest(object):
    """docstring for ATest"""
    def __init__(self, *arg):
        super(ATest, self).__init__()
        self.arg = arg

    def b(self):
        self.a()

    def a(self):
        print('a')


def lookupPrice(book):
    """
    lookupPrice
    """

    TAAZE = {
        'name': 'TAAZE 讀冊生活',
        'url': 'http://www.taaze.tw',
        'search_url': '/search_go.html',
        # keyword[]
        # keyType[]
        # prodKind
        # prodCatId
        # catId
        # salePriceStart
        # salePriceEnd
        # saleDiscStart
        # saleDiscEnd
        # publishDateStart
        # publishDateEnd
        # prodRank
        # addMarkFlg
        'search_payload': {
            #combined with +
            'keyword[]': '',
            # >搜尋類型
            #全文
            #書名
            #作者
            #出版社
            #標籤
            #冊格子
            'keyType[]': 0,
            # >商品類型
            #選擇業種
            #全館
            #圖書
            #雜誌
            #電子書／雜誌
            #創意生活
            'prodKind': 0,
            #選擇商品源別 0
            # #全館
            #新品 A
            #二手 C
            # #圖書
            #新品 111
            #二手 113
            # #雜誌
            #中文雜誌 211
            #歐美雜誌 231
            #日文MOOK 241
            #日文雜誌 271
            # #電子書／雜誌
            #中文電子書 141
            #中文電子雜誌 251
            # #創意生活
            #創意文具 611
            #生活雜貨 621
            'prodCatId': 0,
            # #全館
            #
            #不分類 0
            #
            # #圖書
            #
            # # #新品 111
            # # #二手 113
            #
            #選擇類別 0
            #華文文學 010000000000
            #世界文學 020000000000
            #類型文學 030000000000
            #歷史地理 040000000000
            #哲學宗教 050000000000
            #社會科學 060000000000
            #藝術 070000000000
            #建築設計 080000000000
            #商業 090000000000
            #語言 100000000000
            #電腦 110000000000
            #生活風格 120000000000
            #醫學保健 130000000000
            #旅遊 140000000000
            #漫畫／輕小說 150000000000
            #政府考用 160000000000
            #少兒親子 170000000000
            #教育 180000000000
            #科學 190000000000
            #心理勵志 200000000000
            #傳記 210000000000
            #華文文學研究 010100000000
            #中國古典文學 010200000000
            #現代詩 010400000000
            #現代散文 010500000000
            #小說 010600000000
            #華文文學人物傳記 010800000000
            #
            # #雜誌
            #
            # # #中文雜誌 211
            # # #歐美雜誌 231
            #
            # 選擇類別 0
            # 財經企管 010000000000
            # 人文文學 020000000000
            # 科學科技 030000000000
            # 電腦3C 040000000000
            # 生活風格 050000000000
            # 休閒嗜好 060000000000
            # 影視娛樂 070000000000
            # 旅遊情報 080000000000
            # 語言學習 090000000000
            # 藝術欣賞 100000000000
            # 建築裝潢 110000000000
            # 音樂音響 120000000000
            # 親子育樂 130000000000
            # 工商企管 010100000000
            # 投資理財 010200000000
            # 新聞時事 010300000000
            # 法律 010400000000
            #
            # # #日文MOOK 241
            #
            # 選擇類別 0
            # 風格藝術設計 010000000000
            # 生活空間佈置 020000000000
            # 和風文藝史地 030000000000
            # 卡漫動畫電玩 040000000000
            # 親子兒童繪本 050000000000
            # 居家生活手藝 060000000000
            # 樂活休閒旅遊 070000000000
            # 美容美髮彩妝 080000000000
            # 女性流行時尚 090000000000
            # 男性流行時尚 100000000000
            # 藝術欣賞 010100000000
            # 商業設計 010200000000
            # 工藝技術 010300000000
            # 趣味文具 010400000000
            # 鋼琴樂譜 010500000000
            # 電腦設計 010600000000
            #
            # # #日文雜誌 271
            #
            # 選擇類別 0
            # 風格藝術設計 010000000000
            # 生活空間佈置 020000000000
            # 趣味嗜好收藏 030000000000
            # 卡漫動畫電玩 040000000000
            # 親子兒童繪本 050000000000
            # 居家生活手藝 060000000000
            # 樂活休閒旅遊 070000000000
            # 美容美髮彩妝 080000000000
            # 女性流行時尚 090000000000
            # 男性流行時尚 100000000000
            #
            # #電子書／雜誌
            #
            # # #中文電子書 141
            #
            # 選擇類別 0
            # 華文文學 010000000000
            # 世界文學 020000000000
            # 類型文學 030000000000
            # 歷史地理 040000000000
            # 哲學宗教 050000000000
            # 社會科學 060000000000
            # 藝術 070000000000
            # 建築設計 080000000000
            # 商業 090000000000
            # 語言 100000000000
            # 電腦 110000000000
            # 生活風格 120000000000
            # 醫學保健 130000000000
            # 旅遊 140000000000
            # 漫畫／輕小說 150000000000
            # 政府考用 160000000000
            # 少兒親子 170000000000
            # 教育 180000000000
            # 科學 190000000000
            # 心理勵志 200000000000
            # 傳記 210000000000
            # 華文文學研究 010100000000
            # 中國古典文學 010200000000
            # 現代詩 010400000000
            # 現代散文 010500000000
            # 小說 010600000000
            # 文學人物傳記 010800000000
            #
            # # #中文電子雜誌 251
            #
            # 選擇類別 0
            # 財經企管 010000000000
            # 新聞時事 020000000000
            # 旅遊情報 030000000000
            # 流行時尚 040000000000
            # 影視娛樂 050000000000
            # 設計藝術 060000000000
            # 電腦電玩 070000000000
            # 建築家居 080000000000
            # 家庭健康 090000000000
            # 休閒生活 100000000000
            # 人文文學 110000000000
            # 汽機車 120000000000
            # 音樂音響 130000000000
            # 語言學習 140000000000
            # 科技科學 150000000000
            # 運動競技 160000000000
            # 親子育樂 170000000000
            # 工商企管 010100000000
            # 投資理財 010200000000
            # 行銷廣告 010300000000
            # 保險金融 010400000000
            # 房市地政 010500000000
            # 法律 010600000000
            #
            # #創意生活
            #
            # # #創意文具 611
            #
            # 選擇類別 0
            # 事務文具 010000000000
            # 書寫文具 020000000000
            # 紙品系列 030000000000
            # 3C電腦科技 040000000000
            # 美術繪圖 050000000000
            # 辦公事務精品 060000000000
            # 時效性紙品 070000000000
            # 裝訂用品 010100000000
            # 黏貼用品 010200000000
            # 修正用品 010300000000
            # 切割剪用品 010400000000
            # 磁鐵 010500000000
            # 收納袋/資料內袋 010600000000
            # 文件/檔案夾/資料簿 010700000000
            # 書衣 010800000000
            # 筆袋/筆盒 010900000000
            # 車票夾/套 011000000000
            # 證件夾/套 011100000000
            # 書籤/尺 011200000000
            # 筆筒 011400000000
            # 名片夾/盒 011500000000
            # 書架 011600000000
            # 雜誌箱 011700000000
            #
            # # #生活雜貨 621
            #
            # 選擇類別 0
            # 手作DIY 010000000000
            # 包裝收納 020000000000
            # 禮品收藏 030000000000
            # 衣飾用品 040000000000
            # 提袋收納 050000000000
            # 生活旅行 060000000000
            # 居家用品 070000000000
            # 美食禮品 080000000000
            # 節慶禮品 090000000000
            # 玩具教具 100000000000
            # 紙膠帶 010100000000
            # 收納/藏本 010200000000
            # 貼紙 010300000000
            # 剪貼本 010400000000
            # 印章 010500000000
            # 印泥 010600000000
            # ＤＩＹ相關 010700000000
            # 手作用品其他 010800000000
            # 拼圖 010900000000
            # 黏土 011000000000
            'catId': 0,
            #optional
            'salePriceStart': 0,
            #optional
            'salePriceEnd': 0,
            # 請選擇 0
            # 1折 10
            # 2折 20
            # 3折 30
            # 4折 40
            # 5折 50
            # 6折 60
            # 7折 70
            # 8折 80
            # 9折 90
            'saleDiscStart': 0,
            # 請選擇 0
            # 1折 10
            # 2折 20
            # 3折 30
            # 4折 40
            # 5折 50
            # 6折 60
            # 7折 70
            # 8折 80
            # 9折 90
            'saleDiscEnd': 0,
            #optional Min: '19960101'
            'publishDateStart': '19960101',
            #optional
            'publishDateEnd': '20160508',
            #unsure
            'prodRank': 0,
            #unsure
            'addMarkFlg': 0,
        }
    }
