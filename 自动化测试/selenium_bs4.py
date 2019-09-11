from selenium import webdriver
from bs4 import BeautifulSoup
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
driver.get(r'C:\Users\Administrator\PycharmProjects\selenium_test\自动化测试\test1.html')
element=driver.find_element_by_id("choose car")
# print(element.text)
text1=element.get_attribute("innerHTML") #获取内部代码
# print(text1)

soup=BeautifulSoup(text1,"html5lib")

list1=soup.find_all("option")
print(list1)
verilist={"volvo":"volvo","Saab":"saab","Mercedes":"mercedes","Audi":"audi"}

for x in list1:
    key=x.get_text()
    value=x.get("value")
    print(key,value)
    if value==verilist[key]:
        print("pass")
    else:
        print("error")