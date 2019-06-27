# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 08:51:14 2019

@author: koi93
"""
import ConfigParser
import time
import wget
import os
import re,requests
from bs4 import BeautifulSoup

wz=0            #默认从第一个本下载
page=1          #默认从第一页开始下载
hzflag=".jpg"  #默认以jpg格式下载 

class Messg():
    def dirok(self):
        print "文件夹建立完毕"
        
    def direx(self):
        print "文件夹已存在"
        
    def imgok(self):
        print "此页已下载"
        
    def bimgok(self):
        print "此页副本已下载"
        
    def aimgok(self):
        print "已全下载完毕"
        
    def clnok(self):
        print "已清理"
         
    def regerr(self):
        print "region语种参数错误"
        
    def zderr(self):
        print "zd指定位置参数错误，只可取0到50的整数"
    
    def weberr(self):
        print "网址输入有误，请检查hmg.ini"
    
    def bimgstart(self):
        print "此页副本下载完毕，将进行副本替换"
        
    def bimgend(self):
        print "副本替换完成"    
    
    def pngtry(self):
        print "下载失败，试用png格式下载"
        
    def downstart(self):
        print "开始下载"
    
    
class Foo(Messg):   
###对整个网络页面进行爬取###
    def ana(self):
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        originurl=self.url
        fir=requests.get(originurl,headers=headers)
        fir_bs=BeautifulSoup(fir.text,'lxml')
        page=fir_bs.find_all(['h2','img','table'])
        a=[]
        if self.zd==0:
            sl=0
            el=50
        elif self.zd > 0 and self.zd < 51:
            sl=self.zd-1
            el=self.zd
            self.region="all"
            self.zdflag=True
        else:
            self.zderr()
        for n in range(sl,el):
            i=2+4*n
            title=re.compile(r'\<.*?\>').sub('',str(page[i]))
            id=str(page[i+2]).split("\"")[5].split("/")[5]
            sign=str(page[i+2]).split("\"")[5].split("/")[4]
            allpage=int(str(page[i+3]).split("枚")[1].split(">")[2])
            if self.region=="all" or self.region==sign:
                a.append([str(title),str(id),int(allpage),n])
            elif self.region not in ["all","cn","ja","en"]:
                self.regerr()
                break
        self.a=a
        
###重新下载等待###
    def rdwait(self):
        time.sleep(self.timeout)
        
###检查文件夹是否存在###                
    def mckdir(self):
        a=self.a
        for i in range(0,len(a)):
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

###对四种图片名配置###
    def nameimg(self,imgname):
        self.imgname=imgname
        self.jpgname=imgname+".jpg"
        self.pngname=imgname+".png"
        self.bjpgname=imgname+" (1).jpg"
        self.bpngname=imgname+" (1).png" 

###检查图片文件是否存在，不存在将进行下载###                
    def ckimg(self,imgname):
        self.nameimg(imgname)        
        if os.path.exists(self.jpgname) == True and int(os.path.getsize(self.jpgname)) != 0:
            self.imgok()
            self.hzflag=".jpg"
            return True
        elif os.path.exists(self.bjpgname) == True and int(os.path.getsize(self.bjpgname)) != 0:
            self.bimgok()
            self.hzflag=".jpg"
            return True
        if os.path.exists(self.pngname) == True and int(os.path.getsize(self.pngname)) != 0:
            self.imgok()
            self.hzflag=".png"
            return True
        elif os.path.exists(self.bpngname) == True and int(os.path.getsize(self.bpngname)) != 0:
            self.bimgok()
            self.hzflag=".png"
            return True
        else:                
            return False

###将生成的(1)文件对原文件进行替换###    
    def bckimg(self):
        if os.path.exists(self.imgbname) == True and int(os.path.getsize(self.imgbname)) != 0:
            self.bimgstart()
            os.remove(self.imgdname)
            os.rename(self.imgbname,self.imgdname)
            self.bimgend()
            return True

###文件夹下载完毕整理###
    def clndir(self,apage):
        for k in range(1,apage+1):
            imgname=os.path.join(os.getcwd(),self.dirname.decode('utf-8'),str(k))
            self.nameimg(imgname)
            self.clnimg(self.jpgname,self.bjpgname)
            self.clnimg(self.pngname,self.bpngname)
        print self.dirname
        self.aimgok()      

###将图片下载###    
    def imgdown(self):
        a=self.a
        if self.zdflag:
            wzend=self.wz+1
        else:
            wzend=len(a)
        for i in range(self.wz,wzend):
            self.downstart()
            print self.dirname    
            for j in range(self.page,a[i][2]+1):
                flag=False
                url="https://c.mipcdn.com/i/s/https://img.comicstatic.xyz/img/cn/"+a[i][1]+"/"+str(j)
                iurl=url+self.hzflag
                imgname=os.path.join(os.getcwd(),self.dirname.decode('utf-8'),str(j))
                self.imgdname=imgname+self.hzflag
                self.imgbname=self.imgdname[:-4]+" (1)"+self.imgdname[-4:]
                imgflag=self.ckimg(imgname)
                if imgflag:
                    if j == a[i][2]:
                        self.clndir(j)
                    continue
                
                if imgflag == False:
                    print "开始下载第"+str(j)+"页，共"+str(a[i][2])+"页"
                    wget.download(iurl,out=self.imgdname)
                    count=0
                    while int(os.path.getsize(self.imgdname)) == 0 and count < self.rdcount+1:
                        print "第"+str(j)+"页下载失败，重新开始下载"
                        self.rdwait()
                        wget.download(iurl,out=self.imgdname)
                        print iurl
                        if self.bckimg():
                            break
                        if count == self.rdcount:
                            flag = True
                        count=count+1
                        
                if flag:
                    self.pngtry()
                    self.hzflag=".png"
                    if self.zdflag:
                        self.wz=0
                    else:
                        self.wz=a[i][3]
                    self.page=j
                    self.imgdown()
                print "第"+str(j)+"页下载完毕"
                
                if j == a[i][2]:
                    self.clndir(j)
                    self.hzflag=".jpg"

###对下载出错的文件进行清理###               
    def clnimg(self,imgdname,imgbname):
        if os.path.exists(imgdname) == True and int(os.path.getsize(imgdname)) == 0:
            os.remove(imgdname)
            print imgdname
            self.clnok()
        if os.path.exists(imgbname) == True and int(os.path.getsize(imgbname)) == 0:
            os.remove(imgbname)
            print imgbname
            self.clnok()

###检查生成的目录文件名合法###    
    def ckdirname(self,dirname):
        self.dirname=dirname.replace("\\","").replace("|","").replace("/","").replace("?","").replace("*","").replace(":","").replace(">","").replace("<","")
    
###读取配置###
    def iniget(self):
        cfgpath=os.path.join(os.getcwd(),"hmg.ini")
        conf=ConfigParser.ConfigParser()
        conf.read(cfgpath)
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
    
###main###    
    def __init__(self):
        self.iniget()
        self.hzflag=hzflag
        self.wz=wz
        self.page=page
        print self.url
        self.ana()
        self.mckdir()
        self.imgdown()

###开始下载###
Foo()