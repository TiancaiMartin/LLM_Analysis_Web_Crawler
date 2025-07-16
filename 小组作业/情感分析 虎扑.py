import numpy as np
import pandas as pd
import jieba
import matplotlib.pyplot as plt
import re
from gensim.models import doc2vec, ldamodel
from gensim import corpora
import pyLDAvis.gensim_models as gensimvis
from sklearn.feature_extraction.text import CountVectorizer
import scipy.sparse
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

data = pd.read_excel('C:\\Users\\86157\\Desktop\\simplifyweibo_4_moods\\simplifyweibo_4_moods\\s.xlsx').astype(str)
data = data.sample(n=10000)
with open('C:\\Users\\86157\\Desktop\\simplifyweibo_4_moods\\simplifyweibo_4_moods\\停用词.txt', 'r', encoding='utf-8') as f:  #
    stopword_list = [word.strip('\n') for word in f.readlines()]

texts = []
for i in data.index:
    cloud = jieba.lcut(data.loc[i, "review"])
    cloud = [i for i in cloud if not i in stopword_list]
    cloud_t = ' '.join(cloud)
    texts.append(cloud_t)

count = CountVectorizer(max_df=0.80, min_df=2, max_features=5000)
bag = count.fit_transform(texts)
bag_x = scipy.sparse.coo_matrix(bag)
texts=[]
for i in data.index:
    cloud=jieba.lcut(data.loc[i,"review"])
    cloud=[i for i in cloud if not i in stopword_list]
    cloud_t=' '.join(cloud)
    texts.append(cloud_t)


df=pd.read_excel("C:\\Users\\86157\\Desktop\\爬虫所有文件\\虎扑伊朗.xlsx").astype(str)
l=[]
for i in df.index:
    d= df.loc[i,"url"].splitlines()
    for j in d:
        l.append(j)
        cloud=jieba.lcut(j)
        cloud=[i for i in cloud if not i in stopword_list]
        cloud_t=' '.join(cloud)
        texts.append(cloud_t)
count = CountVectorizer(max_df=0.80, min_df=2, max_features=5000)
bag = count.fit_transform(texts)
bag_a=bag[:10000]
bag_b=bag[10000:]
bag_x=bag_a.toarray()
bag_xx=bag_b.toarray()
x_train=bag_x
y_train=data["label"]
x_test=bag_xx
from sklearn.svm import SVC
# svc=SVC(kernel='linear',random_state=0,gamma=0.1,C=1)
svc=SVC(kernel='rbf',random_state=0,gamma=0.1,C=1)
svc.fit(x_train,y_train)
y_predict=svc.predict(x_test)
c={"comment":l,"label":y_predict}
r=pd.DataFrame(c)
# df["label"]=list(y_predict)
r.to_excel("C:\\Users\\86157\\Desktop\\情感分析结果\\虎扑伊朗.xlsx")