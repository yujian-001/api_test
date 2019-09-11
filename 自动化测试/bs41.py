from bs4 import BeautifulSoup
with open(r"C:\Users\Administrator\PycharmProjects\selenium_test\自动化测试\test1.html",encoding="utf-8") as file:
    doc_html=file.read()

#html文件必选以字符串的形式，进行解析
soup1=BeautifulSoup(doc_html,"html5lib")
print(soup1.get_text) #获取所有内容文本
print(soup1.find("title")) #获取元素的代码

print(soup1.find("p",id="test1")) #根据id获取指定的代码
#--------------
print(soup1.title.string)#获取元素的文本内容
print(soup1.option.string)

print(soup1.title.get_text())#获取元素的文本内容

print(soup1.title.name) #获取标签的名称

print(soup1.title.parent) #获取父节点的代码

print(soup1.find_all("p")) #获取所有为p标签的内容，为列表
print(soup1.find_all("p")[1]) #通过索引获取列表的内容

print(up1.a.get("href"))#获取元素属性的值，类似字典的语法
print(soup1.a["href"])#获取属性的值