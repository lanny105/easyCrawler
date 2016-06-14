#coding=utf-8

import re
import urllib

base = "http://www.adreep.cn/fw/"  #水滴英语作文网
base2 = "www.go121.cn"  #水滴英语作文网
base2 = "www.eeeen.com"
xx = 33 #小学
cz = 54 #初中
gz = 70 #高中
dxyy = 122 #大学
fw = 39 #范文

final_list = []

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getDocHtml(html):
    #reg = r'href='(/xx/[0-9]+\.html)'target'  # /xx/54571.html
    reg = r'/fw/\d+\.html'
    doc_re = re.compile(reg)
    doc_list = re.findall(doc_re,html)
    #doc_list = set(doc_list)  去重复
    return doc_list

html = getHtml(base)

temp = getDocHtml(html)
final_list += temp

print '第',1,'页有:\n',temp


for x in range(fw):
    source = base + '?page=' + str(x+1)
    html = getHtml(source)
    temp = getDocHtml(html)
    final_list += temp


final_list = list(set(final_list))  #去重复

for x in range(len(final_list)):
    final_list[x] = "http://www.adreep.cn" + final_list[x]
    print final_list[x]


fl=open('水滴英语范文链接.txt', 'w')
for x in final_list:
    fl.write(x)
    fl.write("\n")
fl.close()


print '范文作文共有',len(final_list),'条html','如下:\n',final_list




