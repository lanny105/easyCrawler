#coding=utf-8

import re
import urllib2
import nltk
from bs4 import BeautifulSoup


base = "http://www.eeeen.com/zhuanye/baji/"  #水滴英语作文网
base2 = "www.go121.cn"  #水滴英语作文网
base2 = "www.eeeen.com"
xx = 92 #小学
cz = 174 #初中
gz = 240 #高中
dx = 146 #大学
zk = 39 #中考
gk = 72 #高考
ky = 95 #考研
zb = 22 #专八

final_list = []

def getHtml(url):
    page = urllib2.urlopen(url,timeout=10000)
    html = page.read()
    return html

def getDocHtml(html):
    #reg = r'href='(/xx/[0-9]+\.html)'target'  # /xx/54571.html  /nianji/xiaoxue/sh42165.html
    soup = BeautifulSoup(html)
    text = str(soup.find(class_= "list-main"))
    reg = r'sh\d+\.html'
    doc_re = re.compile(reg)
    doc_list = re.findall(doc_re,text)
    #doc_list = set(doc_list)  去重复
    return doc_list

html = getHtml(base)

temp = getDocHtml(html)

final_list += temp

fl=open('英语作文网专八作文链接.txt', 'w')

print '第',1,'页有:\n',temp

for x in temp:
    fl.write(base+x)
    fl.write('\n')


for x in range(1,zb):
    source = base + 'list_27_'+str(x+1) +'.html'
    html = getHtml(source)
    temp = getDocHtml(html)
    print '第',x+1,'页有:\n',temp
    for x in temp:
        fl.write(base+x)
        fl.write('\n')
    
    final_list += temp

'''
print len(final_list)

for x in range(len(final_list)):
    final_list[x] = base + final_list[x]
    print final_list[x]

'''


fl.close()


#print '小学作文共有',len(final_list),'条html','如下:\n',final_list




