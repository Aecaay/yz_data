import requests
import bs4
import re
import os
import time
import pathlib
import init_json
import pick_json


def write_txt(data,name):
    txt = open("./datas/"+name,'a+',encoding='utf-8')
    txt.write('[')
    for i in range(len(data)):
        txt.write(data[i])
        if i != len(data)-1:
            txt.write(',\t')
    txt.write(']\n')
    txt.close()



class Web_Url(object):                              #整理网址类

    newurlflag = None
    init_flag = False
    filename = time.strftime("%y%m%d%H%M",time.localtime())

    def __new__(cls,*argc,**kwargs):                #分配单例空间
        if cls.newurlflag is None:
            cls.newurlflag = super().__new__(cls)
        return cls.newurlflag

    def __init__(self):                             #初始化
        if not self.init_flag:
            self.pageno = 0
            folder = "./datas"
            init_data = pathlib.Path(folder)
            if not init_data.is_dir():
                os.system('mkdir ./datas')
            self.init_flag = True

    def catalog(self,data):
        '''category,subject,specialty="",place="",school="",xxfs="",xxlb=""'''
        '''生成目录网址'''
        
        self.ssdm = data[3]           #地区
        self.dwmc = data[4]          #学校
        self.mldm = data[1]         #门类
        self.yjxkdm = data[0]      #学科类别
        self.zymc = data[2]       #专业
        self.xxfs = data[5]            #是否全日制
        self.pageno += 1            #页数
        self.xxlb = data[6]            #站点
        self.url = "http://yz.chsi.com.cn/zsml/queryAction.do?ssdm=%s&dwmc=%s&mldm=%s&mlmc=&yjxkdm=%s&zymc=%s&xxfs=%s%s&pageno="%\
                        (self.ssdm,self.dwmc,self.mldm,self.yjxkdm,self.zymc,self.xxfs,self.xxlb)+str(self.pageno)
        return self.url

    def initschoolurl(self,data):
        '''生成学校网址'''
        for i in range(len(data)):
            data[i] = data[i].replace(";","=&")
            data[i] = "http://yz.chsi.com.cn"+data[i]
        self.data = data
        return self.data

    def zyurl(self,data_list):
        for i in range(len(data_list)):
            data_list[i] = "http://yz.chsi.com.cn"+data_list[i]
        text = open("./datas/"+self.filename+".json",'a+',encoding='utf-8')
        text.write("[\n")
        for i in range(len(data_list)):
            text.write('\t"'+data_list[i]+'"')
            if i != len(data_list)-1:
                text.write(',\n')
        text.write("\n],\n")
        text.close()
        return data_list



class Reptile(object):                                              #爬取类
    newrepflag = None
    init_flag = False

    def __new__(cls,*args,**kwargs):                                #分配单例空间

        if cls.newrepflag is None:
            cls.newrepflag = super().__new__(cls)
        return cls.newrepflag


    def __init__(self):                                         #初始化
        if not self.init_flag:
            self.init_sum = 0
            self.init_flag = True


    def get(self,url):
        self.url = url
        self.init_sum += 1                                           #目录get请求
        page = requests.get(self.url)
        return page.text

    def zyget(self,data):
        self.init_sum += 1                                            #学校get请求
        page = requests.get(data)
        return page.text

class Parser(object):                                               #解析类
    rows, columns = os.popen('stty size', 'r').read().split()
    newparflag = None
    pageno = 1

    def __new__(cls,*args,**kwargs):                                #生成单例空间
        if cls.newparflag is None:
            cls.newparflag = super().__new__(cls)
        return cls.newparflag

    def __init__(self,page_text):                                   #初始化最大页数
        self.lotime = time.strftime("%y%m%d%H%M",time.localtime())+".txt"
        self.text = page_text
        self.soup = bs4.BeautifulSoup(self.text,"html.parser")
        chpage = str(self.soup.find_all("ul",class_="ch-page"))
        find_pageno = re.compile(r'<a href="#" onclick="nextPage\(.*?\)">(.*?)<\/a>')
        # pageno = re.findall(find_pageno,chpage)[-2]
        pageno = re.findall(find_pageno,chpage)
        if len(pageno) >= 2:
            pageno = pageno[-2]
        else:
            pageno = pageno[0]
        self.pageno = pageno

    def parser_school_url(self,page_text):                                    #解析学校url
        self.text = page_text
        self.soup = bs4.BeautifulSoup(self.text,"html.parser")
        link = str(self.soup.find_all("table",class_="ch-table"))
        find_school_url = re.compile(r'<a href="(.*?)" target="_blank">')
        school_url = re.findall(find_school_url,link)
        return school_url

    def parser_link_url(self,data_text):                            #解析范围url
        self.page_text = data_text
        self.page_soup = bs4.BeautifulSoup(self.page_text,"html.parser")
        all_zy_url = str(self.page_soup.find_all("table",class_="ch-table more-content"))
        find_zy_url = re.compile(r'<td class="ch-table-center"><a href="(.*?)" target="_blank">')
        zy_url = re.findall(find_zy_url,all_zy_url)
        return zy_url

    def parser_data(self,data_event):
        self.data_event = data_event
        self.data_soup = bs4.BeautifulSoup(self.data_event,"html.parser")
        soup_text = str(self.data_soup.find_all("div",class_="zsml-wrapper"))
        soup_scope = str(self.data_soup.find_all("thead"))
        soup_suject = str(self.data_soup.find_all("tbody",class_="zsml-res-items"))

        find_unit = re.compile(r'<td class="zsml-summary">(.*?)</td>')
        find_scope = re.compile(r'<th>(.*?)</th>')
        find_suject = re.compile(r'<td>([\S\s]*?)<span class')
        find_msg = re.compile(r'<span class="sub-msg">(.*?)</span>')

        unit = re.findall(find_unit,soup_text)
        if unit[6] == "":
            unit[6] = "不区分"
        elif unit[6].find('\u3000'):
            unit[6].replace('\u3000','、')
        scope = re.findall(find_scope,soup_scope)
        suject = re.findall(find_suject,soup_suject)
        for i in range(len(suject)):
            suject[i] = suject[i].strip()
        msg = re.findall(find_msg,soup_suject)

        print("-"*int(self.columns))
        print(unit)
        print(scope)
        print(suject)
        print(msg)
        print("-"*int(self.columns))


        txt = open("./datas/"+self.lotime,'a+',encoding='utf-8')
        txt.write('-'*int(self.columns)+'\n')
        txt.close()
        write_txt(unit,self.lotime)
        write_txt(scope,self.lotime)
        write_txt(suject,self.lotime)
        write_txt(msg,self.lotime)
        txt = open("./datas/"+self.lotime,'a+',encoding='utf-8')
        txt.write('-'*int(self.columns)+'\n')
        txt.close()







def Ui():
    '''category,subject,specialty="",place="",school="",xxfs="",xxlb=""'''
    pick_json.pick_ml()
    subject = str(input('门类：'))           #input(show ml.json+zyxw)
    if subject == "15":
        pick_json.pick_zyxw()
    else:
        pick_json.pick_mldm(subject)
    category = str(input('门类专业：'))          #input(show mldm.json.2||zyxw.json)
    init_json.zyget(category)
    choice = pick_json.pick_q(category)
    '''转get请求'''
    specialty = str(input('专业方向：'))         #input(get category_url)
    if specialty == "" or specialty == " ":
        specialty = ""
    else:
        specialty = choice[int(specialty)-1]
    pick_json.pick_place()
    place = str(input('地区：'))             #input(show place.json)
    if place == " ":
        place = ""
    school = str(input("校名，还没做："))            #input(show )
    school = ""                                 #先不识别
    xxfs = str(input("1：全日制，2：非全日制："))
    if xxfs != '1' and xxfs != '2':
        xxfs = ""
    xxlb = str(input('1：研究生院,2：自划线院校,3：博士点：'))
    xxlb = pick_json.xxzd(xxlb)
    return category,subject,specialty,place,school,xxfs,xxlb



def main():
    init_json.adir()
    demand = Web_Url()
    datas = Ui()
    url = demand.catalog(datas)
    reptlie = Reptile()
    page_text = reptlie.get(url)
    parser = Parser(page_text)
    demand.pageno = 0
    while(int(demand.pageno)<int(parser.pageno)):
    # while(int(demand.pageno)<1):
        url = demand.catalog(datas)              #首页
        page_text = reptlie.get(url)                                    #请求
        # time.sleep(0.5)
        parser_out = parser.parser_school_url(page_text)                #解析外链接
        page_url = demand.initschoolurl(parser_out)                     #生成外链接
        for i in page_url:
            page_in_text = reptlie.zyget(i)                             #请求
            # time.sleep(0.5)
            parser_in_out = parser.parser_link_url(page_in_text)        #解析
            page_in_url = demand.zyurl(parser_in_out)                   #生成
            for j in parser_in_out:
                page_fin_text = reptlie.zyget(j)                        #请求
                data = parser.parser_data(page_fin_text)                #生成数据

if __name__ == "__main__":
    main()