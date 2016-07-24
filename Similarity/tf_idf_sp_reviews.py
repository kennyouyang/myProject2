#coding=utf-8
'''
Created on 2016年7月19日

@author: hadoop
'''

 

#import util.fileprocessing as fp
import logging
from gensim import corpora, models, similarities
import csv


def read_csv_file(querypath):
    f_csv = open(querypath)
    rows  = csv.reader(f_csv)
    rows.next() 
    print "read_csv_file\n"
    #for row in rows:
        #print row[7]
    return rows

def toMatrix(q_file,q_file2,storepath):
    users_id = []
    matrixfile = open(storepath  + '.csv', 'w')
    for qrow in q_file:#生成矩阵-表头
        print qrow[15],"#生成矩阵-表头"
        #matrixfile.write(qrow[15]+",")
        users_id.append(qrow[15])
    matrixfile.write(",".join(users_id))
    print "matrixfile.write(",".join(users_id))"
    #f = open('../results/reviewscut.csv', 'a')
    for q_row2 in q_file2:#把每条评论当作搜索词
        print " for q_row2 in q_file2:"
        #print "for q_row in q_file"
        userid=  q_row2[15]
        query = q_row2[7]
        #query = "酒水 两百 消费 300 团购 人均 出品 还会 白开水 ~ 不错 豪吃 提供 券 哈哈哈 餐饮 美中不足"
        print userid,"------------"  
        print query,"------------" 
        vec_bow = dictionary.doc2bow(query.split())#把商品描述转为词包
        vec_tfidf = tfidf[vec_bow]#直接使用上面得出的tf-idf 模型即可得出商品描述的tf-idf 值
        
         
        index = similarities.MatrixSimilarity(corpus_tfidf) #把所有评论做成索引
        sims = index[vec_tfidf]#利用索引计算每一条评论和商品描述之间的相似度
        
        similarity = list(sims)#把相似度存储成数组，以便写入txt 文档
        
        write = csv.writer(matrixfile)
        #row=row.strip('\n')
        #seg_result = (row.encode("utf-8"))
        
        
        ii=0
        point = []
        for sim_point in similarity:
            #print ii,'-',i
            point.append(sim_point+",")
            #sim_file.write(str(sim_point)+'\n')#写入txt 时不要忘了编码
            ii=ii+1
        str_point=",".join(point)
        matrixfile.write('aaa'+'\n')
        
    print "matrixfile.close()"   
    matrixfile.close()
        #print users_id
        

def similarity_toMatrix(datapath, querypath, storepath):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    class MyCorpus(object):
        def __iter__(self):
            rows = read_csv_file(datapath)
            for line in rows:
                #print line[7]+"line[7]"
                #print line[7].split()
                #print line.split()
                #print str(line[7]).split()
                #print (line[7].decode("utf-8")).split(),"========"
                yield line[7].split()
                
            #for line in open(datapath):
                #yield line.split()
    #将网页文档转化为tf-idf
    #以下是把评论通过gensim 转化为tf-idf 形式，程序具体解释参见52nlp的博客或gensim官方文档
    Corp = MyCorpus()
    print "Corp",Corp,"---------"   
    
    dictionary = corpora.Dictionary(Corp)
    corpus = [dictionary.doc2bow(text) for text in Corp]#把所有评论转化为词包（bag of words）
    #print "corpus",corpus,"---------" 
    
    #print corpus
    tfidf = models.TfidfModel(corpus)#使用tf-idf 模型得出该评论集的tf-idf 模型
    #print "tfidf",tfidf,"---------" 
    corpus_tfidf = tfidf[corpus]#此处已经计算得出所有评论的tf-idf 值
    #print "corpus_tfidf",corpus_tfidf,"---------" 
    
    q_file = read_csv_file(querypath)#open(querypath, 'r')#读取商品描述的txt 文档
    q_file2 = read_csv_file(querypath)
    #生产评分矩阵
    
    #toMatrix(q_file,q_file2,"../Statistics/data/usermatrix.csv")    
    users_id = []
    matrixfile = open("../Statistics/data/usermatrix____111.csv", 'ab')
    for qrow in q_file:#生成矩阵-表头
        print qrow[15]
        #matrixfile.write(qrow[15]+",")
        users_id.append(qrow[15])
    matrixfile.write("row,"+(",".join(users_id))+"\n")
    print "matrixfile.write(",".join(users_id))"
    #f = open('../results/reviewscut.csv', 'a')
    for qrow2 in q_file2:#把每条评论当作搜索词
        print " for q_row2 in q_file2:"
        #print "for q_row in q_file"
        userid=  qrow2[15]
        query = qrow2[7]
        #query = "酒水 两百 消费 300 团购 人均 出品 还会 白开水 ~ 不错 豪吃 提供 券 哈哈哈 餐饮 美中不足"
        print userid,"------------"  
        print query,"------------" 
        vec_bow = dictionary.doc2bow(query.split())#把商品描述转为词包
        vec_tfidf = tfidf[vec_bow]#直接使用上面得出的tf-idf 模型即可得出商品描述的tf-idf 值
        
         
        index = similarities.MatrixSimilarity(corpus_tfidf) #把所有评论做成索引
        sims = index[vec_tfidf]#利用索引计算每一条评论和商品描述之间的相似度
        
        similarity = list(sims)#把相似度存储成数组，以便写入txt 文档
        
        #write = csv.writer(matrixfile)
        #row=row.strip('\n')
        #seg_result = (row.encode("utf-8"))
        
        
        ii=0
        point = []
        for sim_point in similarity:
            #print ii,'-',sim_point
            point.append(str(sim_point))
            #sim_file.write(str(sim_point)+'\n')#写入txt 时不要忘了编码
            ii=ii+1
        str_point=",".join(point)
        matrixfile.write(str(userid)+','+str_point+'\n') 
        print userid+"写成功"+point[0]
        #print str(userid)+','+str_point+'\n'
    print "matrixfile.close()"   
    matrixfile.close()
        #print users_id
     
    
def similarity(datapath, querypath, storepath):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    class MyCorpus(object):
        def __iter__(self):
            rows = read_csv_file(datapath)
            for line in rows:
                #print line[7]+"line[7]"
                #print line[7].split()
                #print line.split()
                #print str(line[7]).split()
                #print (line[7].decode("utf-8")).split(),"========"
                yield line[7].split()
                
            #for line in open(datapath):
                #yield line.split()
    #将网页文档转化为tf-idf
    #以下是把评论通过gensim 转化为tf-idf 形式，程序具体解释参见52nlp的博客或gensim官方文档
    Corp = MyCorpus()
    print "Corp",Corp,"---------"   
    
    dictionary = corpora.Dictionary(Corp)
    corpus = [dictionary.doc2bow(text) for text in Corp]#把所有评论转化为词包（bag of words）
    #print "corpus",corpus,"---------" 
    
    #print corpus
    tfidf = models.TfidfModel(corpus)#使用tf-idf 模型得出该评论集的tf-idf 模型
    #print "tfidf",tfidf,"---------" 
    corpus_tfidf = tfidf[corpus]#此处已经计算得出所有评论的tf-idf 值
    #print "corpus_tfidf",corpus_tfidf,"---------" 
    
    q_file = read_csv_file(querypath)#open(querypath, 'r')#读取商品描述的txt 文档
    q_file2 = read_csv_file(querypath)
    #生产评分矩阵
    #toMatrix(q_file,q_file2,"../Statistics/data/usermatrix____100.csv")    
    
    
    print "q_file",q_file
    #query = q_file.readline() 
    #求每条评论与其他评论的相似度
    for q_row in q_file:#把每条评论当作搜索词
        #print "for q_row in q_file"
        userid=  q_row[15]
        query = q_row[7]
        #query = "酒水 两百 消费 300 团购 人均 出品 还会 白开水 ~ 不错 豪吃 提供 券 哈哈哈 餐饮 美中不足"
        print userid,"------------"  
        print query,"------------" 
        vec_bow = dictionary.doc2bow(query.split())#把商品描述转为词包
        vec_tfidf = tfidf[vec_bow]#直接使用上面得出的tf-idf 模型即可得出商品描述的tf-idf 值
        
         
        index = similarities.MatrixSimilarity(corpus_tfidf) #把所有评论做成索引
        sims = index[vec_tfidf]#利用索引计算每一条评论和商品描述之间的相似度
        
        similarity = list(sims)#把相似度存储成数组，以便写入txt 文档
        
        sim_file = open(storepath + userid + '.csv', 'w')
        ii=0
             
        for i in similarity:
                #print ii,'-',i
            sim_file.write(str(i)+'\n')#写入txt 时不要忘了编码
            ii=ii+1
        sim_file.close()
        
        '''
        for q_row2 in q_file:
            query2 = q_row2[7]
            print query2
            vec_bow = dictionary.doc2bow(query2.split())#把商品描述转为词包
            vec_tfidf = tfidf[vec_bow]#直接使用上面得出的tf-idf 模型即可得出商品描述的tf-idf 值
        
         
            index = similarities.MatrixSimilarity(corpus_tfidf) #把所有评论做成索引
            sims = index[vec_tfidf]#利用索引计算每一条评论和商品描述之间的相似度
        
            similarity = list(sims)#把相似度存储成数组，以便写入txt 文档
        
            sim_file = open(storepath + userid + '.csv', 'w')
            ii=0
             
            for i in similarity:
                #print ii,'-',i
                sim_file.write(str(i)+'\n')#写入txt 时不要忘了编码
                ii=ii+1
            sim_file.close()
            break#调试
        '''
           

   
    #query = "冲着冬瓜火锅去噶，有138同188选择，唔系太多人，188噶有蛇。。。冬瓜火锅比较需要大火，用噶系煤气炉，比较热。。。而且等噶时间比较耐。特别蛇，要等好耐先熟。。。不过用冬瓜打火锅，味道清甜且不容易上火，特别是青菜，超甜入味。。。鸡也是，用冬瓜火锅煮，又滑嫩好吃。。。另外点了一个淮山丝瓜芋头手打双丸，味道是不错，可猪肉丸牛肉丸太粉不弹牙。。。服务态度好好，火锅都是有专人服务，还有温馨提示。。。蛇血饭就好一般，没啥味道，就油比较多。。。".decode("utf-8")
    #q_file.close()
    
   
similarity_toMatrix("../Statistics/data/reviews_all_4990_test_10.csv","../Statistics/data/reviews_all_4990_test_10.csv","E:/dist/point/")
#similarity("../Statistics/data/reviews_all_4990.csv","C:/Users/hadoop/Workspaces/MyEclipse Professional 2014/Sentimental_Polarities/Statistics/data/reviews_all_4990.csv","../Statistics/data/reviews_all_4990.csv.txt")
#q_file = fp.read_csv_file("C:/Users/hadoop/Workspaces/MyEclipse Professional 2014/Sentimental_Polarities/Statistics/data/reviews_all_4990.csv")#open(querypath, 'r')#读取商品描述的txt 文档
#for q_row in q_file:
    #print q_row[7]

