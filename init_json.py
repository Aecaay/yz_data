import requests
import pathlib
import time
import os


def write(folder,name):
    if name == "place":
        url = "http://yz.chsi.com.cn/zsml/pages/getSs.jsp"
        text = requests.get(url).text
    elif name == "ml":
        url = "http://yz.chsi.com.cn/zsml/pages/getMl.jsp"
        text = requests.get(url).text
    elif name == "mldm":
        text = []
        for i in range(1,15):
            if i < 10:
                url = "http://yz.chsi.com.cn/zsml/pages/getZy.jsp?mldm=0"+str(i)
            else:
                url = "http://yz.chsi.com.cn/zsml/pages/getZy.jsp?mldm="+str(i)
            text.append(requests.get(url).text)
            text[i-1] = text[i-1].replace('\r','')
            text[i-1] = text[i-1].replace('\n','')
    elif name == "zyxw":
        url = "http://yz.chsi.com.cn/zsml/pages/getZy.jsp?mldm=zyxw"
        text = requests.get(url).text
    elif name == "flag":
        place = open(folder+"/"+name,"w",encoding='utf-8')
        place.write("ml.json\t\t"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.stat(folder+'/ml.json').st_mtime))+'\n')
        place.write("mldm.json\t"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.stat(folder+'/mldm.json').st_mtime))+'\n')
        place.write("place.json\t"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.stat(folder+'/place.json').st_mtime))+'\n')
        place.close()
        return 'init flag'
    place = open(folder+"/"+name+".json",'w',encoding='utf-8')
    place.write(str(text).replace("'",""))
    place.close()


def zyget(q):
    url = "http://yz.chsi.com.cn/zsml/code/zy.do?q="+str(q)
    folder = "./number"
    text = requests.get(url).text
    place = open(folder+"/"+q+".json",'w',encoding='utf-8')
    place.write(str(text).replace("'",""))
    place.close()


def adir():
    folder = "./number"
    flag = folder+"/flag"
    number = pathlib.Path(folder)
    init_flag = pathlib.Path(flag)
    if not number.is_dir():
        os.system("mkdir number")
        write(folder,"ml")
        write(folder,"mldm")
        write(folder,"place")
        write(folder,"zyxw")
        write(folder,"flag")
    elif not init_flag.is_file():
        write(folder,"ml")
        write(folder,"mldm")
        write(folder,"place")
        write(folder,"zyxw")
        write(folder,"flag")
    return print("init.....")

def main():
    adir()




if __name__ == "__main__":
    main()



