import re
import requests
import time,json
from datetime import datetime
from bs4 import BeautifulSoup
class HtmlGetter:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Host': 'aic.hbswkj.com:8080',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',    
        }
        self.session.get("http://aic.hbswkj.com:8080/jedu/",headers=self.headers)
        self.isLogin = False
        
        localtime = time.localtime(time.time())
        now_time = time.strftime("%Y-%m-%d %H:%M:%S",localtime) #获取年月日
        
        self.weekofday = str(datetime.today().isoweekday())          #获取当前期第周几
        
        self.weeks = int(time.strftime("%W"))-34                     #获取当前是第几周

        print('当前时间：'+now_time)

        # self.data_info = '第:{}周,星期:{}'.format(self.weeks,self.weekofday)
        
    def trylogin(self,username,password):
            res= self.session.post("http://aic.hbswkj.com:8080/jedu/login.do",{
                "username":username,
                "password":password
            },headers=self.headers).json()
            self.isLogin = res["success"]
            if res["success"]:
                self.session.cookies.set('username',username)
                time.sleep(0.2)
                self.session.get("http://aic.hbswkj.com:8080/jedu/index.do",headers=self.headers).content
            return self.isLogin

    def get_course_info(self,weeks = int(time.strftime("%W"))-8):
        # weeks+=1 #测试

        res = self.session.get('http://aic.hbswkj.com:8080/jedu/edu/core/eduScheduleInfo/getStudentWeekSchedule.do?week=%s&semId='%(weeks),headers = self.headers)
        length = len(res.json()['data']['schedule'])
        info = {}
        name1 = []
        name2 = []
        name3 = []
        name4 = []
        name5 = []
        name6 = []
        name7 = []
        for i in range(length):
            name = res.json()['data']['schedule'][i]['courseName']
            week = res.json()['data']['schedule'][i]['weekOfDay']
            placename = res.json()['data']['schedule'][i]['placeName']
            start = str(res.json()['data']['schedule'][i]['eduTimeSchedule']['eduLesson']['startLesson'])
            end = str(res.json()['data']['schedule'][i]['eduTimeSchedule']['eduLesson']['endLesson'])
            if week=='mon':
                name1.append('第'+start+'~'+end+'节:' + name +' 地点:'+ placename)
            if week=='tue':
                name2.append('第'+start+'~'+end+'节:' + name +' 地点:'+ placename)
            if week=='wed':
                name3.append('第'+start+'~'+end+'节:' + name +' 地点:'+ placename)
            if week=='thu':
                name4.append('第'+start+'~'+end+'节:' + name +' 地点:'+ placename)
            if week=='fri':
                name5.append('第'+start+'~'+end+'节:' + name +' 地点:'+ placename)
            if week=='sat':
                name6.append('第'+start+'~'+end+'节:' + name +' 地点:'+ placename)
            if week=='sun':
                name7.append('第'+start+'~'+end+'节:' + name +' 地点:'+ placename)
        name1.sort()
        name2.sort()
        name3.sort()
        name4.sort()
        name5.sort()
        name6.sort()
        name7.sort()
        info['Monday'] = name1
        info['Tuesday'] = name2
        info['Wednesday'] = name3
        info['Thursday'] = name4
        info['Friday'] = name5
        info['Saturday'] = name6
        info['Sunday'] = name7

        return info




        

    def get_data(self,**kwrags):
        html_data = {}
        data = kwrags
        # --------------------处理数据-----------------------------
        query = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday","Sunday" ]
        for week in query:
            items = {}
            for o in data[week]:
                for i in o.split('\n'):
                    if i[1:4] == '1~2':

                        items['1'] = i[6:]
                        items['2'] = i[6:]
                    elif i[1:4] == '3~4':
                        items['3'] = i[6:]
                        items['4'] = i[6:]

                    elif i[1:4] == '5~6':
                        items['5'] = i[6:]
                        items['6'] = i[6:]

                    elif i[1:4] == '7~8':
                        items['7'] = i[6:]
                        items['8'] = i[6:]

                    elif i[1:4] == '5~8':
                        items['5'] = i[6:]
                        items['6'] = i[6:]
                        items['7'] = i[6:]
                        items['8'] = i[6:]

                    elif i[1:5] == '9~10':

                        items['9'] = i[7:]
                        items['10'] = i[7:]

                    elif i[1:6] == '11~12':

                        items['11'] = i[8:]
                        items['12'] = i[8:]
            html_data[week] = items
        return html_data




if __name__=="__main__":
    items_json = {}
    h = HtmlGetter()
    #这里改账号
    h.trylogin('1905080101', '1905080101a')
    h.get_course_info()
    #这里是第13周到第22周的课表参数,自定义修改
    for i in range(13,23):
        key = f"第{i}周"
        data = h.get_course_info(i)
        items_json[key] = h.get_data(**data)
    #文件路径自己改
    with open("课表.json",mode='a',encoding = "utf-8")as file:
        json.dump(items_json,file,ensure_ascii=False)
        print("写入成功！")






    


        
    

        

        
