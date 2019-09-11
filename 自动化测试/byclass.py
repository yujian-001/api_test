from selenium import webdriver
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
#打开本地的html文件，只能用绝对路径打开html文件
driver.get(r"C:\Users\Administrator\PycharmProjects\selenium_test\自动化测试\test1.html")

#根据class的名字查找对象
ele=driver.find_element_by_class_name("cheese")
print(ele.text)