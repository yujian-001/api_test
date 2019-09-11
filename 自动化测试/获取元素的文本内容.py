from selenium import webdriver
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
driver.get(r'C:\Users\Administrator\PycharmProjects\selenium_test\自动化测试\test1.html')
element=driver.find_element_by_id("test")

print(element.text) #获取元素的文本内容
print(element.get_attribute("id")) #获取属性的值
print(element.get_attribute("outerHTML"))#获取元素对应的HTML代码
print(element.get_attribute("innerHTML"))#获取元素对应内部的HTML代码
a=element.get_attribute("innerHTML")
print(type(a))#字符串类型
driver.quit()