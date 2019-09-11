#查找最新一个星期的天气
from selenium import webdriver
import random
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")

driver.get("http://tianqi.2345.com/wuhan/57494.htm")
ele=driver.find_element_by_id("day7info")  #使用整体框架的div_class

# print(ele)
# print(ele.text)
date_teap=[] #时间和温度表
tag=ele.find_elements_by_tag_name("li") #找到webelement列表对象,strong,blue都是子标签的内容
for one in tag:
    dataTime=one.find_element_by_tag_name("strong")
    # print(dataTime.text)
    dataTime=dataTime.text

    teampe=one.find_element_by_class_name("blue")
    # print(lowteampe.text)
    teampe=int(teampe.text)
    date_teap.append([dataTime,teampe]) #将时间和温度以列表的形式插入到列表中
# print(date_teap)
lowdate=[] #最低温度的时间表

minteamp=100 #赋值一个初始变量
for one in date_teap:
    date=one[0]
    teampe1=one[1]
    if teampe1<minteamp:
        minteamp=teampe1 #改变初始变量
        lowdate=[date] #插入空列表要加[]
    elif teampe1==minteamp:
        lowdate.append(date)
# print("%s最低温度是%d度" %  (lowdate[0]+lowdate[1],minteamp))
# print("%s最低温度是%d度" % (random.choice(lowdate),minteamp))
print("%s最低温度是%d度" % (",".join(lowdate),minteamp))

print(lowdate)

driver.quit()