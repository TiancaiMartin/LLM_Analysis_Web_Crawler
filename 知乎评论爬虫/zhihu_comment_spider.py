import requests
import time
import pandas as pd
import os
import random

# 请求头
# 请求头
agents = [
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
        "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
        "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
        "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1"
    ]
headers = {
        # ip代理池获取时用的url的headers
    'User-Agent': random.choice(agents),
    'ue': 'utf-8'  # 设置翻译支持中文
}
proxy = '127.0.0.1:7890'
proxies = {
    'http':'http://'+proxy,
    'https':'https://'+proxy,
}
requests.adapters.DEFAULT_RETRIES=5
s=requests.session()
s.keep_alive=False


def trans_date(v_timestamp):
	"""10位时间戳转换为时间字符串"""
	timeArray = time.localtime(v_timestamp)
	otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
	return otherStyleTime


def tran_gender(gender_tag):
	"""转换性别"""
	if gender_tag == 1:
		return '男'
	elif gender_tag == 0:
		return '女'
	else:  # -1
		return '未知'

offset = 437393073_10348618130_0
comments = []
i=0
def comment_spider(v_result_file, v_answer_list):
    for answer_id in v_answer_list:
        url0 = url0 = f'https://www.zhihu.com/api/v4/comment_v5/answers/{str(answer_id)}/root_comment?order_by=score&limit=20&offset=935581886_10348671619_0'
        r0 = requests.get(url0, headers=headers)  # 发送请求
        total = r0.json()['counts']['total_counts']  # 一共多少条评论
        print('一共{}条评论'.format(total))
        # 判断一共多少页（每页20条评论）
        max_page = int(total / 20)
        print('max_page:', max_page)
        print('max_page:', max_page)
        for i in range(max_page):
            offset = 935581886_10348671619_0
            url = 'https://www.zhihu.com/api/v4/answers/{}/root_comments?order=normal&limit=20&offset={}&status=open'.format(
                answer_id,
                str(offset))
            r = requests.get(url, headers=headers)
            print('正在爬取第{}页'.format(i + 1))
            j_data = r.json()
            comments = j_data['data']
            # 如果没有评论了，就结束循环
            if not comments:
                print('无评论，退出循环')
                break
            answer_urls = []  # 回答url
            authors = []  # 评论作者
            genders = []  # 作者性别
            author_homepages = []  # 作者主页
            author_pics = []  # 作者头像
            create_times = []  # 评论时间
            contents = []  # 评论内容
            child_tag = []  # 评论级别
            # like_counts = []  # 点赞数
            for c in comments:  # 一级评论
                # 回答url
                answer_urls.append('https://www.zhihu.com/answer/' + answer_id)
                # 评论作者
                author = c['author']['member']['name']
                authors.append(author)
                print('作者：', author)
                # 作者性别
                gender_tag = c['author']['member']['gender']
                genders.append(tran_gender(gender_tag))
                # 作者主页
                homepage = 'https://www.zhihu.com/people/' + c['author']['member']['url_token']
                author_homepages.append(homepage)
                # 作者头像
                pic = c['author']['member']['avatar_url']
                author_pics.append(pic)
                # 评论时间
                create_time = trans_date(c['created_time'])
                create_times.append(create_time)
                # 评论内容
                comment = c['content']
                contents.append(comment)
                print('评论内容：', comment)
                # 评论级别
                child_tag.append('一级评论')
                # 点赞数
                # like_counts.append(c['like_count'])
                if c['child_comments']:  # 如果二级评论存在
                    for child in c['child_comments']:  # 二级评论
                        # 回答url
                        answer_urls.append('https://www.zhihu.com/answer/' + answer_id)
                        # 评论作者
                        print('子评论作者：', child['author']['member']['name'])
                        authors.append(child['author']['member']['name'])
                        # 作者性别
                        genders.append(tran_gender(child['author']['member']['gender']))
                        # 作者主页
                        author_homepages.append(
                            'https://www.zhihu.com/people/' + child['author']['member']['url_token'])
                        # 作者头像
                        author_pics.append(child['author']['member']['avatar_url'])
                        # 评论时间
                        create_times.append(trans_date(child['created_time']))
                        # 评论内容
                        print('子评论内容：', child['content'])
                        contents.append(child['content'])
                        # 评论级别
                        child_tag.append('二级评论')
            # 点赞数
            # like_counts.append(child['like_count'])
            # 保存数据到csv
            header = True
            if os.path.exists(csv_file):  # 如果csv存在，不写表头，避免重复写入表头
                header = False
            df = pd.DataFrame(
                {
                    '回答url': answer_urls,
                    '页码': [i + 1] * len(answer_urls),
                    '评论作者': authors,
                    '作者性别': genders,
                    '评论内容': contents,
                    '作者主页': author_homepages,
                    '作者头像': author_pics,
                    '评论时间': create_times,
                    '评论级别': child_tag,
                    # '点赞数': like_counts,
                }
            )
            # 保存到csv文件
            df.to_csv(v_result_file, mode='a+', index=False, header=header, encoding='utf_8_sig')


if __name__ == '__main__':
	csv_file = '/Users/tiancaixiaohuoban/Desktop/知乎评论爬虫/知乎评论_test.csv'
	# 如果csv存在，先删除，避免由于追加产生重复数据
	if os.path.exists(csv_file):
		print('文件存在，删除：{}'.format(csv_file))
		os.remove(csv_file)
	# 开始爬取, "考研"相关的知乎热门回答id
	# 保存文件名
	comment_spider(v_result_file=csv_file, v_answer_list=['930193847', '802226501', '857896805', '910489150', '935352960'])  # "考研"回答列表
	print('爬虫执行完毕！')
