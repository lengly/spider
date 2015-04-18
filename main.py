#-*- coding: utf8 -*-

import urllib
import urllib2
import re

def getHtml(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent}
    #values = {}
    #data = urllib.urlencode(values)

    req = urllib2.Request(url = url, headers = headers)
    try:
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.URLError,e:
        return e.reason

numSt = 100000
numEnd = 2200000
for i in range(numSt, numSt + 20):
    url1 = 'http://www.ppdai.com/list/' + str(i) + '?loanlist'

    html = getHtml(url1)

    if (html != 'Not Found'):
        record = []
        #获取  名字
        reg = r'class="username">(.+)</a>'
        name = re.findall(reg, html)
        record.append(i)
        record.append(name[0])
        #获取  接待总额  年利率  期限
        reg = r'<dd>(?:<em>.*</em>)?([0-9.,]+)(?: ?<em>.*</em>)?</dd>'
        list = re.findall(reg, html)
        record.extend(list)

        #获取  借入信用  借出信用  性别  年龄
        url = 'http://www.ppdai.com/user/' + name[0]
        html = getHtml(url)
        reg = r'class="cf7971a">([0-9]+)'
        list = re.findall(reg, html)
        record.extend(list)
        reg = r'<p class="lh30 txc"><span> *(.+)</span>'
        sex = re.findall(reg, html)
        record.extend(sex)
        reg = r'([^ \n]+) *</span></p>'
        age = re.findall(reg, html)
        record.extend(age)

        for value in record:
            print value,
        print




