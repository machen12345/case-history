from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.http import HttpResponse
from medicine.models import Medicine,Hospital,user,Disease,OutCome,OutComM,bingli,usedd,usedm
from aip import AipOcr
import os
# Create your views here.

# 定义常量
APP_ID = 'ocrApp'
API_KEY = 'OKTSr3p9kSjoGwP9TDCITYZM'
SECRET_KEY = 'jeDwq3pZaYiQcP34jaw1sMb1lHzsqd93'

# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 定义参数变量
options = {
    'detect_direction': 'true',  # 检测朝向
    'language_type': 'CHN_ENG',  # CHN_ENG：中英文混合
}

# 处理关键字包含或交叉的特殊情况
def fx(s,r):
    if len(s) == 1:
        r.append(s[0])
    else:
        # 处理交叉
        if s[0][1]>=s[1][0] and s[0][1]<=s[1][1] and s[1][0]>s[0][0]:
            s.remove(s[1])
        # 处理包含
        elif s[0][1]>=s[1][1]:
            s.remove(s[1])
        elif s[0][0]>=s[1][0] and s[0][1]<=s[1][1]:
            s.remove(s[0])
        # 既不包含也不交叉
        else:
            r.append(s[0])
            s.remove(s[0])
        fx(s, r)
    return r

# 按照开始索引进行排序
def mysort(s):
    for i in range(1, len(s)):
        for j in range(0, i):
            if s[i][0] < s[j][0]:
                temp = s[j]
                s[j] = s[i]
                s[i] = temp
                break
            else:
                continue
    return s

# 在字符串中查找关键字并进行拆分
def myjieba(s, kList):
    s = s.strip()
    indexLis = []
    resultLis = []
    r = []
    # kList = list(kList)
    indexLis_1 = list()
    for key in kList:
        index = s.find(key)
        indexLis.append([index,index+len(key)])
    for i in range(len(indexLis)):
        if indexLis[i][0]!=-1:
            indexLis_1.append(indexLis[i])
    if indexLis_1:
        # 按照开始索引进行排序
        indexLis = mysort(indexLis_1)
        # 处理关键字包含或交叉的特殊情况
        indexLis = fx(indexLis,r)
        for i in range(len(indexLis)):
            if i < (len(indexLis)-1):
                index1 = indexLis[i][0]
                index1_1 = indexLis[i][1]
                index2 = indexLis[i+1][0]
                str1 = s[index1:index1_1]+'  '+s[index1_1:index2]
                resultLis.append(str1)
        index3 = indexLis[-1][0]
        index3_3 = indexLis[-1][1]
        str2 = s[index3:index3_3]+'  '+s[index3_3:]
        resultLis.append(str2)
    else:
        resultLis.append(s)
    return resultLis

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def index(request):
    return render(request,"yongyao.html")

def dealbl(request):
    blimg=request.FILES.get('BLImage',None)
    if not blimg:
        return HttpResponse("您没有选择文件!")
    destination = open(os.path.join(r'd:\study\vscode python文件\firstDemo\upload\blimg',blimg.name),'wb+')    # 打开特定的文件进行二进制的写操作
    for chunk in blimg.chunks():      # 分块写入文件
        destination.write(chunk)
    destination.close()
    Path='d:\\study\\vscode python文件\\firstDemo\\upload\\blimg\\' + str(blimg.name)
    # 关键字
    key = ['姓名', '年龄', '性别', '住址', '编号', '患者编号','接收时间','送检医师','报告时间',
       '科别', '床号', '标本', '病员号', '诊断', '诊断证明书', '医生', '联系电话', '标本种类', '备注']
    result = aipOcr.basicGeneral(get_file_content(Path), options)
    print(result)
    words_result = result['words_result']
    result=''
    path='upload/blimg/'+str(blimg)
    for i in range(len(words_result)):
        res = myjieba( words_result[i]['words'],key)
        for i in res:
            result=result+i+'\n'
    return render(request,"ack.html",{"result":result,"path":path})


class MedicineListView(ListView):
    model=Medicine 
    # 应用名/modelname_list.html
    # template_name='bingli.html'
    context_object_name='my_medicine'

def getHospital(s,hosName):
    hospitals=Hospital.objects.all()
    Thospital=Hospital.objects
    for hospital in hospitals:
        name=hospital.hostName
        if name in s:
            hosName=name
            Thospital=hospital
            break
        else:
            continue
    return Thospital
    
def getDisease(s,DiseaseName):
    diseases=Disease.objects.all()
    Diseases=[]
    for disease in diseases:
        name=disease.dName
        if name in s:
            DiseaseName.append(name)
            Diseases.append(disease)
        else:
            continue
    return Diseases

def uploadbl(request):
    User=user.objects.first()
    blresult=request.POST.get('result')
    hospitalName=""
    hospital=getHospital(blresult,hospitalName)
    dieaseName=[]
    diseases=getDisease(blresult,dieaseName)
    check_box_list = request.POST.getlist('IsImg')
    if check_box_list:
        path=request.POST.get('path')
        outcome=OutCome.objects.create(outcome=blresult,img=path)
    else:
        outcome=OutCome.objects.create(outcome=blresult)
    bl=bingli.objects.create(hsId=hospital,userId=User,outId=outcome)
    for disease in diseases:
        usedd.objects.create(dId=disease,blId=bl)
    return HttpResponse("Successful!")

