from operator import le
import requests
import bs4
from bs4 import BeautifulSoup
import lxml
import re
import random
from time import sleep

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
]

cnt = 0

def crawl(url):
    global cnt
    cnt = cnt + 1
    header = {
        'User-Agent' : random.choice(user_agent_list)
    }
    web_data = requests.get(url, headers=header)
    if web_data.status_code != 200:
        print(web_data.status_code)
    web_data.encoding='utf-8'
    data = BeautifulSoup(web_data.content, 'lxml')

    # 标题:title
    title = data.find(class_ = 'title-article', id = 'articleContentId').string

    # 博客信息：time,read,liked,collected
    articleInfoBox = data.find(class_ = 'article-info-box')

    # 编辑时间
    timeInfo = articleInfoBox.find(class_ = 'time').string
    search = re.search(r"\d.*\d", timeInfo)
    time = search.group()

    # 浏览量
    read = int(articleInfoBox.find(class_ = 'read-count').string)

    toolBox = data.find(class_ = 'more-toolbox-new')

    # 点赞数
    li = toolBox.find(id = 'is-like')
    liked = int(li.find(id = 'spanCount').string)

    # 收藏数
    li = toolBox.find(class_ = 'tool-item tool-item-size tool-active is-collection')
    collected = int(li.find(class_ = 'count get-collection').string)

    # 作者信息:img_src, name, age, certification, works, weekly, overall, views, level, points, fans, likes, comments, collects
    aside = data.aside
    asideProfile = aside.find(id = 'asideProfile')

    # 头像
    img = asideProfile.find(class_ = 'avatar_pic')
    img_src = img['src']

    # id
    boxTop = asideProfile.find(class_ = 'profile-intro-name-boxTop')
    span = boxTop.find(class_ = 'name')
    name = span.string

    # 码龄
    boxFooter = asideProfile.find(class_ = 'profile-intro-name-boxFooter')
    span = boxFooter.find(class_ = 'personal-home-page personal-home-years')
    ageInfo = span.string
    search = re.search(r"\d+", ageInfo)
    age = search.group()

    # 身份认证
    a = boxFooter.find(class_ = 'personal-home-certification')
    certification = a['title']

    dataInfos = asideProfile.find_all(class_ = 'data-info d-flex item-tiling')

    # 原创数量、周排名、总排名、访问量、等级
    dataInfo = dataInfos[0]
    textCenters = dataInfo.find_all(class_ = 'text-center')
    works = textCenters[0]['title']
    weekly = textCenters[1]['title']
    overall = textCenters[2]['title']
    views = textCenters[3]['title']
    levelInfo = textCenters[4]['title']
    search = re.search(r"\d+", levelInfo)
    level = search.group()

    # 积分、粉丝、获赞、评论、收藏
    dataInfo = dataInfos[1]
    textCenters = dataInfo.find_all(class_ = 'text-center')
    points = textCenters[0]['title']
    fans = textCenters[1]['title']
    likes = textCenters[2]['title']
    comments = textCenters[3]['title']
    collects = textCenters[4]['title']

    #分类
    # <div class="tags-box artic-tag-box">
    content = data.find(class_ = 'baidu_pl')
    # div = data.find(class_ = 'tags-box artic-tag-box')
    # text = div.get_text()
    text = title + content.get_text()
    isClassified = False
    tag = '其他'
    hasTag = {
        'C++' : 0, 'C#' : 0, 'java' : 0, 'javascript' : 0, 'php' : 0, 'python' : 0, 'sql' : 0, 'else' : 1
    }
    if re.search(r'C\+\+', text, re.I):
        hasTag['C++'] = 1
        hasTag['else'] = 0
        if not isClassified:
            isClassified = True
            tag = 'C++'
        else:
            tag+=' C++'
    if re.search(r'C#', text, re.I):
        hasTag['C#'] = 1
        hasTag['else'] = 0
        if not isClassified:
            isClassified = True
            tag = 'C#'
        else:
            tag+=' C#'
    if re.search(r'java(?!.*script)', text, re.I):
        hasTag['java'] = 1
        hasTag['else'] = 0
        if not isClassified:
            isClassified = True
            tag = 'java'
        else:
            tag+=' java'
    if re.search(r'javascript', text, re.I):
        hasTag['javascript'] = 1
        hasTag['else'] = 0
        if not isClassified:
            isClassified = True
            tag = 'javascript'
        else:
            tag+=' javascript'
    if re.search(r'php', text, re.I):
        hasTag['php'] = 1
        hasTag['else'] = 0
        if not isClassified:
            isClassified = True
            tag = 'php'
        else:
            tag+=' php'
    if re.search(r'python', text, re.I):
        hasTag['python'] = 1
        hasTag['else'] = 0
        if not isClassified:
            isClassified = True
            tag = 'python'
        else:
            tag+=' python'
    if re.search(r'sql', text, re.I):
        hasTag['sql'] = 1
        hasTag['else'] = 0
        if not isClassified:
            isClassified = True
            tag = 'sql'
        else:
            tag+=' sql'

    #网页内容
    html_str = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="referrer" content="no-referrer">
        <title>{title}</title>
        <style>
            body {{ 
                padding : 50px 300px 100px 300px;
            }}
            .avatar_pic {{
                height : 50px
            }}
            .author-id {{
                font-size : 25px;
            }}
        </style>
    </head>
    <body>
        <div class='article-title-box'>
            <h1 class='article-title' id='articleContentId'>{articleTitle}</h1>
        </div>
        <div class='tag'>
            分类：{tag}
        </div>
        <hr>
        <div class='article-info-box'>
            <a class='nickName'>作者：{nickName}&nbsp;</a>
            <span class='time'>编辑于&nbsp;{time}&nbsp;</span>
            <span class='read-count'>浏览量：{read}&nbsp;</span>
            <span class='liked'>点赞：{liked}&nbsp;</span>
            <span class='collected'>收藏：{collected}&nbsp;</span>
        </div>
        <hr>
        <div class='author-info-box'>
            <img class='avatar_pic' src='{imgSrc}' alt='加载失败' align='absmiddle'>
            <span class='author-id'>{nickName}&nbsp;</span><br>
            <span class='age'>码龄：{age}&nbsp;</span>
            <span class='certification'>身份认证：{certification}&nbsp;</span>
        </div>
        <div class='author-info-boxTop'>
            <span class='works'>原创：{works}&nbsp;</span>
            <span class='weekly'>周排名：{weekly}&nbsp;</span>
            <span class='overall'>总排名：{overall}&nbsp;</span>
            <span class='views'>浏览数：{views}&nbsp;</span>
            <span class='level'>等级：{level}&nbsp;</span>
        </div>
        <div class='author-info-boxBottom'>
            <span class='points'>积分：{points}&nbsp;</span>
            <span class='fans'>粉丝：{fans}&nbsp;</span>
            <span class='likes'>获赞：{likes}&nbsp;</span>
            <span class='comments'>评论：{comments}&nbsp;</span>
            <span class='collects'>收藏：{collects}&nbsp;</span>
        </div>
        <hr>
        <article>
            {article}
        </article>
        <a class='source' href='{url}' target='_blank'>
            原文链接
        </a>
    </body>
    </html>
    """


    html = html_str.format(title = title, articleTitle = title, nickName = name, time = time, read = read,liked = liked,  
    collected = collected, imgSrc = img_src, age = age, certification = certification, 
    works = works, weekly = weekly, overall = overall, views = views, level = level, points = points, fans = fans,
    likes = likes, comments = comments, collects = collects, article = content, url = url, tag = tag)

    file_name = 'crawler\\html\\' + str(cnt) + '.html'
    print(cnt)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(html)
        f.close()
    
    for key, value in hasTag.items():
        if value == 1:
            file_name = 'crawler\\'+key+'\\'+str(cnt)+'.html'
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(html)
                f.close()
    
    sleep(1)
