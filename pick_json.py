import json


def pick_ml():
    ml = open("./number/ml.json","r",encoding="utf-8")
    data = ml.read()
    dd = json.loads(data)
    for i in range(len(dd)):
        print(dd[i]['dm']+":"+dd[i]['mc'],end=" ")
    print("15:专业学位")
    ml.close()

def pick_mldm(dm="08"):
    if dm == "":
        mldm = open("./number/mldm.json","r",encoding="utf-8")
        data = mldm.read()
        print(data)
        dd = json.loads(data)
        for i in range(len(dd)):
            for j in range(len(dd[i])):
                print(dd[i][j]['dm']+":"+dd[i][j]['mc'],end="\t")
                if j%7 == 0 and j!=0:
                    print("")
        print("")
        mldm.close()
    else:
        dm = int(dm)
        mldm = open("./number/mldm.json","r",encoding="utf-8")
        data = mldm.read()
        dd = json.loads(data)
        for i in range(len(dd[dm-1])):
            print(dd[dm-1][i]['dm']+":"+dd[dm-1][i]['mc'],end="\t")
            if i%7 == 0 and i!=0:
                    print("")
        print("")
        mldm.close()


def pick_zyxw():
    zyxw = open("./number/zyxw.json","r",encoding="utf-8")
    data = zyxw.read()
    dd = json.loads(data)
    for i in range(len(dd)):
        print(dd[i]['dm']+":"+dd[i]['mc'],end="\t")
        if i%7 == 0 and i!=0:
            print("")
    print("")
    zyxw.close()


def pick_place():
    place = open("./number/place.json","r",encoding="utf-8")
    data = place.read()
    dd = json.loads(data)
    for i in range(len(dd)):
        print(dd[i]['dm']+":"+dd[i]['mc'],end="\t")
        if i%8 == 0 and i!=0:
            print("")
    print(end="\n")
    place.close()


def xxzd(xxlb):
    if xxlb == "1" or xxlb == "1,":
        xxlb = '&xxlb=YJSY'
    elif xxlb == "2" or xxlb == "2,":
        xxlb = "&xxlb=ZHX"
    elif xxlb == "3" or xxlb == "3,":
        xxlb = '&xxlb=BS'
    elif xxlb == "12" or xxlb == "1,2":
        xxlb = "&xxlb=YJSY&xxlb=ZHX"
    elif xxlb == "13" or xxlb == "1,3":
        xxlb = "&xxlb=YJSY&xxlb=BS"
    elif xxlb == "23" or xxlb == "2,3":
        xxlb = "&xxlb=ZHX&xxlb=BS"
    elif xxlb == "123" or xxlb == "1,2,3":
        xxlb = "&xxlb=YJSY&xxlb=ZHX&xxlb=BS"
    else:
        xxlb=""
    return xxlb


def pick_q(q="0839"):
    qs = open("./number/"+q+".json","r",encoding="utf-8")
    data = qs.read()
    data = data.replace("[","")
    data = data.replace("]","")
    data = data.replace('"',"")
    data = data.split(",")
    for i in range(len(data)):
        if i+1 < 10:
            print("0"+str(i+1)+":"+data[i],end="\t")
        else:
            print(str(i+1)+":"+data[i],end="\t")
        if i%7 == 0 and i != 0:
            print("")
    print("")
    qs.close()
    return data

def main():
    pick_ml()
    # pick_mldm()
    # pick_zyxw()
    # pick_place()
    # pick_q()




if __name__ == "__main__":
    main()

