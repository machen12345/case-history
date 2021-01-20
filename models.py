from django.db import models

# Create your models here.

# 抽象类，不会生成数据表
# class CommonInfo(models.Model):
#     name=models.CharField(max_length=20)
#     class Meta:
#         adstract=True

# class MedicineClass(models.Model):
#     name=models.CharField(max_length=20,verbose_name=u"分类名称")
#     def _str_(self):
#         return self.name

# class MedicineInfo(models.Model):
#     medicineClass=models.ForeignKey(MedicineClass,on_delete=models.CASCADE,null=True,blank=True) # 外键连接MedicineClass，级联删除
#     name=models.CharField(max_length=50)
#     company=models.CharField(max_length=50)
#     dose=models.CharField(max_length=200)
#     medicineimage=models.ImageField(upload_to='upload/%Y/%m',default="upload/default.jpg")


class Hospital(models.Model):
    hostName=models.CharField(max_length=30,verbose_name=u"医院名")
    address=models.CharField(max_length=50,verbose_name=u"医院地址")
    link=models.CharField(max_length=100,verbose_name=u"医院链接")

class Disease(models.Model):
    dName=models.CharField(max_length=20,verbose_name=u"疾病名")
    symptom=models.CharField(max_length=50,verbose_name=u"症状")
    likD=models.CharField(max_length=50,verbose_name=u"疾病链接")

class Medicine(models.Model):
    mName=models.CharField(max_length=40,verbose_name=u"药品名")
    dose=models.CharField(max_length=20,verbose_name=u"剂量")
    company=models.CharField(max_length=20,verbose_name=u"药品公司")

class user(models.Model):
    icard=models.BinaryField(verbose_name=u"身份证号")
    username=models.CharField(max_length=15,verbose_name=u"用户名")
    gender=models.CharField(max_length=4,verbose_name=u"性别")
    phone=models.BigIntegerField(verbose_name=u"电话号码")
    password=models.BinaryField(verbose_name=u"密码")
    regTime=models.DateTimeField(verbose_name=u"注册时间")

class OutCome(models.Model):
    outcome=models.CharField(max_length=500)
    img=models.ImageField(upload_to='upload/%Y/%m',default=None)

class OutComM(models.Model):
    outcomM=models.CharField(max_length=200)
    imgM=models.ImageField(upload_to='uploadM/%Y/%m',default=None)

class bingli(models.Model):
    hsId=models.ForeignKey(Hospital,on_delete=models.CASCADE,null=False,blank=True)
    outId=models.ForeignKey(OutCome,on_delete=models.CASCADE,null=True,blank=True)
    userId=models.ForeignKey(user,on_delete=models.CASCADE,null=False,blank=True)
    time=models.TimeField(auto_now=True)

class usedd(models.Model):
    dId=models.ForeignKey(Disease,on_delete=models.CASCADE,null=False,blank=True)
    blId=models.ForeignKey(bingli,on_delete=models.CASCADE,null=False,blank=True)

class usedm(models.Model):
    mid=models.ForeignKey(Medicine,on_delete=models.CASCADE,null=False,blank=True)
    outMid=models.ForeignKey(OutComM,on_delete=models.CASCADE,null=False,blank=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=False,blank=True)
    blId=models.ForeignKey(bingli,on_delete=models.CASCADE,null=False,blank=True)

