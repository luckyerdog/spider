# -*- encoding:utf-8 -*-

#-------------------------------------------------------------------------#
#-date:2016.1.14
#-功能：爬取新浪微博大V内容，利用非负矩阵因式分解分析每个博主的特征
#-执行顺序代码：

#import login
#all_words, store_weibos,allwords,l1=get_weibos()
#v=matrix(l1)
#w,h=factorize(v,pc=10,iter=50)
#toppatterns,patternnames=showfeatures(w,h,name_tuple,allwords)
#showarticles(name_tuple,toppatterns,patternnames)
#--------------------------------------------------------------------------#


import requests
from bs4 import BeautifulSoup as bs
import re
import urllib2
import urllib
import json
import sys
import jieba
from numpy import *

COOKIE={'cookie':'SUHB=0auxM_jasiH8MY; _T_WM=a12d9b9c031df54705b7a13dce4f29e0; SUB=_2A257ki-hDeRxGedH6VUZ8SrFzT2IHXVZfLHprDV6PUJbrdANLXPnkW1LHesAjCQzLj9YMHqFXX2tum98m0uBDQ..; gsid_CTandWM=4uic32b91waM0rBi9XqhQ85vMfv'}
header={'Connection':'keep-alive','cookie':COOKIE,'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'}
url='http://weibo.cn/1927814961/profile?vt=4'
req = urllib2.Request(url, headers=header)
content =urllib2.urlopen(req)
result=content.read()
soup=bs(result,"html.parser")
#print result


weibotext=soup.findAll('span',attrs={'class':"ctt"})
print weibotext[1].text


name_tuple = (u'皇马球迷网',u'皇马球迷俱乐部',u'皇马新闻',u'今生只恋伯纳乌',u'凌瑄Cris',u'鸟哥CAGE',u'7CRCRC7',u'美凌格App',u'我是城堡之王666',u'Elainewithu', u'鲜花与海洋之地',u'第七个流浪诗人',u'软梅斯',u'Isco伊斯科',u'灰原蝎')
name_dic = {u'皇马球迷网':u'halamadridcn',u'皇马球迷俱乐部':u'realmadridfans',u'皇马新闻':u'realmadridnews',u'今生只恋伯纳乌':u'realronaldor9',u'凌瑄Cris':u'cashireevans',u'鸟哥CAGE':u'cagezhujunjie',u'7CRCRC7':u'u/2205911672',u'美凌格App':u'LosMerenguesApp',u'我是城堡之王666':u'imking666',u'Elainewithu':u'u/2373007274', u'鲜花与海洋之地':u'oceanfield',u'第七个流浪诗人':u'u/2007952517',u'软梅斯':u'u/2046038533',u'Isco伊斯科':u'kevinv',u'灰原蝎':u'haibarasasori'}

def get_weibos():
    all_words={}    
    store_weibos = {}
    allperson_words=u''.encode('utf8')
    jieba.add_word('C罗')
    jieba.add_word('c罗')
    jieba.add_word('水水')
    jieba.add_word('队宠')
    jieba.add_word('哈梅斯')
    jieba.add_word('魔笛')
    jieba.add_word('齐祖')
    jieba.add_word('我罗')
    for person in name_tuple:        
        person_id = name_dic[person]        
        store_weibos.setdefault(person,{})        
        for index in range(1,11):       #每个人抓6页的微博     
            index_added = str(index)            
            person_url = 'http://weibo.cn/'+person_id+'?filter=1&page='+index_added+'&vt=4'       #url加入filter＝1参数只查看原创微博
            print person_id+':::'+person_url
            req2 = urllib2.Request(person_url, headers=header)
            content2 =urllib2.urlopen(req2).read()
            soup2 = bs(content2,"html.parser")
            #print req2.text
            #print soup1
            for op in soup2.find_all('div'):                
                if u'class' and u'id' in op.attrs.keys() and u'c' in op.attrs[u'class']:               #通过观察网页中div标签中class类为'c'的是微博内容
                    op_weibo = op.span.text       #span.text   text没有括号()
                    #print op_weibo
                    for word in jieba.cut(op_weibo,cut_all=False):  
                        #if len(word)>1 and word not in clean_words:
                        if len(word)>1:
                            #利用jieba.cut得到分词结果集，筛选去掉长度很短的符号或词，同时可以设立clean_words进行过滤
                            #store_weibos为一个字典，每个人下又为一个字典，纪录他的微博中出现的单词及次数                  
                            store_weibos[person].setdefault(word,0)                        
                            store_weibos[person][word]+=1                
            for word_1 in store_weibos[person].keys():  
                all_words.setdefault(word_1,0)   
                all_words[word_1]+=1
            print 'get %s already' %person
            
        #输出每个人微博中出现次数最多的5个词
        sorted_person_words = sorted(store_weibos[person].iteritems(), key=lambda x : x[1], reverse=True)
        words=(person+u': ').encode('utf8')+'\n'
        for word in sorted_person_words[0:5]:
            words=words+(u'  '+word[0]+':'+str(word[1])).encode('utf8')
        allperson_words=allperson_words+words+'\n'+'\n'
        #print allperson_words
    outfile=file('personnel_max_words2.txt','w')
    print allperson_words
    outfile.write(allperson_words)
    outfile.close()
    #allwords 是筛选出在超过3个人中都出现的词以及在少于90%的人中出现的词 
    allwords = [w for w,n in all_words.items() if n>3 and n<len(name_dic.keys())*0.7]
    #l1是每个人创建跟allwords一样长的词表，对应这些词在该人下出现的次数，即为[person-words]矩阵
    l1 = [[(word in store_weibos[person] and store_weibos[person][word] or 0) for word in allwords] for person in name_tuple]

    
    return all_words, store_weibos,allwords,l1


def difcost(a,b):     #构造代价函数，用于矩阵特征分解 
  dif=0    
  for i in range(shape(a)[0]):        
    for j in range(shape(a)[1]):            
      dif += pow(a[i,j]-b[i,j],2)    
  return dif

 #分解矩阵，将[个人－单词]矩阵分解为[个人－特征]＊[特征－单词]矩阵 . l1为元组，需v=matrix(l1)转化为数组代入
def factorize(v, pc=10, iter=100):    
  ic = shape(v)[0]   #ic*fc   
  fc = shape(v)[1]    
  w = matrix([[random.random() for j in range(pc)] for i in range(ic)])  #ic*pc weight matrix    
  h = matrix([[random.random() for j in range(fc)] for i in range(pc)])  #pc*fc feature matrix    
  #find v = w*h Matrix Factorization
  for i in range(iter):
      wh = w*h        
      cost = difcost(wh,v)        
      #every 10 times print the cost        
      if i%10 == 0: print cost        
      if cost == 0: break        
      hn = (transpose(w)*v)          
      hd = (transpose(w)*w*h)
      h = matrix(array(h)*array(hn)/array(hd))       
      wn = (v*transpose(h)) 
      wd = (w*h*transpose(h))
      w = matrix(array(w)*array(wn)/array(wd))    
  return w,h   

  #按特征展示
def showfeatures(w,h,titles,wordvec,out = 'features2.txt'):    #titles为权重矩阵中的index值，即每一篇文章的题目，或者每一个微博名；Wordvec为所有单词的数组，不至太普通筛选后的，此处为allwords
  outfile = file(out,'w')    
  pc,wc = shape(h)  # h is feature matrix    
  toppatterns=[[] for x in range(len(titles))]    
  patternnames= []    

  #pc is the number of features    
  for i in range(pc):         
    slist=[]        # wc is the number of words        
    for j in range(wc):            
      slist.append((h[i,j],wordvec[j]))        
    slist.sort()        
    slist.reverse()        #sorted by weight-h[i,j] from big to little, the get the correlated word        
    n = [s[1] for s in slist[0:7]]        
    outfile.write(str(n)+'\n')        
    patternnames.append(n)        #w[j,i] refer to article-feature        
    flist = []        
    for j in range(len(titles)):            
      flist.append((w[j,i],titles[j]))            
      toppatterns[j].append((w[j,i],i,titles[j]))        

    flist.sort()        
    flist.reverse()        
    for f in flist[0:3]:            
      outfile.write(str(f)+'\n')        
    outfile.write('\n')    

  outfile.close()    
  return toppatterns,patternnames    

# 按文章展示
def showarticles(titles, toppatterns, patternnames, out='fanUsers2.txt'):
    outfile = file(out,'w')
    for j in range(len(titles)):
        outfile.write(titles[j].encode('utf8')+'\n')
        # sort w:article-feature desc
        toppatterns[j].sort()
        toppatterns[j].reverse()
        #top3 w[article,feature]
        for i in range(3):
            #outfile.write(str(toppatterns[j][i][1])+' '+str(patternnames[toppatterns[j][i][0]])+'\n')
        #outfile.write('\n')
            a = u''.encode('utf8')
            for word in patternnames[toppatterns[j][i][1]]:
                a=a+' '+word.encode('utf8')
            outfile.write(str(toppatterns[j][i][0])+' '+ a +'\n')        
# w[article,feature]+feature    ,respectively
        outfile.write('\n')
    outfile.close()



all_words, store_weibos,allwords,l1=get_weibos()
v=matrix(l1)
w,h=factorize(v,pc=20,iter=50)
toppatterns,patternnames=showfeatures(w,h,name_tuple,allwords)
showarticles(name_tuple,toppatterns,patternnames)
    

