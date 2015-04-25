#-*- coding: utf8 -*-
import urllib2
import re
import threading

def getHtml(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent}
    req = urllib2.Request(url = url, headers = headers)
    
    try:
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.URLError,e:
        return e.reason

def getInfo(num):
    url1 = 'http://www.ppdai.com/list/' + str(num) + '?loanlist'
    html = getHtml(url1)
    record = []
    #获取  名字
    reg = r'class="username">(.+)</a>'
    name = re.findall(reg, html)
    if len(name) == 0:
        return
    record.append(num)
    record.append(name[0])
    #获取  接待总额  年利率  期限
    reg = r'<dd>(?:<em>.*</em>)?([0-9.,]+)(?: ?<em>.*</em>)?</dd>'
    list = re.findall(reg, html)
    record.extend(list)
    """
        #获取  借入信用  借出信用  性别  年龄
        url = 'http://www.ppdai.com/user/' + name[0]
        html = getHtml(url)
        reg = r'class="cf7971a">([0-9]+)'
        list = re.findall(reg, html)
        record.extend(list)
        #reg = r'<p class="lh30 txc"><span> *(.+)</span>'
        reg = r'<span> *(.+)</span>'
        sex = re.findall(reg, html)
        record.extend(sex)
        reg = r'([^ \n]+) *</span></p>'
        age = re.findall(reg, html)
        record.extend(age)
        #获取  借入等级信息
        reg = r'<[bs]>([0-9]+)</[bs]>'
        list = re.findall(reg, html)
        record.extend(list[:4])
        reg = r'class="txc">([-0-9]+)'
        list = re.findall(reg, html)
        record.extend(list)
        reg = r'([0-9]+) 分</p>'
        list = re.findall(reg, html)
        record.extend(list)
        """
    #互斥锁保证同一时间只有一个线程在输出
    mutex.acquire()
    for value in record:
        print value,
    print
    mutex.release()
#每个线程处理一个区间
def getRange(l, r):
    for i in range(l,r):
        getInfo(i)

numSt = 100000
numEnd = 2200000
totalThread = 100
gap = (numEnd - numSt) / totalThread
#总共开100个线程 所以每个线程要处理gap个页面
mutex = threading.Lock()
for i in range(numSt, numEnd, gap):
    t = threading.Thread(target=getRange,args=(i, i+gap,))
    t.start()
