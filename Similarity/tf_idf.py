#! /usr/bin/env python2.7
#coding=utf-8


import logging
from gensim import corpora, models, similarities


def similarity(datapath, querypath, storepath):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    class MyCorpus(object):
        def __iter__(self):
            for line in open(datapath):
                yield line.split()
    #将网页文档转化为tf-idf
    #以下是把评论通过gensim 转化为tf-idf 形式，程序具体解释参见52nlp的博客或gensim官方文档
    Corp = MyCorpus()
    dictionary = corpora.Dictionary(Corp)
    corpus = [dictionary.doc2bow(text) for text in Corp]#把所有评论转化为词包（bag of words）
    
    #print corpus
    tfidf = models.TfidfModel(corpus)#使用tf-idf 模型得出该评论集的tf-idf 模型

    corpus_tfidf = tfidf[corpus]#此处已经计算得出所有评论的tf-idf 值
 
    q_file = open(querypath, 'r')#读取商品描述的txt 文档
    query = q_file.readline()
    #query = "冲着冬瓜火锅去噶，有138同188选择，唔系太多人，188噶有蛇。。。冬瓜火锅比较需要大火，用噶系煤气炉，比较热。。。而且等噶时间比较耐。特别蛇，要等好耐先熟。。。不过用冬瓜打火锅，味道清甜且不容易上火，特别是青菜，超甜入味。。。鸡也是，用冬瓜火锅煮，又滑嫩好吃。。。另外点了一个淮山丝瓜芋头手打双丸，味道是不错，可猪肉丸牛肉丸太粉不弹牙。。。服务态度好好，火锅都是有专人服务，还有温馨提示。。。蛇血饭就好一般，没啥味道，就油比较多。。。".decode("utf-8")
    q_file.close()
    vec_bow = dictionary.doc2bow(query.split())#把商品描述转为词包
    vec_tfidf = tfidf[vec_bow]#直接使用上面得出的tf-idf 模型即可得出商品描述的tf-idf 值

 
    index = similarities.MatrixSimilarity(corpus_tfidf) #把所有评论做成索引
    sims = index[vec_tfidf]#利用索引计算每一条评论和商品描述之间的相似度

    similarity = list(sims)#把相似度存储成数组，以便写入txt 文档

    sim_file = open(storepath, 'w')
    for i in similarity:
        print i
        sim_file.write(str(i)+'\n')#写入txt 时不要忘了编码
    sim_file.close()

similarity("E:/dist/re.txt","E:/dist/re.txt","E:/dist/output2.txt")