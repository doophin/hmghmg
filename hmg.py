# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 08:51:14 2019

@author: koi93
"""
import ConfigParser
import time
import os
import re,requests
from bs4 import BeautifulSoup

page=1          #默认从第一页开始下载
hzflag=".jpg"  #默认以jpg格式下载 

class Messg():
    def dirok(self):
        print u'文件夹建立完毕'
        
    def direx(self):
        print u'文件夹已存在'
        
    def imgok(self):
        print u'此页已下载'
        
    def aimgok(self):
        print u'已全下载完毕'
        
    def clnok(self):
        print u'已清理'
                 
    def zderr(self):
        print u'zd指定位置参数错误，只可取0到50的整数'
    
    def weberr(self):
        print u'网址输入有误，请检查hmg.ini"'  
    
    def pngtry(self):
        print u'下载失败，试用png格式下载'
        
    def downstart(self):
        print u'开始下载'
        
    def creatlocalok(self,name):
        print name
        print u'缓存文件建立成功'
        
    def loadlocalok(self):
        print u'读取缓存文件成功'

    def regmsg(self,msg):
        if msg == "all":
            print u'下载所有本子'
        elif msg == "ja":
            print u'下载所有日语本子'
        elif msg == "en": 
            print u'下载所有英语本子' 
        elif msg == "cn":
            print u'下载所有中文本子'
        else:
            print u'region语种参数错误'
    
class Foo(Messg):   
###对整个网络页面进行爬取###
    def ana(self):
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        originurl=self.url
        fir=requests.get(originurl,headers=headers)
        fir_bs=BeautifulSoup(fir.text,'lxml')
        page=fir_bs.find_all(['h2','img','table'])
        self.f=[]
        for n in range(0,self.allend):
            i=2+4*n
            title=re.compile(r'\<.*?\>').sub('',str(page[i]))
            id=str(page[i+2]).split("\"")[5].split("/")[5]
            sign=str(page[i+2]).split("\"")[5].split("/")[4]
            allpage=str(page[i+3]).split("枚")[1].split(">")[2]
            self.f.append([title,id,allpage,str(n),sign])
        self.creatlocal()
        
###载入缓存文件###
    def loadlocal(self):
        self.f=[]
        r=open(self.localf)
        for i in r.readlines():
            self.f.append(i.strip('\n').split(','))
        r.close()
        self.loadlocalok()
               
###写入缓存文件###
    def creatlocal(self):
        fp = open(self.localf,"w")
        for i in self.f:
            s=','.join(i)
            fp.write(s+"\n")
        fp.close()
        self.creatlocalok(self.localf)              
        
###检查缓存文件###        
    def cklocal(self):
        if os.path.exists(self.localf):
            self.loadlocal()
        else:
            self.ana()
            
###检查语种设置###
    def ckregion(self):
        if self.region not in ["all","cn","ja","en"]:
            self.regmsg(self.region)
            exit()
        elif self.region == "all":
            self.regmsg(self.region)
        else:
            b=[]
            for i in self.f:
                if i[4]==self.region:
                    b.append(i)
            self.f=b
            self.zdend=len(self.f)
            self.regmsg(self.region)
           
###检查是否指定下载###            
    def zddep(self):
        if self.zd==0:
            self.zdflag=False
            self.zdend=len(self.f)
        elif self.zd > 0 and self.zd < 51:
            self.region="all"
            self.zdflag=True
            self.zdend=self.zd+1
        else:
            self.zderr()
            exit()
        
###重新下载等待###
    def rdwait(self):
        time.sleep(self.timeout)
        
###检查文件夹是否存在###                
    def mckdir(self):
        a=self.f
        for i in range(self.zd,self.zdend):
            self.ckdirname(a[i][0])
            dirne=self.dirname
            dirna=os.path.join(os.getcwd(),dirne.decode('utf-8'))
            if os.path.exists(dirna) == False:
                os.mkdir(dirne.decode('utf-8'))
                print dirne
                self.dirok()
            else:
                print dirne
                self.direx()

###对两种图片格式配置###
    def nameimg(self,imgname):
        self.imgname=imgname
        self.jpgname=imgname+".jpg"
        self.pngname=imgname+".png"

###检查图片文件是否存在，不存在将进行下载###                
    def ckimg(self,imgname):
        self.nameimg(imgname)        
        if os.path.exists(self.jpgname) == True and int(os.path.getsize(self.jpgname)) != 0:
            self.imgok()
            self.hzflag=".jpg"
            return True
        elif os.path.exists(self.pngname) == True and int(os.path.getsize(self.pngname)) != 0:
            self.imgok()
            self.hzflag=".png"
            return True
        else:                
            return False

###文件夹下载完毕整理###
    def clndir(self,apage):
        for k in range(1,apage+1):
            imgname=os.path.join(self.dirname,str(k))
            self.nameimg(imgname)
            self.clnimg(self.jpgname,self.pngname)
        print self.dirname
        self.aimgok()      

###下载###
    def downtool(self,url,out):
        r=requests.get(url)
        with open(out,"wb") as f:
            f.write(r.content)
        f.close()

###将图片下载###    
    def imgdown(self):
        a=self.f
        for i in range(self.zd,self.zdend):
            self.downstart()
            self.dirname=a[i][0].decode('utf-8')
            print self.dirname
            for j in range(self.page,int(a[i][2])+1):
                flag=False
                url="https://c.mipcdn.com/i/s/https://img.comicstatic.xyz/img/cn/"+a[i][1]+"/"+str(j)
                iurl=url+self.hzflag
                imgname=os.path.join(self.dirname,str(j))
                self.imgdname=imgname+self.hzflag
                imgflag=self.ckimg(imgname)
                if imgflag:
                    if j == int(a[i][2]):
                        self.clndir(j)
                    continue
                
                if imgflag == False:
                    print "开始下载第"+str(j)+"页，共"+a[i][2]+"页"
                    self.downtool(iurl,self.imgdname)
                    count=0
                    while int(os.path.getsize(self.imgdname)) == 0 and count < self.rdcount+1:
                        print "第"+str(j)+"页下载失败，重新开始下载"
                        self.rdwait()
                        self.downtool(iurl,self.imgdname)
                        print iurl
                        if count == self.rdcount:
                            flag = True
                        count=count+1        
                if flag:
                    self.pngtry()
                    self.hzflag=".png"
                    self.zd=i
                    self.page=j
                    self.imgdown()
                print "第"+str(j)+"页下载完毕"
                
                if j == int(a[i][2]):
                    self.clndir(j)
                    self.hzflag=".jpg"

###对下载出错的文件进行清理###               
    def clnimg(self,imganame,imgbname):
        if os.path.exists(imganame) == True and int(os.path.getsize(imganame)) == 0:
            os.remove(imganame)
            print imganame
            self.clnok()
        if os.path.exists(imgbname) == True and int(os.path.getsize(imgbname)) == 0:
            os.remove(imgbname)
            print imgbname
            self.clnok()

###检查生成的目录文件名合法###    
    def ckdirname(self,dirname):
        self.dirname=dirname.replace("\"","").replace("\\","").replace("|","").replace("/","").replace("?","").replace("*","").replace(":","").replace(">","").replace("<","")
    
###读取配置###
    def iniget(self):
        self.localdir=u'缓存列表'
        if os.path.exists(self.localdir) == False:
            os.mkdir(self.localdir)
        conf=ConfigParser.ConfigParser()
        conf.read("hmg.ini")
        self.url=conf.get("config","url")
        if self.url[-1] != '/':
            self.url=self.url+'/'
        elif self.url[:26] != "https://hmghmg.xyz/search/":
            self.weberr()
        self.region=conf.get("config","region")
        self.zd=int(conf.get("config","zd"))
        timeout=conf.has_option("config","timeout")
        if timeout:
            self.timeout=int(conf.get("config","timeout"))
        else:
            self.timeout=3
        rdcount=conf.has_option("config","rdcount")
        if rdcount:
            self.rdcount=int(conf.get("config","rdcount"))
        else:
            self.rdcount=5
        allend=conf.has_option("config","allend")
        if allend:
            self.allend=int(conf.get("config","allend"))
        else:
            self.allend=50
    
###main###    
    def __init__(self):
        self.iniget()
        self.hzflag=hzflag
        self.page=page
        print self.url
        self.localf=self.localdir+"\\"+self.url.split("/")[4]+"("+self.url.split("/")[5]+").txt"
        self.cklocal()
        self.zddep()
        self.ckregion()
        self.mckdir()
        self.imgdown()
        

###开始下载###
Foo()