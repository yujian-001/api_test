from selenium import webdriver
driver=webdriver.Chrome(r"E:\chromedriver_win32\chromedriver.exe")
#打开本地的html文件，只能用绝对路径打开html文件
driver.get(r"C:\Users\Administrator\PycharmProjects\selenium_test\自动化测试\test1.html")

#partial，根据文本的部分内容来查找元素
ele=driver.find_element_by_partial_link_text("点击链接")
ele.click()